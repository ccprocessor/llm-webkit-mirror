## 作用

根据敏感词表，返回数据包含的敏感词或是否安全

## 配置文件需要改动的部分

```json
"resources": {
        "unsafe_words": {
            "download_path": "s3://web-parse-huawei/shared_resource/unsafe_words/unsafe_words_porn_politics.jsonl",
            "md5": "ef51faf114353d987ec97b211a8d2b06"
        }
    },
```

## 调用方法

```python
from llm_web_kit.model.unsafe_words_detector import *

checker = UnsafeWordChecker(language="zh-en")

content = "64式销售QQ"
unsafe_words = checker.check_unsafe_words(
    content_str=content,
)
print(unsafe_words)
[{'word': '64式', 'type': '违禁品', 'level': 'L3', 'language': 'zh', 'count': 1.0}, {'word': '64式销售', 'type': '违禁品', 'level': 'L3', 'language': 'zh', 'count': 1.0}, {'word': '销售', 'type': '广告营销', 'level': 'L3', 'language': 'zh', 'count': 1.0}, {'word': '64式销售qq', 'type': '违禁品', 'level': 'L1', 'language': 'zh', 'count': 1.0}]

checker = UnsafeWordsFilter()
content = "64式销售QQ"
#from_safe_source:是否来自安全来源。如果是，直接返回安全。
#from_domestic_source: 是否来自国内来源。如果是，仅检查 L1 级别的不安全词；否则检查 L1 和 L2 级别。
result = checker.filter(
    content,
    'zh',
    from_safe_source = False,
    from_domestic_source = True,
)
```
