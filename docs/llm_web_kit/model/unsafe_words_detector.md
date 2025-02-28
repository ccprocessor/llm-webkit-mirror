## 作用

匹配敏感词并返回当前场景下的命中情况。

## 配置文件需要改动的部分

```json
"resources": {
        "common":{
            "cache_path": "~/.llm_web_kit_cache"
        },
        "unsafe_words":{
            "download_path": "s3://web-parse-huawei/shared_resource/political/unsafe_words.jsonl",
            "md5": "e81dd1050a79f68b9d9b3f66baadde66",
        },
        "xyz_internal_unsafe_words":{
            "download_path": "s3://web-parse-huawei/shared_resource/political/xyz_internal_unsafe_words.jsonl",
            "md5": "05024905f03a420fc63ecae2f35b6e24",
        },
    },
```

## 用法

入口函数有2个：

- unsafe_words_filter：返回最严重命中词级别。
- unsafe_words_filter_overall: 返回是否命中严重敏感词。

## 速度

- 词表下载：auto_download，下载zh-en和xyz两个词表耗时分别为0.09s，0.02s
- 词表加载（不包括下载时间）：get_ac，加载两个词表耗时分别为3.0s，0.7s
- 词表加载（包括下载时间）：get_ac，加载两个词表耗时分别为3.3s , 0.72s
- 词表命中计算：在词表已加载的情况下，qps分别为约10525、3147
