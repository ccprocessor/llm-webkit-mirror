# main html后处理

## 流程方案

![img.png](asserts/img.png)

## 执行步骤

| filename         | function                    | input & input_type                                        | output_type         | 实现功能       |
| :--------------- | :-------------------------- | :-------------------------------------------------------- | :------------------ | :------------- |
| choose_html.py   | select_typical_html         | html_strs: html迭代器                                     | str                 | 选出代表html   |
| add_tags.py      | process_html                | input_html: str                                           | str                 | 添加itemid     |
| post_llm.py      | get_llm_response            | api_key: str, url: str, html_id_str: str, model_name: str | str                 | 模型打标       |
| generate_rule.py | restore_html_trim_ends_only | processed_html: str, llm_response: Dict\[str, int\]       | Dict\[str, object\] | 生成删除规则   |
| post_mapping.py  | mapping_html_by_rules       | html_str: str, post_delete_node: List\[object\]           | str                 | 推广到所有数据 |
