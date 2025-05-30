# Introduction

`cc-store` is a more efficient domain-centric storage system designed for scenarios that require domain-level computation on the entire Common Crawl dataset, enabling domain-level analysis to be completed in seconds.

# Data Construction Pipeline

## Stage 1: Batch Writing CC Dump Data into Domain Hash Buckets

The detailed workflow is as follows:

![CC_Store Stage 1 Processing Workflow](/docs/images/cc_store_stage1.png)

Data production code:

- [cc_store_stage1.py](./pipeline/cc_store_stage1.py) - Implements the Stage 1 data processing pipeline, storing raw data in buckets organized by domain

Data storage structure:

```yaml
s3://cc-store-stage1/
  ├── CC-domain/                # Main data sorted by domain
  │   ├── 0000/                      # domain_hash_id, domains are hashed into 1000 buckets using xxhash.xxh64_intdigest(domain) % 1000
  │   │   ├── CC-MAIN-2013-20/          # Specific domain directory (after domain normalization)
  │   │   │   ├── 0/part-67fa76d24112-003956.jsonl.gz  # Split into 100k records, file_idx=0
  │   │   │   └── 1/part-67fa76d24112-004656.jsonl.gz  # file_idx=1
  │   │   └── CC-MAIN-2013-48
  │   │   │   ├── 0/part-67fa76d24112-003956.jsonl.gz  # Split into 100k records, file_idx=0
  │   ├── 0001/
  │   │   └── ...
  │   └── ...

```

## Stage 2: Aggregating Domains within Hash Buckets to Generate Final Storage

The detailed workflow is as follows:

![CC_Store Stage 2 Processing Workflow](/docs/images/cc_store_stage2.png)

Data production code:

- [cc_store_stage2.py](./pipeline/cc_store_stage2.py) - Implements the Stage 2 data processing pipeline, aggregating bucketed data by domain and generating the final storage format
- [cc_domain_index_gen.py](./pipeline/cc_domain_index_gen.py) - Implements the creation of domain-level indexes for Stage 2 final data

Data storage structure:

```yaml
s3://cc-store-stage2/
  ├── data/                        # Main data storage path
  │   ├── 0000/                    # domain_hash_id, domains are hashed into 1000 buckets using xxhash.xxh64_intdigest(domain) % 1000
  │   │   ├── 0/part-67fa76d24112-000001.jsonl.gz  # Data file containing multiple domains (~2GB)
  │   │   └── 1/part-67fa76d24112-000002.jsonl.gz
  │   └── ...
  │   ├── 0001/
  │   │   └── 0/part-67fa76d24113-000001.jsonl.gz
  │   └── ...
  └── metadata/                    # Metadata storage
      │   ├── 0001.jsonl           # Index file for corresponding bucket data
      │   ├── 0002.jsonl
      │   └── ...
```

File index format:

```json
# Metadata structure
{
  "domain": "01-news.ru",                         # Domain name
  "domain_hash_id": "1696",                       # domain_hash_id, domains are hashed into 10000 buckets using xxhash.xxh64_intdigest(domain) % 10000
  "count": 5000, # Total number of records stored for this domain
  "files": [
    {
      "filepath": "s3://cc-store-stage2/data/1696/part-00001.jsonl.gz",  # File path
      "offset": 0,                          # Starting byte offset for this domain's data in the file
      "length": 1250,                         # Length of this domain's data
      "record_count": 125,                       # Number of documents within this offset and length
      "timestamp": 1674767988                    # Last update timestamp
    },
    # Multiple files may contain data for the same domain
  ]
}
```

# Reading cc-store Data

Read data using the following interface:

```python
from xinghe.s3.read import read_s3_rows_from_offset

filepath = "s3://cc-store-stage2/data/11/16/part-681a543bbd05-001090.jsonl.gz"
offset = 257877031
record_count = 10

# Read records from specified offset and count
rows = list(read_s3_rows_from_offset(filepath, offset=offset, limit=record_count))
```
