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
  "data_source_category": "CC",
  "path": "s3://cc-raw/crawl-data/CC-MAIN-xxx/"
}
{
  "dataset_name": "CC",
  "data_source_category": "CC",
  "path": "s3://cc-raw/crawl-data/CC-MAIN-xxx/"
}

```

字段说明：

| 字段                 | 类型   | 描述                                                                                | 是否必须 |
| -------------------- | ------ | ----------------------------------------------------------------------------------- | -------- |
| dataset_name         | string | 数据集的名字（全局唯一），这个名字是管理员输入的，然后做索引的时候带到index里来     | 是       |
| data_source_category | string | 这一行数据代表的是HTML、 PDF 、EBOOK 、AUDIO 、VIDEO、CC、labCC、TXT、MD类型        | 可选     |
| path                 | string | html源数据路径，其中 /CC-MAIN-xxx/ 表示dump index                                   | 是       |
| warc_idx             | string | 分类染色结果路径，其中 /CC-MAIN-xxx/ 表示dump index，CC-MAIN-xxx.jsonl 表示warc路径 | 是       |

path 文件中的字段说明：

| 字段            | 类型   | 描述            | 是否必须 |
| --------------- | ------ | --------------- | -------- |
| track_id        | string | 唯一标识        | 是       |
| url             | string | html页面url     | 是       |
| html            | string | 网页html源码    | 是       |
| status          | int    | 网页请求status  | 可选     |
| response_header | dict   | 网页请求header  | 可选     |
| date            | int    | 网页获取日期    | 可选     |
| content_length  | int    | content_length  | 可选     |
| content_charset | int    | content_charset | 可选     |
| remark          | dict   | remark          | 可选     |

warc_idx 文件中的字段说明：

| 字段               | 类型   | 描述                                            | 是否必须 |
| ------------------ | ------ | ----------------------------------------------- | -------- |
| track_id           | string | 唯一标识                                        | 是       |
| page_class         | string | html分类结果(other, article, forum, e-commerce) | 是       |
| url                | string | html页面url                                     | 可选     |
| url_host_name      | string | html域名                                        | 可选     |
| warc_filename      | string | html数据来源warc path                           | 可选     |
| filename           | string | html数据来源详细路径                            | 可选     |
| warc_record_offset | string | html数据 offset                                 | 可选     |
| warc_record_length | string | html数据 length                                 | 可选     |
| layout_id          | string | html layout({url_host_name}\_{layout_id})       | 可选     |
| model_version      | string | html 产生的批次(0.0.1)                          | 可选     |
