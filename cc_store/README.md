# 简介

`cc-store`是针对全量Common Crawl按domain计算的需求场景设计更高效的domain-centric存储系统，使得domain级别的分析可分钟级别实现。

# 数据构建流程

## stage1: 分批将CC dump数据写入到domain hash桶内

具体流程图如下：

![CC_Store stage1 处理流程图](/docs/images/cc_store_stage1.png)

数据生产代码：

- [cc_store_stage1.py](./pipeline/cc_store_stage1.py) - 实现了 Stage1 的数据处理流程，将原始数据按域名分桶存储

数据存储结构如下：

```yaml
s3://cc-store-stage1/
  ├── CC-domain/                # 按域名排序的主数据
  │   ├── 0/                      # domain_hash_id, 按域名hash后分为1000个桶，xxhash.xxh64_intdigest(domain) % 1000
  │   │   ├── CC-MAIN-2013-20/          # 具体域名目录（domain normalize后）
  │   │   │   ├── 0/part-67fa76d24112-003956.jsonl.gz  # 10w条分割，file_idx=0
  │   │   │   └── 1/part-67fa76d24112-004656.jsonl.gz  # file_idx=1
  │   │   └── CC-MAIN-2013-48
  │   │   │   ├── 0/part-67fa76d24112-003956.jsonl.gz  # 10w条分割，file_idx=0
  │   ├── 1/
  │   │   └── ...
  │   └── ...

```

## stage2:  hash桶内聚合domain生成最终存储

具体流程图如下：

![CC_Store stage2 处理流程图](/docs/images/cc_store_stage2.png)

数据生产代码：

- [cc_store_stage2.py](./pipeline/cc_store_stage2.py) - 实现了 Stage2 的数据处理流程，将分桶数据按域名聚合并生成最终存储格式
- [cc_domain_index_gen.py](./pipeline/cc_domain_index_gen.py) - 实现了 Stage2 的最终数据domain维度的索引创建

数据存储结构如下：

```yaml
s3://cc-store-stage2/
  ├── data/                        # 主数据存储路径
  │   ├── 0/                    # domain_hash_id, 按域名hash后分为1000个桶，xxhash.xxh64_intdigest(domain) % 1000
  │   │   ├── 0/part-67fa76d24112-000001.jsonl.gz  # 包含多个域名的数据文件（约2GB）
  │   │   └── 1/part-67fa76d24112-000002.jsonl.gz
  │   └── ...
  │   ├── 1/
  │   │   └── 0/part-67fa76d24113-000001.jsonl.gz
  │   └── ...
  └── metadata/                    # 元数据存储
      │   ├── 0001.jsonl           # 对应桶内数据的索引文件
      │   ├── 0002.jsonl
      │   └── ...
```

文件索引格式如下：

```json
# 元数据结构
{
  "domain": "01-news.ru",                         # 域名
  "domain_hash_id": "1696",                       # domain_hash_id, 按域名hash后分为10000个桶，xxhash.xxh64_intdigest(domain) % 10000
  "count": 5000, # 该域名下所有的存储数量
  "files": [
    {
      "filepath": "s3://cc-store/data/1696/part-00001.jsonl.gz",  # 文件路径
      "offset": 0,                          # 该domain数据在文件中的起始bytes
      "length": 1250,                         # 该domain数据的偏移大小length
      "record_count": 125,                       # 该offset和length下doc数量
      "timestamp": 1674767988                    # 最后更新时间戳
    },
    # 可能有多个文件包含同一domain的数据
  ]
}
```

# cc-store数据读取

通过如下接口读取数据：

```python
rom xinghe.s3.read import read_s3_rows_from_offset

filepath = "s3://cc-store-stage2/data/11/16/part-681a543bbd05-001090.jsonl.gz"
offset = 257877031
record_count = 10

# 读取指定偏移量和数量的记录
rows = list(read_s3_rows_from_offset(filepath, offset=offset, limit=record_count))
```
