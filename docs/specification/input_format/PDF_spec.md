# 文档数据流水线输入格式标准

此标准定义的格式标准的使用在：[pipeline_pdf_tpl.jsonc](../../../llm-web-kit/pipeline/pipe_tpl/pipeline_pdf_tpl.jsonc)
其中 `formatted_raw_input_data_output_path` 字段中制定的路径中数据需要满足本标准。

## 样例

```json lines
{"track_id": "xxx", "dataset_name":"books-1", "data_source_type":"PDF", "raw_file_path":"s3://bucket-unzip/ds_name/研报.docx", "path":"s3://bucket-input/ds_name/研报.pdf", "file_bytes":10024, "md5":"xxabdcdeaefdsfsf", "page_num":512, "is_dup":false, "meta_info":{"input_datetime":"2024-02-01 12:59:50"}}
{"track_id": "ccc", "dataset_name":"books-1", "data_source_type":"PDF", "raw_file_path":"s3://bucket-unzip/ds_name/盐铁论.doc", "path":"s3://bucket-input/ds_name/盐铁论.pdf", "file_bytes":6666, "md5":"bcdesdfdsfdsfai", "page_num":212, "is_dup":false, "meta_info":{"input_datetime":"2024-02-01 12:59:50"}}
{"track_id": "ddd", "dataset_name":"books-1", "data_source_type":"PDF", "raw_file_path":"s3://bucket-unzip/ds_name/大学物理.ppt", "path":"s3://bucket-input/ds_name/大学物理.pdf", "file_bytes":2323, "md5":"xxabdcdeaefdsfsf", "page_num":300, "is_dup":false, "meta_info":{"input_datetime":"2024-02-01 12:59:50"}}
{"track_id": "eee", "dataset_name":"books-1", "data_source_type":"PDF", "raw_file_path":"s3://bucket-unzip/ds_name/小学数学.docx", "path":"s3://bucket-input/ds_name/小学数学.pdf", "file_bytes":8500000, "md5":"xxabdcdeaefdsfsf", "page_num":900, "is_dup":false, "meta_info":{"input_datetime":"2024-02-01 12:59:50"}}
{"track_id": "fff", "dataset_name":"books-1", "data_source_type":"PDF", "path":"s3://bucket-input/ds_name/C语言程序设计.pdf", "file_bytes":8500000, "md5":"xxabdcdeaefdsfsf", "page_num":900, "is_dup":false, "meta_info":{"input_datetime":"2024-02-01 12:59:50"}}

```

## 字段说明

| 字段名                    | 格式                                 | 意义                                                                                                  | 是否必填                               |
| ------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------- | -------------------------------------- |
| track_id                  | uuid                                 | 全局唯一的ID                                                                                          | 是                                     |
| dataset_name              | str                                  | 数据集的名字（全局唯一），这个名字是管理员输入的，然后做索引的时候带到index里来                       | 是                                     |
| data_source_category      | str                                  | 这一行数据代表的是HTML、 PDF 、EBOOK 、AUDIO 、VIDEO、CC、labCC、TXT、MD类型。                        | 是，此处是 PDF或EBOOK                  |
| raw_file_path             | 字符串                               | s3全路径                                                                                              | 否，如果文件没有发生格式转换，则非必填 |
| path                      | 字符串                               | s3全路径                                                                                              | 是                                     |
| file_bytes                | 整数                                 | 文件的大小，单位是byte                                                                                | 是                                     |
| md5                       | 字符串                               | 文件二进制的md5值，用于文件级别去重                                                                   | 是                                     |
| page_num                  | 整数                                 | PDF文件有多少页；如果文件损坏则写为0，并且相对应的`is_bad_file=true`                                  | 是                                     |
| is_dup                    | 布尔类型                             | 文件是否重复，如果重复则下游不再处理                                                                  | 是                                     |
| is_bad_file               | 布尔类型                             | 是否是损坏的文件                                                                                      | 是                                     |
| meta_info                 | 字典                                 | 存放关于文件的元信息：如果能从文件里获取到作者、制作日期等信息，或者数据本身就带有一些其他信息都放入到这个字段里 | 是                                     |
| meta_info->input_datetime | datetime (格式：yyyy-mm-dd HH:MM:SS) | 生成这个json索引文件这一条数据的时间，可以不用那么精确                                                | 是                                     |
