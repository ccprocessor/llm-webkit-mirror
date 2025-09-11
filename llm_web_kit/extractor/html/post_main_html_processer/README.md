# main html后处理

## 流程方案

![img.png](assets/img.png)

## 执行步骤

### choose_html.py 选出代表html

```
func: select_typical_htmls

输入参数：
    html_strings: List[dict]
        [
            {"html": "html字符串","filename": "数据来源路径"}
        ]
    select_n: int (选出代表html的数量，default: 3)

输出参数：
    List[dict]
        [
            {"html": "html字符串","filename": "数据来源路径"}
        ]
```

### post_llm.py 模型识别生成规则

```
func: get_llm_response

输入参数：
    html_strings: List[dict]
        ["html0", "html1", "html2"]
    api_key: str (openai api key)
    url: str (openai api url)
    model_name: str (openai model name)

输出参数：
    str
        [
            {
              "xpath": "//div[@class='et_pb_social_media_follow']",
              "parent_tag": "div",
              "parent_attributes": {
                "class": "et_pb_column et_pb_column_2_3 et_pb_column_6 et_pb_css_mix_blend_mode_passthrough et-last-child"
              },
              "reson": "Social media follow links are non-core content, typically used for sharing and external linking."
            },
            {
              "xpath": "//form[@class='et_pb_contact_form clearfix']",
              "parent_tag": "div",
              "parent_attributes": {
                "class": "et_pb_column et_pb_column_2_3 et_pb_column_6 et_pb_css_mix_blend_mode_passthrough et-last-child"
              },
              "reson": "Contact form is a footer widget, often considered as part of the contact section rather than main content."
            }
        ]
```

### post_mapping.py 推广到所有数据

```
func: mapping_html_by_rules

输入参数：
    html_content: str
    xpaths_to_remove: List[dict]
        [
            {
              "xpath": "//div[@class='et_pb_social_media_follow']",
              "parent_tag": "div",
              "parent_attributes": {
                "class": "et_pb_column et_pb_column_2_3 et_pb_column_6 et_pb_css_mix_blend_mode_passthrough et-last-child"
              },
              "reson": "Social media follow links are non-core content, typically used for sharing and external linking."
            },
            {
              "xpath": "//form[@class='et_pb_contact_form clearfix']",
              "parent_tag": "div",
              "parent_attributes": {
                "class": "et_pb_column et_pb_column_2_3 et_pb_column_6 et_pb_css_mix_blend_mode_passthrough et-last-child"
              },
              "reson": "Contact form is a footer widget, often considered as part of the contact section rather than main content."
            }
        ]

输出参数：
    tuple[str, bool]
        (
            html_content,  # html字符串
            is_success  # 推广是否成功
        )
```
