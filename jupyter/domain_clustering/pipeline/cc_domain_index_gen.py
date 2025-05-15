import json
import time

import pyspark.sql.functions as F
from pyspark.sql.types import (IntegerType, LongType, StringType, StructField,
                               StructType)
from xinghe.s3 import put_s3_object_with_retry
from xinghe.spark import new_spark_session, read_any_path

from jupyter.domain_clustering.libs.domain import compute_domain_hash


def analyze_file_offsets(file_path):
    """分析文件内容，获取每条记录的偏移量信息，并合并相同域名的记录.

    Args:
        file_path: S3文件路径

    Returns:
        记录的偏移量信息列表，按域名组织
    """
    # 使用字典来存储相同域名的记录
    domain_records = {}

    try:
        # 读取整个文件到DataFrame
        df = read_any_path(spark, file_path, config)

        # 定义UDF提取offset和length
        def extract_offset_length(doc_loc):
            if doc_loc and '?bytes=' in doc_loc:
                try:
                    _, param = doc_loc.split('?bytes=')
                    offset, length = map(int, param.split(','))
                    return (offset, length)
                except Exception as e:
                    print(f"提取offset和length时出错: {e}")
                    return (None, None)
            return (None, None)

        # 注册UDF，返回结构化类型
        offset_schema = StructType([
            StructField('offset', LongType(), True),
            StructField('length', LongType(), True)
        ])
        extract_offset_length_udf = F.udf(extract_offset_length, offset_schema)

        # 定义JSON结构
        schema = StructType([
            StructField('domain', StringType(), True),
            StructField('domain_hash_id', IntegerType(), True),
            StructField('doc_loc', StringType(), True)
            # 其他必要字段
        ])

        # 一次性解析JSON
        parsed_df = df.withColumn('parsed',
                                  F.from_json(F.col('value'), schema))

        # 提取所需字段
        df = parsed_df.select(
            F.col('parsed.domain').alias('domain'),
            F.col('parsed.domain_hash_id').alias('domain_hash_id'),
            F.col('parsed.doc_loc').alias('doc_loc'),
            'value',  # 保留原始值
            'filename'  # 保留filename列
        )

        # 然后提取offset和length
        df = df.withColumn(
            'loc_info',
            extract_offset_length_udf(F.col('doc_loc'))).withColumn(
                'offset', F.col('loc_info.offset')).withColumn(
                    'length',
                    F.col('loc_info.length')).drop('loc_info', 'doc_loc')

        # 过滤掉无效记录
        df = df.filter((F.col('domain').isNotNull())
                       & (F.col('offset').isNotNull())
                       & (F.col('length').isNotNull()))

        # 收集每个域名的记录信息，按文件路径分组
        domain_records_df = df.select(
            'domain',
            'domain_hash_id',
            'filename',  # 文件路径
            'offset',
            'length',
            F.struct(F.col('offset'),
                     F.col('length')).alias('record_info')).groupBy(
                         'domain', 'filename').agg(  # 按域名和文件路径分组
                             F.collect_list('record_info').alias('records'),
                             F.first('domain_hash_id').alias('domain_hash_id'),
                             F.count('*').alias('record_count'),
                             F.min('offset').alias('min_offset'),
                             F.max('offset').alias('max_offset'))  # 添加最大偏移量

        # 将DataFrame转换为字典格式
        domain_records = {}
        for row in domain_records_df.collect():
            domain = row['domain']
            domain_hash_id = row['domain_hash_id']
            filename = row['filename']

            # 如果domain_hash_id为空，使用计算值
            if domain_hash_id is None:
                domain_hash_id = compute_domain_hash(domain, HASH_COUNT)

            # 计算新的length，使用max(offset) - min(offset) + 1
            # 这种方法假设记录是连续的，没有大的空隙
            min_offset = row['min_offset']
            max_offset = row['max_offset']

            # 确保length大于0，处理边缘情况
            calculated_length = max(0, max_offset - min_offset)

            # 创建文件记录（字典形式）
            file_record = {
                'filepath': filename,
                'offset': min_offset,
                'length': calculated_length,  # 使用计算的长度
                'record_count': row['record_count'],
                'timestamp': int(time.time())
            }

            # 添加到域名记录中
            if domain not in domain_records:
                domain_records[domain] = {
                    'domain': domain,
                    'domain_hash_id': domain_hash_id,
                    'count': row['record_count'],
                    'files': [file_record]  # 初始化为包含当前文件记录的列表
                }
            else:
                # 已存在该域名，累加记录数并添加文件记录
                domain_records[domain]['count'] += row['record_count']
                domain_records[domain]['files'].append(file_record)

    except Exception as e:
        print(f"批量分析文件 {file_path} 的偏移量时出错: {str(e)}")

    # 将字典转换为列表，并按count降序排列
    offset_info = sorted(domain_records.values(),
                         key=lambda x: x['count'],
                         reverse=True)
    return offset_info


def process_file_index(file_info):
    """
    处理单个文件的索引生成 - Spark并行处理版本

    Args:
        file_info: 包含文件路径、哈希ID和路径信息的元组

    Returns:
        处理结果信息
    """
    file_path, hash_id, input_base_path, output_base_path = file_info

    try:
        # 分析文件获取偏移量信息
        domain_offset_info = analyze_file_offsets(file_path)

        if domain_offset_info:
            # 构建索引文件路径
            index_file_path = f"{output_base_path}/{hash_id}.jsonl"

            # 将偏移量信息转换为JSON
            index_json = '\n'.join(
                json.dumps(record) for record in domain_offset_info)

            # 写入S3
            put_s3_object_with_retry(index_file_path,
                                     index_json.encode('utf-8'))

            return {
                'status': 'success',
                'file': file_path,
                'domains': len(domain_offset_info)
            }
        else:
            return {
                'status': 'empty',
                'file': file_path,
                'reason': 'no domain records'
            }

    except Exception as e:
        error_msg = str(e)
        return {'status': 'error', 'file': file_path, 'error': error_msg}


def generate_domain_indices(input_base_path, output_base_path, start_hash_id,
                            end_hash_id):
    """为每个域名生成索引文件，按hash_id顺序处理.

    Args:
        input_base_path: 输入数据基础路径
        output_base_path: 输出数据基础路径
        start_hash_id: 起始哈希桶ID
        end_hash_id: 结束哈希桶ID
    """
    print(f"开始为域名生成索引文件，从 {input_base_path} 到 {output_base_path}")

    # 创建指定范围内的哈希ID列表
    hash_ids = list(range(start_hash_id, end_hash_id + 1))

    try:
        for hash_id in hash_ids:
            try:
                print(f"开始处理哈希桶 {hash_id}")

                # 构建输入路径
                input_path = f"{input_base_path}/{hash_id}"

                # 构建参数元组
                file_info = (input_path, hash_id, input_base_path,
                             output_base_path)

                # 执行process_file_index
                result = process_file_index(file_info)

                # 输出处理结果
                if result['status'] == 'success':
                    print(
                        f"哈希桶 {hash_id} 处理成功，包含 {result.get('domains', 0)} 个域名"
                    )
                elif result['status'] == 'empty':
                    print(f"哈希桶 {hash_id} 没有域名记录")
                else:
                    print(f"哈希桶 {hash_id} 处理失败: {result.get('error', '未知错误')}")

            except Exception as e:
                print(f"处理哈希桶 {hash_id} 时出错: {str(e)}")

    except Exception as e:
        print(f"处理索引时出错: {str(e)}")


# =====主函数=====
# 配置
config = {
    'spark_conf_name': 'spark_4',
    'skip_success_check': True,
    # "spark.yarn.queue": "pipeline.clean",
    # "spark.dynamicAllocation.maxExecutors":120,
    'spark.executor.memory': '80g',
    'spark.executor.memoryOverhead': '40g',  # 增加到40GB
    # "spark.speculation": "true",     # 启用推测执行
    # "maxRecordsPerFile": 200000,      # 增加每文件记录数以减少总文件数
    'output_compression': 'gz',
    'skip_output_check': True,
    # "spark.sql.shuffle.partitions": "10000",
    # "spark.default.parallelism": "10000",
    'spark.network.timeout': '1200s',  # 网络超时
    'spark.broadcast.timeout': '1800s',  # 增加广播超时
    'spark.broadcast.compress': 'true',  # 确保广播压缩
    'spark.task.maxFailures': 8,
}

# 配置参数
HASH_COUNT = 10000  # 总域名哈希桶数量
START_HASH_ID = 5  # 起始哈希桶ID
END_HASH_ID = 10  # 结束哈希桶ID（包含）
MAX_RECORDS_PER_FILE = 100000  # 每个存储文件的最大记录数

# 定义重要域名阈值
IMPORTANT_DOMAIN_THRESHOLD = 100000  # ≥10万记录的视为重要域名（用于区分hot/cold）

# 创建Spark会话
spark = new_spark_session(f"cc_domain_index_{START_HASH_ID}_{END_HASH_ID}",
                          config)
sc = spark.sparkContext
sc.setLogLevel('ERROR')
sc

# 配置参数
input_base_path = 's3://cc-store/cc-domain-stage2'  # 输入数据基础路径
output_base_path = 's3://cc-store/cc-domain-index'  # 输出数据基础路径

# 生成域名索引
print('开始生成域名索引...')
generate_domain_indices(input_base_path, output_base_path, START_HASH_ID,
                        END_HASH_ID)

print('处理完成')
