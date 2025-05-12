import json

import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType, StringType, StructField, StructType
from xinghe.spark import new_spark_session, read_any_path, write_any_path

from cc_store.libs.domain import compute_domain_hash, extract_domain

# 配置参数
hash_count = 10000  # 域名哈希桶数量10000
target_records_per_file = 100000  # 每个文件的目标记录数100000
# 分区设置10000
numPartitions_id = 10000
numPartitions_subpath = 15000


# 优化后的file_idx计算函数
def process_with_precomputed_stats(df,
                                   stats_file_path,
                                   target_records_per_file=100000):
    """使用预计算的统计信息分配file_idx，避免使用窗口函数.

    Args:
        df: 输入DataFrame，需包含domain_hash_id列
        stats_file_path: 包含domain_hash_id统计信息的CSV文件路径
        target_records_per_file: 每个文件的目标记录数

    Returns:
        添加了file_idx的DataFrame
    """
    import math

    import pandas as pd
    from pyspark.sql.functions import floor, rand
    from pyspark.sql.types import IntegerType

    # 1. 读取统计信息
    stats_df = pd.read_csv(stats_file_path)

    # 2. 计算每个domain_hash_id需要的文件数量
    stats_df['files_needed'] = (stats_df['count'] /
                                target_records_per_file).apply(math.ceil)

    # 3. 创建映射字典：domain_hash_id -> files_needed
    hash_to_files = {
        int(row['domain_hash_id']): int(row['files_needed'])
        for _, row in stats_df.iterrows()
    }

    # 4. 创建映射DataFrame并广播
    # 明确定义schema
    schema = StructType([
        StructField('domain_hash_id', IntegerType(), False),
        StructField('files_needed', IntegerType(), False)
    ])

    files_needed_df = spark.createDataFrame(
        [(hash_id, files) for hash_id, files in hash_to_files.items()],
        schema=schema)

    # 5. 使用JOIN和内置函数分配file_idx（替代UDF）
    result_df = df.join(files_needed_df, 'domain_hash_id', 'left').withColumn(
        'file_idx', floor(rand() * F.col('files_needed'))).na.fill(
            0, ['file_idx'])  # 对可能的NULL值填充0

    # 6. 删除files_needed列，只保留需要的列
    result_columns = [col for col in df.columns] + ['file_idx']
    result_df = result_df.select(*result_columns)

    return result_df


# 注册UDF以在DataFrame操作中使用
extract_domain_udf = F.udf(extract_domain, StringType())
compute_domain_hash_udf = F.udf(compute_domain_hash, IntegerType())


# 使用预计算统计的方法处理
def process_with_df_api_and_file_indices_optimized(
        df, cc_dump, target_records_per_file=100000):
    """优化版的一体化处理函数，使用预计算统计代替窗口函数."""
    # 1. 提取url用于计算域名和哈希
    # 只定义需要提取的字段
    minimal_schema = StructType([
        StructField('url', StringType(), True),
        StructField('sub_path', StringType(), True)
    ])

    # 只解析这两个字段
    extracted_df = df.withColumn('parsed', F.from_json(F.col('value'), minimal_schema)) \
        .select(
            'value',
            F.col('parsed.url').alias('url'),
            F.col('parsed.sub_path').alias('original_sub_path'))

    # 2. 提取域名和计算哈希ID
    processed_df = extracted_df \
        .withColumn('domain', extract_domain_udf(F.col('url'))) \
        .withColumn('domain_hash_id', compute_domain_hash_udf(F.col('domain'), F.lit(hash_count))) \
        .filter(F.col('domain_hash_id').isNotNull()) \
        .filter(F.col('original_sub_path').isNotNull())

    # 3. 使用预计算统计分配file_idx
    stats_file_path = f"./statics/{cc_dump}_domain_hash_counts.csv"
    df_with_indices = process_with_precomputed_stats(processed_df,
                                                     stats_file_path,
                                                     target_records_per_file)

    # 4. 创建新的sub_path字段，包含domain_hash_id和file_idx
    def update_complete_json(json_str, domain, domain_hash_id, file_idx,
                             original_sub_path):
        """更新JSON，保留所有原始字段."""
        try:
            data = json.loads(json_str)
            # 添加新字段
            data['domain'] = domain
            data['domain_hash_id'] = domain_hash_id
            data['file_idx'] = file_idx
            # 更新sub_path
            data[
                'sub_path'] = f"{domain_hash_id}/{original_sub_path if original_sub_path else ''}/{file_idx}"
            return json.dumps(data)
        except Exception as e:
            print(f"JSON更新错误: {e}")
            return json_str

    # 注册UDF
    update_json_udf = F.udf(update_complete_json, StringType())

    # 应用UDF
    final_df = df_with_indices.withColumn(
        'value',
        update_json_udf(
            F.col('value'),  # 原始完整JSON
            F.col('domain'),
            F.col('domain_hash_id'),
            F.col('file_idx'),
            F.col('original_sub_path'))).withColumn(
                'sub_path',
                F.concat(
                    F.col('domain_hash_id').cast('string'), F.lit('/'),
                    F.col('original_sub_path'), F.lit('/'),
                    F.col('file_idx').cast('string'))).select(
                        'value', 'sub_path')  # 只保留value和sub_path列

    return final_df


config = {
    'spark_conf_name': 'spark_4',
    'skip_success_check': True,
    'spark.yarn.queue': 'pipeline.clean',
    # "spark.dynamicAllocation.maxExecutors":120,
    'spark.executor.memory': '80g',
    'spark.executor.memoryOverhead': '40g',  # 增加到40GB
    # "spark.speculation": "true",     # 启用推测执行
    # "maxRecordsPerFile": 200000,      # 增加每文件记录数以减少总文件数
    'output_compression': 'gz',
    'skip_output_check': True,
    'spark.sql.shuffle.partitions': '10000',
    'spark.default.parallelism': '10000',
    'spark.network.timeout': '1200s',  # 网络超时
    'spark.broadcast.timeout': '1800s',  # 增加广播超时
    'spark.broadcast.compress': 'true',  # 确保广播压缩
    'spark.task.maxFailures': 8,
}

DUMPS = [
    'CC-MAIN-2015-14',
    'CC-MAIN-2015-18',
    'CC-MAIN-2015-22',
    'CC-MAIN-2015-27',
    'CC-MAIN-2015-32',
    'CC-MAIN-2015-35',
    'CC-MAIN-2015-40',
    'CC-MAIN-2015-48',
    'CC-MAIN-2017-04',
    'CC-MAIN-2017-09',
    'CC-MAIN-2017-13',
    'CC-MAIN-2017-17',
    'CC-MAIN-2017-22',
    'CC-MAIN-2017-26',
    'CC-MAIN-2017-30',
    'CC-MAIN-2017-34',
    'CC-MAIN-2017-39',
    'CC-MAIN-2017-43',
    'CC-MAIN-2017-47',
    'CC-MAIN-2017-51',
    'CC-MAIN-2020-05',
    'CC-MAIN-2020-10',
    'CC-MAIN-2020-16',
    'CC-MAIN-2020-24',
    'CC-MAIN-2020-29',
    'CC-MAIN-2020-34',
    'CC-MAIN-2020-40',
    'CC-MAIN-2020-45',
    'CC-MAIN-2020-50',
    'CC-MAIN-2021-04',
    'CC-MAIN-2021-10',
    'CC-MAIN-2021-17',
    'CC-MAIN-2021-21',
    'CC-MAIN-2021-25',
    'CC-MAIN-2021-31',
    'CC-MAIN-2021-39',
    'CC-MAIN-2021-43',
    'CC-MAIN-2021-49',
    'CC-MAIN-2022-05',
    'CC-MAIN-2022-21',
    'CC-MAIN-2022-27',
    'CC-MAIN-2022-33',
    'CC-MAIN-2022-40',
    'CC-MAIN-2022-49',
]

for i, cc_dump in enumerate(DUMPS):
    print(f"=== 开始处理 {cc_dump} ===")

    spark = new_spark_session(f"cc_domain_hash_{cc_dump}", config)
    sc = spark.sparkContext
    sc.setLogLevel('ERROR')
    sc
    # ===== 主处理流程 =====
    # 读数据
    input_paths = [
        f"s3://input-data/{cc_dump}/",
    ]

    input_df = read_any_path(spark, ','.join(input_paths), config)

    # 使用一体化处理函数处理数据
    prepared_df = process_with_df_api_and_file_indices_optimized(
        input_df, cc_dump, target_records_per_file)

    regrouped_df = prepared_df.repartition(numPartitions_subpath, 'sub_path')

    # 写数据
    output_path = 's3://cc-store/cc-domain-stage1/'
    write_any_path(regrouped_df, output_path, config)
    print(f"{cc_dump} done!")
