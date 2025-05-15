import json
import time

import pyspark.sql.functions as F
from pyspark.sql import Window
from pyspark.sql.types import IntegerType, StringType, StructField, StructType
from xinghe.spark import new_spark_session, read_any_path, write_any_path

from jupyter.domain_clustering.libs.domain import compute_domain_hash

# 配置参数
MAX_RECORDS_PER_FILE = 100000  # 每个文件的目标记录数
HASH_COUNT = 10000


def load_domain_stats(spark, hash_id, stats_base_path, config):
    """加载已经统计好的域名统计数据.

    Args:
        spark: Spark会话
        hash_id: 哈希桶ID
        stats_base_path: 统计数据的基础路径
        config: 配置参数

    Returns:
        包含域名统计信息的DataFrame
    """
    try:
        # 加载统计数据
        stats_path = f"{stats_base_path}/{hash_id}.csv"
        print(f"加载域名统计数据: {stats_path}")

        # 使用read_any_path先读取文本文件
        text_df = read_any_path(spark, stats_path, config)

        # 检查是否包含value列
        if "value" in text_df.columns:
            try:
                # 将文本数据转换为CSV格式的DataFrame
                csv_df = spark.read.csv(
                    text_df.select("value").rdd.map(lambda r: r.value),
                    header=True,  # 第一行是标题
                    inferSchema=True
                )

                stats_df = csv_df
            except Exception as e:
                print(f"CSV转换失败: {str(e)}")
                # 直接使用文本数据作为备选方案
                stats_df = text_df
        else:
            # 如果没有value列，则可能已经是结构化数据
            stats_df = text_df

        # 预处理统计数据
        stats_df = stats_df.select(
            F.col("url_host_name").alias("domain"),
            F.lit(hash_id).alias("domain_hash_id"),
            F.col("count").cast(IntegerType())
        )

        # 检查是否包含必要的列
        required_columns = ["domain", "count"]
        for col in required_columns:
            if col not in stats_df.columns:
                raise ValueError(f"统计数据缺少必要的列: {col}")

        return stats_df

    except Exception as e:
        print(f"加载哈希桶 {hash_id} 的域名统计数据失败: {str(e)}")
        raise e


def calculate_file_indices(spark, stats_df):
    """根据域名统计数据计算每个域名的file_idx和需要的文件数
    确保每个file_idx中的实际记录数(count总和)接近MAX_RECORDS_PER_FILE.

    Args:
        spark: Spark会话
        stats_df: 包含域名统计信息的DataFrame

    Returns:
        包含域名、domain_hash_id、count和files_needed的DataFrame
    """
    # 1. 按域名出现频率降序排序
    window_spec = Window.partitionBy("domain_hash_id").orderBy(F.desc("count"), "domain")
    stats_df = stats_df.withColumn("row_number", F.row_number().over(window_spec))

    # 2. 使用累积求和统计记录数
    stats_df = stats_df.withColumn(
        "cumulative_count",
        F.sum("count").over(Window.partitionBy("domain_hash_id").orderBy("row_number"))
    )

    # 3. 计算基础file_idx (未考虑大域名拆分)
    stats_df = stats_df.withColumn(
        "base_file_idx",
        F.floor((F.col("cumulative_count") - F.col("count")) / F.lit(MAX_RECORDS_PER_FILE))
    )

    # 4. 计算每个域名需要的文件数量
    stats_df = stats_df.withColumn(
        "files_needed",
        F.ceil(F.col("count") / F.lit(MAX_RECORDS_PER_FILE))
    )

    # 5. 保留需要的列
    result_df = stats_df.select(
        "domain",
        "domain_hash_id",
        "count",
        "base_file_idx",
        "files_needed"
    )

    return result_df


def process_multiple_hash_buckets(spark, start_hash_id, end_hash_id, input_base_path, output_base_path, stats_base_path, config):
    """并行处理多个哈希桶.

    Args:
        spark: Spark会话
        start_hash_id: 起始哈希桶ID
        end_hash_id: 结束哈希桶ID
        input_base_path: 输入数据基础路径
        output_base_path: 输出数据基础路径
        stats_base_path: 统计数据基础路径
        config: 配置参数
    """
    try:
        hash_ids = list(range(start_hash_id, end_hash_id + 1))
        print(f"开始并行处理哈希桶 {start_hash_id} 到 {end_hash_id}")

        # 1. 并行加载所有哈希桶的统计数据
        stats_dfs = []
        for hash_id in hash_ids:
            try:
                stats_df = load_domain_stats(spark, hash_id, stats_base_path, config)
                stats_dfs.append(stats_df)
                print(f"已加载哈希桶 {hash_id} 的域名统计数据，共 {stats_df.count()} 条记录")
            except Exception as e:
                print(f"加载哈希桶 {hash_id} 的统计数据失败: {str(e)}")

        if not stats_dfs:
            print("没有成功加载任何哈希桶的统计数据，处理终止")
            return

        # 2. 合并所有统计数据
        combined_stats_df = stats_dfs[0]
        for df in stats_dfs[1:]:
            combined_stats_df = combined_stats_df.union(df)

        print(f"已合并所有哈希桶的统计数据，共 {combined_stats_df.count()} 条记录")

        # 3. 为所有域名计算file_idx
        domain_file_indices = calculate_file_indices(spark, combined_stats_df)
        print(f"已计算所有域名的file_idx，共 {domain_file_indices.count()} 条记录")

        # 4. 并行读取所有哈希桶的输入数据
        input_paths = list(f"{input_base_path}/{hash_id}" for hash_id in hash_ids)
        print(f"正在读取多个哈希桶输入数据: {input_paths}")

        # 使用逗号分隔的路径列表一次性读取所有数据
        input_df = read_any_path(spark, ",".join(input_paths), config)
        print(f"已读取所有哈希桶输入数据，共 {input_df.count()} 条记录")

        # 5. 确保输入数据包含domain
        if "domain" not in input_df.columns:
            # 解析JSON才能获取domain
            schema = StructType([
                StructField("domain", StringType(), True),
                StructField("url", StringType(), True)
            ])

            input_df = input_df.withColumn(
                "parsed",
                F.from_json(F.col("value"), schema)
            ).withColumn(
                "domain",
                F.col("parsed.domain")
            )

        # 将domain_file_indices广播给所有执行器
        domain_file_indices_broadcast = F.broadcast(domain_file_indices.select(
            "domain", "domain_hash_id", "base_file_idx", "files_needed"
        ))

        # 使用广播join
        processed_df = input_df.join(
            domain_file_indices_broadcast,
            "domain",
            "left"
        )

        # 为join后domain_hash_id为null的记录(即缺失域名)计算hash值
        compute_hash_udf = F.udf(lambda domain: compute_domain_hash(domain, HASH_COUNT) if domain else None, IntegerType())

        processed_df = processed_df.withColumn(
            "domain_hash_id",
            F.when(F.col("domain_hash_id").isNull(), compute_hash_udf(F.col("domain"))).otherwise(F.col("domain_hash_id"))
        ).withColumn(
            "base_file_idx",
            F.when(F.col("base_file_idx").isNull(), F.lit(0)).otherwise(F.col("base_file_idx"))
        ).withColumn(
            "files_needed",
            F.when(F.col("files_needed").isNull(), F.lit(1)).otherwise(F.col("files_needed"))
        )

        # 按照原始逻辑计算file_idx
        processed_df = processed_df.withColumn(
            "file_idx",
            F.when(
                F.col("files_needed") <= 1,
                F.col("base_file_idx")
            ).otherwise(
                F.col("base_file_idx") + F.floor(F.rand() * F.col("files_needed"))
            )
        ).na.fill(0, ["file_idx"])  # 对可能的NULL值填充0

        # 7. 更新JSON数据
        def update_json(json_str, file_idx, domain_hash_id):
            try:
                data = json.loads(json_str)
                data["file_idx"] = file_idx
                data["origin_sub_path"] = data.get("sub_path", "")
                sub_path = f"{domain_hash_id}/{file_idx}"
                data["sub_path"] = sub_path
                data["id"] = data.get("track_id", "")
                return json.dumps(data)
            except Exception as e:
                print(f"JSON更新错误: {e}")
                return json_str

        update_json_udf = F.udf(update_json, StringType())

        # 应用UDF更新JSON，使用domain_hash_id构建sub_path
        processed_df = processed_df.withColumn(
            "value",
            update_json_udf(F.col("value"), F.col("file_idx"), F.col("domain_hash_id"))
        )

        # 8. 准备输出的sub_path
        processed_df = processed_df.withColumn(
            "sub_path",
            F.concat(
                F.col("domain_hash_id").cast("string"),
                F.lit("/"),
                F.col("file_idx").cast("string")
            )
        )

        # 9. 移除临时列
        processed_df = processed_df.drop("base_file_idx", "files_needed")

        # 10. 按sub_path分区
        output_df = processed_df.repartition(
            F.col("sub_path")
        )
        print(f"output_df分区数: {output_df.rdd.getNumPartitions()}")

        # 11. 确保每个分区内按domain排序
        output_df = output_df.sortWithinPartitions("domain")

        # 12. 输出数据
        print(f"正在写入输出数据: {output_base_path}")

        write_any_path(output_df, output_base_path, config)
        print(f"已完成并行处理哈希桶 {start_hash_id} 到 {end_hash_id}")

    except Exception as e:
        print(f"并行处理哈希桶 {start_hash_id} 到 {end_hash_id} 时出错: {str(e)}")
        raise e


def process_hash_bucket_batch(start_hash_id, end_hash_id, input_base_path, output_base_path, stats_base_path, config, batch_size=20):
    """分批处理哈希桶，每批最多处理batch_size个，每个批次创建独立的Spark会话.

    Args:
        start_hash_id: 起始哈希桶ID
        end_hash_id: 结束哈希桶ID
        input_base_path: 输入数据基础路径
        output_base_path: 输出数据基础路径
        stats_base_path: 统计数据基础路径
        config: Spark配置
        batch_size: 每批处理的哈希桶数量
    """
    batch_count = 0

    for batch_start in range(start_hash_id, end_hash_id + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, end_hash_id)
        batch_count += 1

        try:
            print(f"开始处理批次 {batch_count}: 哈希桶 {batch_start} 到 {batch_end}")

            # 为每个批次创建独立的Spark会话
            session_name = f"cc_domain_stage2_{batch_start}_{batch_end}"
            spark = new_spark_session(session_name, config)
            sc = spark.sparkContext
            sc.setLogLevel("ERROR")

            try:
                # 将spark和config作为参数传递
                process_multiple_hash_buckets(spark, batch_start, batch_end, input_base_path, output_base_path, stats_base_path, config)
                print(f"成功处理哈希桶批次 {batch_start} 到 {batch_end}")
            except Exception as e:
                print(f"处理哈希桶批次 {batch_start} 到 {batch_end} 失败: {str(e)}")
            finally:
                # 无论处理成功还是失败，都关闭Spark会话
                print(f"关闭批次 {batch_count} 的Spark会话")
                spark.stop()

            # 可选：在批次之间添加延迟，让系统有时间释放资源
            time.sleep(10)  # 10秒延迟

        except Exception as e:
            print(f"批次 {batch_count} 处理过程中出现严重错误: {str(e)}")

    print(f"所有批次处理完成，共处理 {batch_count} 个批次")


# 主程序
if __name__ == '__main__':
    # 配置
    config = {
        'spark_conf_name': 'spark_4',
        'skip_success_check': True,
        'spark.yarn.queue': 'pipeline.clean',
        'spark.executor.memory': '80g',
        'spark.executor.memoryOverhead': '40g',  # 增加到40GB
        'output_compression': 'gz',
        'skip_output_check': True,
        'spark.network.timeout': '1200s',  # 网络超时
        'spark.broadcast.timeout': '1800s',  # 增加广播超时
        'spark.broadcast.compress': 'true',  # 确保广播压缩
        'spark.task.maxFailures': 8,
        'spark.shuffle.io.maxRetries': '10',  # 增加shuffle重试次数
        'spark.shuffle.io.retryWait': '60s',  # 增加重试等待时间
    }

    # 定义要处理的哈希桶范围
    START_HASH_ID = 0
    END_HASH_ID = 9999

    # 配置路径
    input_base_path = 's3://cc-store/cc-domain-stage1'
    output_base_path = 's3://cc-store/cc-domain-stage2'
    stats_base_path = 's3://cc-store/domain-hash-id-statics-201320-202513'

    # 开始并行处理
    print(f"开始并行处理哈希桶 {START_HASH_ID} 到 {END_HASH_ID}")
    process_hash_bucket_batch(START_HASH_ID, END_HASH_ID, input_base_path, output_base_path, stats_base_path, config)
    print('并行处理完成')
