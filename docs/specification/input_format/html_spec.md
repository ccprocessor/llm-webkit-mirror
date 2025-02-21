# HTML文件输入格式标准

文件以jsonl组织，每一行是一个json对象，代表一个HTML文件。这个文件的内容是HTML文件的全文，以UTF-8编码。

## 样例

```json
{"track_id": "f7b3b1b4-0b1b", "url":"http://example.com/1.html", "dataset_name": "CC-TEST", "data_source_type": "HTML",  "html": "<html>.../html>", "file_bytes": 1000, "meta_info": {"input_datetime": "2020-01-01 00:00:00"}}
{"track_id": "f7b3b1b4-0b1c", "url":"http://example.com/2.html", "dataset_name": "CC-TEST", "data_source_type": "HTML",  "html": "<html>...</html>", "file_bytes": 1000, "meta_info": {"input_datetime": "2020-01-01 00:00:00"}}
```

每一行的json对象包含以下字段：

| 字段名字                  | 格式                           | 意义                                                                                                                | 是否必填        |
| ------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------- | --------------- |
| track_id                  | uuid                           | 全局唯一的ID                                                                                                        | 是              |
| dataset_name              | str                            | 数据集的名字（全局唯一），这个名字是管理员输入的，然后做索引的时候带到index里来                                     | 是              |
| data_source_category      | str                            | 这一行数据代表的是HTML，PDF，EBOOK,CC,labCC类型                                                                     | 是，此处是 HTML |
| html                      | 字符串                         | 以UTF-8为编码的HTML文件全文                                                                                         | 是              |
| url                       | 字符串                         | 这个文件的来源网址                                                                                                  | 是              |
| file_bytes                | 整数                           | 文件的size, 单位是byte                                                                                              | 是              |
| page_layout_type          | 字符串                         | 网页的layout分类：Article,QA,其他                                                                                   | 否              |
| meta_info                 | 字典                           | 存放关于文件的元信息:如果能从文件里获取到作者，制作日期等信息。或者数据本身就带有一些其他的信息都放入到这个字段里。 | 是              |
| meta_info->input_datetime | 其格式为 `yyyy-mm-dd HH:MM:SS` | 生成这个json索引文件这一条数据的时间，可以不用那么精确                                                              | 是              |
