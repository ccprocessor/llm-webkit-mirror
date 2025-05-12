import io

import pyspark.sql.functions as F
from pyspark.sql import Window
from pyspark.sql.types import IntegerType
from xinghe.s3 import put_s3_object_with_retry
from xinghe.spark import new_spark_session, read_any_path

from cc_store.libs.domain import compute_domain_hash

# 配置参数
hash_count = 10000  # 域名哈希桶数量
max_hosts_per_bucket = 100000  # 每个桶保存的最大域名数量


compute_domain_hash_udf = F.udf(compute_domain_hash, IntegerType())


def analyze_domain_hash_distribution(input_df, output_dir):
    """分析每个domain_hash_id桶内url_host_name的分布情况."""
    # 确保列名存在
    if 'url_host_name' not in input_df.columns:
        print("Error: 'url_host_name' column does not exist in input data")
        possible_cols = input_df.columns
        print(f"Available columns: {possible_cols}")
        return

    # 添加domain_hash_id列
    processed_df = input_df \
        .withColumn('domain_hash_id', compute_domain_hash_udf(F.col('url_host_name'), F.lit(hash_count))) \
        .filter(F.col('domain_hash_id').isNotNull())

    # 按domain_hash_id和url_host_name进行分组并计数
    host_distribution = processed_df \
        .groupBy('domain_hash_id', 'url_host_name') \
        .count() \
        .orderBy(F.col('count').desc())

    # 使用窗口函数按domain_hash_id分区对url_host_name进行排名
    window_spec = Window.partitionBy('domain_hash_id').orderBy(F.col('count').desc())
    ranked_hosts = host_distribution \
        .withColumn('rank', F.row_number().over(window_spec)) \
        .filter(F.col('rank') <= max_hosts_per_bucket)  # 限制每个桶内的域名数量

    print('开始分析并保存domain_hash_id分布...')

    # 缓存数据以提高性能
    ranked_hosts.cache()

    # 优化1: 使用foreachPartition批量处理，避免单条记录操作
    def process_hash_id_partition(partition_iter):
        # 构建一个本地字典，用于临时存储每个hash_id的数据
        hash_id_data = {}

        # 首先将分区中的所有数据按hash_id分组到本地内存
        for row in partition_iter:
            hash_id = row['domain_hash_id']
            if hash_id not in hash_id_data:
                hash_id_data[hash_id] = []
            # 只保留需要的列
            hash_id_data[hash_id].append({
                'url_host_name': row['url_host_name'],
                'count': row['count'],
                'rank': row['rank']
            })

        # 然后批量处理每个hash_id的数据
        for hash_id, rows in hash_id_data.items():
            if rows:  # 如果有数据
                import io

                import pandas as pd

                # 创建Pandas DataFrame
                pdf = pd.DataFrame(rows)

                # 将DataFrame转换为CSV格式的字符串
                csv_buffer = io.StringIO()
                pdf.to_csv(csv_buffer, index=False)
                csv_text = csv_buffer.getvalue()

                # 准备S3路径
                s3_output_path = f"{output_dir}/{hash_id}.csv"

                # 使用xinghe库的put_s3_object_with_retry函数上传到S3
                body = csv_text.encode('utf-8')
                put_s3_object_with_retry(s3_output_path, body)

    # 优化2: 按domain_hash_id重新分区，确保相同hash_id的数据在同一分区
    # 这样可以减少跨分区的数据移动
    partitioned_hosts = ranked_hosts \
        .repartition('domain_hash_id') \
        .select('domain_hash_id', 'url_host_name', 'count', 'rank')

    # 使用foreachPartition并行处理
    partitioned_hosts.foreachPartition(process_hash_id_partition)

    # 生成汇总统计
    print('生成汇总统计...')
    bucket_summary = host_distribution \
        .groupBy('domain_hash_id') \
        .agg(
            F.count('url_host_name').alias('total_hosts'),
            F.sum('count').alias('total_records'),
            F.max('count').alias('max_host_count'),
            F.avg('count').alias('avg_host_count')
        ) \
        .orderBy(F.col('total_records').desc())

    # 优化3: 使用put_s3_object_with_retry写入汇总数据，与其他部分保持一致
    summary_output_path = f"{output_dir}/summary.csv"

    # 将DataFrame转换为Pandas再转为CSV字符串
    summary_pdf = bucket_summary.toPandas()
    csv_buffer = io.StringIO()
    summary_pdf.to_csv(csv_buffer, index=False)
    csv_text = csv_buffer.getvalue()

    # 使用xinghe库的put_s3_object_with_retry函数上传到S3
    body = csv_text.encode('utf-8')
    put_s3_object_with_retry(summary_output_path, body)

    # 显示前10个最大的桶的统计信息
    print('Top 10 domain_hash_id buckets by total records:')
    bucket_summary.show(10)

    # 释放缓存
    ranked_hosts.unpersist()

    return f"Analysis completed. Results saved to {output_dir}"


# 执行分析
if __name__ == '__main__':
    # Spark配置
    config = {
        'spark_conf_name': 'spark_4',
        'skip_success_check': True,
        'spark.yarn.queue': 'pipeline.clean',
        'input_format': 'parquet',
        'spark.executor.memory': '60g',
        'spark.executor.memoryOverhead': '40g',
        'spark.sql.shuffle.partitions': '10000',
        'spark.default.parallelism': '10000',
        'spark.network.timeout': '1200s',
        'spark.broadcast.timeout': '1800s',
        'spark.broadcast.compress': 'true',
    }

    # 创建Spark会话
    spark = new_spark_session('domain_hash_analysis', config)
    sc = spark.sparkContext
    sc.setLogLevel('ERROR')

    # 读取数据
    input_path = 's3://cc-raw/cc-index/table/cc-main/warc/'
    input_df = read_any_path(spark, ','.join(input_path), config)
    # 输出路径，S3路径
    output_dir = 's3://cc-domain-centric-store/domain-hash-id-statics'  # 改为您的S3目录路径
    result = analyze_domain_hash_distribution(input_df, output_dir)
    print(result)
    spark.stop()
