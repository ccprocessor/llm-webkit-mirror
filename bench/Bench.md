# 概要

`bench`目录是用于评估不同网页抽取仓库的抽取效果，比如`llm-webkit-mirror`，[unstructured](https://github.com/Unstructured-IO/unstructured)，[magic_html](https://github.com/opendatalab/magic-html)等。评测对象最小粒度是单个网页数据。

# 目录结构

- `bench/config/data_config.jsonl`: 数据处理配置文件
- `bench/config/ours_config.jsonc`: 提取器配置文件
- `bench/eval/`: 不同评估工具的实现
- `bench/common/`: 通用评估工具和指标计算
- `bench/output/`: 评测结果输出目录

数据集：原始网页数据在`bench/data/origin`目录下，GT默认保存在`bench/data/groundtruth`目录下。
评测结果：评测结果默认保存在`bench/output/{task_id}`目录下，其中`task_id`为UUID形式，如`5bbf7c8c-e8f2-11ef-a5a8-acde48001122`。

# 使用方法

## 命令行参数

```bash
python bench/run.py [--input INPUT_PATH] [--output OUTPUT_PATH] [--tool {ours,magic_html,unstructured}]
```

参数说明:

- `--input`: 指定HTML文件路径
- `--output`: 指定输出结果保存路径
- `--tool`: 选择使用的提取工具，可选值:
  - `ours`: 使用本项目提供的提取工具(默认)
  - `magic_html`: 使用magic_html工具进行评估
  - `unstructured`: 使用unstructured工具进行评估

## 运行示例

1. 使用默认提取器运行评估:

```bash
python bench/run.py
```

2. 使用其他提取器进行对比:

```bash
python bench/run.py --tool magic_html
```

3. 指定输入和输出路径:

```bash
python bench/run.py --input path/to/input.html --output path/to/output
```

# 评估报告及评估指标

每一个评测结果包含`summary.json`和`detail.json`两个文件，`summary.json`是整个评测集的汇总结果，`detail.json`是单个网页的详细结果。

主要评估指标包括:

- `type_acc`: 元素类型识别准确率
- `content_acc`: 元素内容识别准确率
- 各种元素类型的识别统计

# 评估报告示例

`summary.json`主要展示所有评测数据"评测指标"，"评测耗时"的整体和元素级别的结果：

```json
{
    "task_id": "5bbf7c8c-e8f2-11ef-a5a8-acde48001122",  # 评测任务唯一id
    "output_path": "outputs/20250212_113509_5bbf75c0",  # 评测结果保存路径
    "create_time": "20250212_113509",  # 评测任务创建时间
    "finish_time": "20250212_113632",  # 评测任务完成时间
    "total": 52002,  # 总评测文件数量
    "result_summary": { # 评测结果
        "Overall": {
            "count": 52000, # 元素数量
            "type_acc": 0.9997, # 元素类型识别准确性
            "content_acc": 0.9997 # 元素内容识别准确性
        },
        "equation-interline": {
            "count": 52, # 元素数量
            "type_acc": 0.9997, # 元素类型识别准确性
            "content_acc": 0.9997 # 元素内容识别准确性
        },
        "code": {
            "count": 5, # 元素数量
            "type_acc": 0.9997, # 元素类型识别准确性
            "content_acc": 0.9997 # 元素内容识别准确性
        },
        ...
    },
    "error_summary": {
        "count": 2, # 错误数量
    }
}
```

`detail.json`主要展示每个评测数据"评测指标"，"评测耗时"等元素级别的结果详情，方便分析哪一个网页的哪一个元素抽取效果不好：

```json
{
    "task_id": "5bbf7c8c-e8f2-11ef-a5a8-acde48001122",  # 评测任务唯一id
    "output_path": "outputs/20250212_113509_5bbf75c0",  # 评测结果保存路径
    "create_time": "20250212_113509",  # 评测任务创建时间
    "finish_time": "20250212_113632",  # 评测任务完成时间
    "result_detail": {
        "success_result": [
            {
                "file_path": "html/ccmath/1.html",  # 评测文件路径
                "result": { # 评测结果
                    "Overall": {
                        "count": 52000, # 元素数量
                        "type_acc": 0.9997, # 元素类型识别准确性
                        "content_acc": 0.9997 # 元素内容识别准确性
                    },
                    "equation-interline": {
                        "count": 52, # 元素数量
                        "type_acc": 0.9997, # 元素类型识别准确性
                        "content_acc": 0.9997 # 元素内容识别准确性
                    },
                    "code": {
                        "count": 5, # 元素数量
                        "type_acc": 0.9997, # 元素类型识别准确性
                        "content_acc": 0.9997 # 元素内容识别准确性
                    },
                    ...
                }
            },
            ...
        ],
        "error_result": [ # 抽取失败的网页
            {
                "file_path": "html/ccmath/1.html", # 评测文件路径
                "error_detail": "type_error" # 错误详情
            },
            ...
        ]
    }
}
```

# 输出文件格式

评估结果将保存在指定的输出目录中，针对不同工具的输出格式如下:

## `ours`工具输出

输出为JSONL格式，每行是一个JSON对象，包含以下字段:

- `url`: 原始网页URL
- `content`: 提取的内容
- `main_html`: 提取的主要HTML内容
- `content_list`: 提取的内容列表
- `html`: 原始HTML
- `statics`: 统计信息

## `magic_html`和`unstructured`工具输出

输出为JSONL格式，每行是一个JSON对象，包含以下字段:

- `url`: 原始网页URL
- `content`: 提取的内容
- `html`: 原始HTML

# 故障排除

## 常见问题

1. 文件路径问题

   如果遇到文件路径相关错误，请检查:

   - 配置文件中的路径是否正确
   - 文件路径是否存在
   - 是否有足够的权限读写相关目录

2. 编码问题

   对于包含XML声明的HTML文件，系统会自动进行转换处理。如果遇到编码相关错误，可以:

   - 确保HTML文件使用UTF-8编码
   - 检查XML声明是否正确格式化

3. 结果输出问题

   若输出目录创建失败或结果无法写入:

   - 检查目标目录的写入权限
   - 确保磁盘空间足够

# 如何新增评估数据

评测数据集会根据`pipeline`的功能迭代新增数据，如何快速构建新增数据的`groundtruth`按照下面方法：

1. 准备原始HTML文件，放入`bench/data/origin`目录下
2. 在`bench/config/data_config.jsonl`中添加新的测试数据条目
3. 运行评估工具生成初步结果
4. 人工审核并修正结果作为groundtruth，放入`bench/data/groundtruth`目录
