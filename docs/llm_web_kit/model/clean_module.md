## 作用

**注意!!** 本模块是质量清洗模块的顶层接口

对输入数据进行质量清洗。目前版本只包含 `llm_web_kit/model/quality_model.py` 模块。
注意：需要语言模型先决定输入数据的语言，语言模型见 `docs/llm_web_kit/model/lang_id.md`。

## 配置文件需要改动的部分

```json
"resources": {
        "common":{
            "cache_path": "~/.llm_web_kit_cache"
        },
        "zh_en_article":{
            "download_path": "s3://web-parse-huawei/shared_resource/quality/zh_en/zh_en_article.zip",
            "md5": "ebc8be83b86e0d1ee2c9b797ad8f6130",
        },
        "zh_en_long_article":{
            "download_path": "s3://web-parse-huawei/shared_resource/quality/zh_en/zh_en_long_article.zip",
            "md5": "4586a9536ee7e731dac87361755e8026",
        },
    },
```

## 调用方法

```python
from llm_web_kit.model.clean_module import CleanModule, ContentStyle
from llm_web_kit.model.lang_id import update_language_by_str

content_str = "Your content string here."
# content_style = "article", "book", "paper" ...
content_style = ContentStyle.ARTICLE

language = "en"
language_details = "eng_Latn"
# 注意：如果需要自动决定语言，可以使用下面的方法
# language, language_details = update_language_by_str(content_str)


clean_module = CleanModule(prod = True)
result = clean_module.process(
             content_str=content_str,
             language=language,
             language_details=language_details,
             content_style=content_style,
         )

assert isinstance(result, dict)

print(result["clean_remained"]) # True or False
print(result["clean_infos"]) # An info dict like {'quality_prob': 0.0}

```

## 参数说明

class CleanModule

- prod: bool
  - 是否使用生产环境的模型。默认为True。

def process

- content_str: str
  - 输入的文本内容。
- language: str
  - 输入的文本内容的语言。
  - 例如：en, zh
- language_details: str
  - 输入的文本内容的语言细节。
  - 例如：eng_Latn, zho_Hans
- content_style: ContentStyle
  - 输入的文本内容的风格。
  - ContentStyle.ARTICLE, ContentStyle.BOOK, ContentStyle.PAPER
