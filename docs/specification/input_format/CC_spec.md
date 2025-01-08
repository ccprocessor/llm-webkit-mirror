# CC 数据输入格式标准

此输入格式的用途是定义CC标准处理流程的输入数据格式。
在CC进入到提取之前，输入流水线的数据格式必须符合此标准。

此处的数据格式的使用方在：[pipeline_html_tpl.jsonc](../../../llm-web-kit/pipeline/pipe_tpl/pipeline_html_tpl.jsonc)
其中 `formatted_raw_input_data_output_path` 字段中制定的路径中数据需要满足本标准。

## 流水线输入数据格式

样例：

```json lines
{
  "dataset_name": "CC",
  "data_source_type": "HTML",
  "path": "s3://cc-raw/crawl-data/CC-MAIN-xxx/"
}
{
  "dataset_name": "CC",
  "data_source_type": "HTML",
  "path": "s3://cc-raw/crawl-data/CC-MAIN-xxx/"
}

```

字段说明：

| 字段             | 类型   | 描述                                                                            | 是否必须 |
| ---------------- | ------ | ------------------------------------------------------------------------------- | -------- |
| dataset_name     | string | 数据集的名字（全局唯一），这个名字是管理员输入的，然后做索引的时候带到index里来 | 可选     |
| data_source_type | string | 这一行数据代表的是HTML、 PDF 、EBOOK 、AUDIO 、VIDEO、CC、labCC、TXT、MD类型    | 可选     |
| path             | string | s3全路径，其中 /CC-MAIN-xxx/ 表示dump index                                     | 是       |

## 流水线输出数据格式

样例：

```json lines
{
  "output_path": "s3://web-parse-huawei/CC/categorized_data/v001/CC-MAIN-xxx/CC-MAIN-xxx.jsonl"
}
{
  "output_path": "s3://web-parse-huawei/CC/categorized_data/v001/CC-MAIN-xxx/CC-MAIN-xxx.jsonl"
}
```

字段说明：

| 字段        | 类型   | 描述                                                                               | 是否必须 |
| ----------- | ------ | ---------------------------------------------------------------------------------- | -------- |
| output_path | string | 数据输出路径，其中 /CC-MAIN-xxx/ 表示dump index，/CC-MAIN-xxx.jsonl 表示warc index | 是       |
