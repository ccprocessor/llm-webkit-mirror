# html layout classify layout分类

## 环境

配置 .xinghe.yaml
配置 .llm_web_kit.jsonc

## 入参

layout_sample_dir: 每个layout_id 随机选取3条的.jsonl文件路径或文件夹路径
layout_classify_dir：计算每个layout_id 对应的分类结果文件夹路径

layout_sample_dir 字段说明：

| 字段      | 类型   | 描述                         | 是否必须 |
| --------- | ------ | ---------------------------- | -------- |
| layout_id | string | layout id                    | 是       |
| url       | string | 数据url                      | 是       |
| simp_html | string | html原数据经过简化处理的html | 是       |

layout_classify_dir 字段说明：

| 字段          | 类型   | 描述                                                            | 是否必须 |
| ------------- | ------ | --------------------------------------------------------------- | -------- |
| url_list      | list   | layout id 对应的url                                             | 是       |
| layout_id     | string | layout id                                                       | 是       |
| page_type     | string | layout_id 经过分类之后的分类结果（'other', 'article', 'forum'） | 是       |
| max_pred_prod | float  | 分类模型的分类可靠度                                            | 是       |
| version       | string | 模型版本                                                        | 是       |
