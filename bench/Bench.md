# 概要

`bench`目录是用于评估不同网页抽取仓库的抽取效果，比如`llm-webkit-mirror`，[unstructured](https://github.com/Unstructured-IO/unstructured)，[magic_html](https://github.com/opendatalab/magic-html)等。评测对象最小粒度是单个网页数据。

# 目录结构

数据集：原始网页数据在`bench/data/origin`目录下，GT默认保存在`bench/data/groundtruth`目录下。
评测结果：评测结果默认保存在`bench/output`目录下日期+随机数的文件夹中，如`20250212_113509_5bbf75c0`。

# 使用方法

```
python run.py
```

# 评估报告及评估指标

每一个评测结果包含`summary.json`和`detail.json`两个文件，`summary.json`是整个评测集的汇总结果，`detail.json`是单个网页的详细结果。

# 评估报告示例

`summary.json`主要展示所有评测数据“评测指标”，“评测耗时”的整体和元素级别的结果：

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

`detail.json`主要展示每个评测数据“评测指标”，“评测耗时”等元素级别的结果详情，方便分析哪一个网页的哪一个元素抽取效果不好：

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

# 如何新增评估数据

评测数据集会根据`pipeline`的功能迭代新增数据，如何快速构建新增数据的`groundtruth`按照下面方法：
