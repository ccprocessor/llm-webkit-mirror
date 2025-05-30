import json
import time
import traceback
from datetime import datetime

import pyspark.sql.functions as F
import xxhash
from pyspark.sql.types import (ArrayType, IntegerType, LongType, StringType,
                               StructField, StructType)
from xinghe.s3 import (S3DocWriter, list_s3_objects, read_s3_rows,
                       write_any_path)
from xinghe.spark import new_spark_session


def generate_domain_indices_parallel_optimized(input_base_path, output_base_path, start_hash_id, end_hash_id, batch_size=100):
    """
    改进的并行索引生成方法 - 一次性读取多个哈希桶的数据，避免多次IO

    Args:
        input_base_path: 输入数据基础路径
        output_base_path: 输出数据基础路径
        start_hash_id: 起始哈希桶ID
        end_hash_id: 结束哈希桶ID
        batch_size: 每批处理的哈希桶数量，默认为100
    """
    print(f"开始优化并行处理，从 {input_base_path} 到 {output_base_path}，批次大小: {batch_size}")

    try:
        # 创建指定范围内的哈希ID列表
        hash_ids = list(range(start_hash_id, end_hash_id + 1))

        # 将哈希ID列表分成多个批次
        total_hash_ids = len(hash_ids)
        batches = [hash_ids[i:i + batch_size] for i in range(0, total_hash_ids, batch_size)]

        print(f"总共 {total_hash_ids} 个哈希桶，分成 {len(batches)} 个批次处理")

        # 记录处理开始时间
        import time
        start_time = time.time()

        # 处理每个批次
        for batch_idx, batch_hash_ids in enumerate(batches):
            batch_start = time.time()
            batch_start_id = min(batch_hash_ids)
            batch_end_id = max(batch_hash_ids)

            # 为每个批次创建独立的Spark会话
            session_name = f"cc_domain_index_{batch_start_id}_{batch_end_id}"
            spark = new_spark_session(session_name, config)
            sc = spark.sparkContext
            sc.setLogLevel("ERROR")

            print(f"开始处理批次 {batch_idx + 1}/{len(batches)}, 哈希桶范围: {batch_start_id}-{batch_end_id}, 包含 {len(batch_hash_ids)} 个哈希桶")

            try:
                # 1. 收集所有输入文件路径
                all_input_paths = []
                for hash_id in batch_hash_ids:
                    input_path = f"{input_base_path}/{hash_id}"
                    file_paths = [f for f in list(list_s3_objects(input_path, recursive=True)) if f.endswith(".gz")]
                    all_input_paths.extend(file_paths)

                print(f"批次 {batch_idx + 1} 共收集到 {len(all_input_paths)} 个输入文件")

                if len(all_input_paths) == 0:
                    print(f"批次 {batch_idx + 1} 没有找到符合条件的输入文件，跳过处理")
                    continue

                # 2. 使用 parallelize 并行处理文件
                file_rdd = sc.parallelize(all_input_paths, len(all_input_paths))  # 调整分区数以优化处理

                # 3. 定义记录模式
                schema = StructType([
                    StructField("domain", StringType(), True),
                    StructField("domain_hash_id", IntegerType(), True),
                    StructField("count", LongType(), True),
                    StructField("files", ArrayType(StructType([
                        StructField("filepath", StringType(), True),
                        StructField("offset", LongType(), True),
                        StructField("length", LongType(), True),
                        StructField("record_count", LongType(), True),
                        StructField("timestamp", IntegerType(), True),
                    ])), True),
                ])

                # 4. 生成域名记录DataFrame
                domain_records_df = file_rdd.mapPartitions(process_domain_records_file).toDF(schema)

                # 5. 按域名聚合，合并来自不同文件的记录
                grouped_df = domain_records_df.groupBy("domain", "domain_hash_id").agg(
                    F.sum("count").alias("count"),
                    F.flatten(F.collect_list("files")).alias("files")
                )

                # 6. 处理结果，将结果转换为标准输出格式
                domain_offset_df = grouped_df.select(
                    "domain",
                    "domain_hash_id",
                    "count",
                    "files"
                ).withColumn(
                    "sub_path",
                    F.col("domain_hash_id").cast("string")
                ).repartition(batch_size, "sub_path").sortWithinPartitions(F.col("count").desc())

                # 7. 转换为JSON格式
                print(f"准备写入批次 {batch_idx + 1} 数据到: {output_base_path}")

                struct_col = F.struct(
                    domain_offset_df["domain"],
                    domain_offset_df["domain_hash_id"],
                    domain_offset_df["count"],
                    domain_offset_df["files"],
                    domain_offset_df["sub_path"]
                )
                output_df = domain_offset_df.withColumn("value", F.to_json(struct_col)).select("value")
                print(f"output_df分区数: {output_df.rdd.getNumPartitions()}")

                # 8. 写入输出路径
                write_any_path(output_df, output_base_path, config)

                print(f"批次 {batch_idx + 1} 处理完成，写入文件: {output_base_path}")

                # 记录批次处理时间
                batch_time = time.time() - batch_start
                print(f"批次 {batch_idx + 1} 处理耗时: {batch_time:.2f} 秒")

            except Exception as e:
                import traceback
                print(f"处理批次 {batch_idx + 1} 时出错: {str(e)}")
                print(traceback.format_exc())
            finally:
                # 无论处理成功还是失败，都关闭Spark会话
                print(f"关闭批次 {batch_idx + 1} 的Spark会话")
                spark.stop()

        # 记录总处理时间
        total_time = time.time() - start_time
        print(f"所有批次处理完成，总耗时: {total_time:.2f} 秒，平均每批次: {total_time / len(batches):.2f} 秒")

    except Exception as e:
        import traceback
        print(f"优化并行处理索引时出错: {str(e)}")
        print(traceback.format_exc())


def process_domain_records_file(_iter):
    """处理文件并生成域名记录索引.

    Args:
        _iter: 文件路径迭代器

    Yields:
        域名记录信息
    """
    # 错误日志存放地址
    error_log_path = "s3://cc-store/error_logs/domain_index_errors.jsonl"
    print(f"error_log_path: {error_log_path}")
    s3_doc_writer = S3DocWriter(path=error_log_path)
    error_info = None

    for fpath in _iter:
        print(f"处理文件: {fpath}")
        current_domain = None
        start_offset = None
        domain_length = 0
        idx = 0
        last_detail_data = None

        try:
            for row in read_s3_rows(fpath):
                idx += 1
                try:
                    detail_data = json.loads(row.value)
                    domain = detail_data["domain"]
                    domain_hash_id = detail_data.get("domain_hash_id")
                    offset, length = map(int, row.loc.split("bytes=")[-1].split(",")) if "bytes=" in row.loc else (0, len(row.value))

                    # 如果是同一个域名的连续记录，累计长度
                    if domain == current_domain:
                        domain_length += length
                        last_detail_data = detail_data
                        continue
                    else:
                        # 如果已有域名记录，则生成一条记录
                        if current_domain is not None:
                            print(f"{current_domain} 该批数据批次结束, 总数据量为: {idx - 1}")
                            # 如果domain_hash_id为空，使用计算值
                            current_domain_hash_id = None
                            if last_detail_data and "domain_hash_id" in last_detail_data:
                                current_domain_hash_id = last_detail_data["domain_hash_id"]
                            if current_domain_hash_id is None:
                                current_domain_hash_id = xxhash.xxh64_intdigest(current_domain) % HASH_COUNT

                            line = {
                                "domain": current_domain,
                                "domain_hash_id": current_domain_hash_id,
                                "count": idx - 1,
                                "files": [{
                                    "filepath": fpath,
                                    "offset": start_offset,
                                    "length": domain_length,
                                    "record_count": idx - 1,
                                    "timestamp": int(time.time())
                                }]
                            }
                            yield line
                            idx = 1

                        # 开始新的域名记录
                        current_domain = domain
                        start_offset = offset
                        domain_length = length
                        last_detail_data = detail_data
                        print(f"新批次数据: {current_domain}, start_offset: {start_offset}, domain_length: {domain_length}")
                except Exception as e:
                    error_info = {
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "traceback": traceback.format_exc(),
                        "input_data": row.value if hasattr(row, 'value') else str(row),
                        "file_path": fpath,
                        "timestamp": datetime.now().isoformat()
                    }
                    s3_doc_writer.write(error_info)
                    continue

            # 处理文件末尾的最后一个域名
            if current_domain is not None and last_detail_data is not None:
                print(f"last: {current_domain} 该批数据批次结束, 总数据量为: {idx}")
                # 如果domain_hash_id为空，使用计算值
                domain_hash_id = last_detail_data.get("domain_hash_id")
                if domain_hash_id is None:
                    domain_hash_id = xxhash.xxh64_intdigest(current_domain) % HASH_COUNT

                line = {
                    "domain": current_domain,
                    "domain_hash_id": domain_hash_id,
                    "count": idx,
                    "files": [{
                        "filepath": fpath,
                        "offset": start_offset,
                        "length": domain_length,
                        "record_count": idx,
                        "timestamp": int(time.time())
                    }]
                }
                yield line
        except Exception as e:
            error_info = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": traceback.format_exc(),
                "file_path": fpath,
                "timestamp": datetime.now().isoformat()
            }
            s3_doc_writer.write(error_info)

    if error_info:
        s3_doc_writer.flush()


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
generate_domain_indices_parallel_optimized(input_base_path, output_base_path, START_HASH_ID,
                        END_HASH_ID)

print('处理完成')
