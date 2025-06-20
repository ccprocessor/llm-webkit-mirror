## 作用

返回基于规则的综合安全检测结果。具体检查内容包括域名是否命中黑名单、来源是否安全、内容是否命中敏感词。

## 配置文件需要改动的部分

```json
"resources": {
        "common":{
            "cache_path": "~/.llm_web_kit_cache"
        },
        "unsafe_words":{
            "download_path": "s3://web-parse-huawei/shared_resource/unsafe_words/unsafe_words_porn_politics.jsonl",
            "md5": "ef51faf114353d987ec97b211a8d2b06",
        },
        "xyz_internal_unsafe_words":{
            "download_path": "s3://web-parse-huawei/shared_resource/political/xyz_internal_unsafe_words.jsonl",
            "md5": "05024905f03a420fc63ecae2f35b6e24",
        },
        "domain_blacklist" : {
            "download_path": "s3://web-parse-huawei/shared_resource/safety/domain_blacklist.json",
            "md5": "8882d7ba2bd80591f4025adec7189f09",
        },
        "data_source_safe_type" : {
            "download_path": "s3://web-parse-huawei/shared_resource/safety/data_source_safe_type.csv",
            "md5": "e9255786a05bf793a489926f7415c775",
        },
    },
```

## 用法示例

调用process方法即可。

```
from llm_web_kit.model.rule_based_safety_module import RuleBasedSafetyModule
m=RuleBasedSafetyModule(True)
m.process("your content",
        "en",
        "",
        "article",
        "www.unknown.com",
        "zh-weixin")

```

返回结果示例：

```
{'safety_remained': True,
 'safety_infos': {'domain_level': '', 'hit_unsafe_words': False}}
```

### 敏感词检测模块用法示例

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

## 速度

### 整体速度：

- 资源下载及加载：23s
- 命中计算：xyz和zh-en的qps分别为10230、2987

具体各模块速度如下：

### 域名检测模块速度：

- 资源下载：2s
- 资源加载：18s
- 资源下载及加载：20.3s
- 命中计算：在域名列表已加载的情况下，qps为187666

### 来源检测模块速度：

- 资源下载及加载：0.16s
- 命中计算：在数据源安全类型表已加载的情况下，qps为992896

### 敏感词模块速度：

- 词表下载：auto_download，下载zh-en和xyz两个词表耗时分别为0.09s，0.02s
- 词表加载（不包括下载时间）：get_ac，加载两个词表耗时分别为3.0s，0.7s
- 词表加载（包括下载时间）：get_ac，加载两个词表耗时分别为3.3s , 0.72s
- 词表命中计算：在词表已加载的情况下，qps分别为约10525、3147
