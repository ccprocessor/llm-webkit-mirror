## 作用

负责读取配置文件的统一入口。

## 配置文件的位置和格式如下：

<b>一、位置</b>
首先读取环境变量 LLM_WEB_KIT_CFG_PATH, 如果有（注意如果环境变量有设置，但是文件不存在会报错）并且配置文件存在则读取这个配置文件。
如果环境变量不存在，则默认去用户的HOME目录下寻找名字为llm-web-kit.jsonc的配置文件

<b>二、格式</b>
配置文件的模板：

```json
{
    "s3": {
        "bucket_name1": {
            "ak": "XXXXXXXXXXXXXXXXXXXX",
            "sk": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "endpoint": "http://endpoint1",
            "addressing_style": "path"
        },
        "bucket_name2": {
            "ak": "XXXXXXXXXXXXXXXXXXXX",
            "sk": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "endpoint": "http://endpoint2",
            "addressing_style": "path"
        }
    },
    "resources": {
        "common":{
            "cache_path": "~/.llm_web_kit_cache"
        },
        "lang-id-176": {
            "download_path": "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin",
            "md5": "01810bc59c6a3d2b79c79e6336612f65"
        },
        "political-24m7": {
            "download_path": "XXXXXX",
            "md5": "XXXXX"
        }
    },
    "logger": [
                {
                    "to": "sys.stdout",
                    "log-level": "DEBUG",
                    "log-format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
                },
                {
                    "to": "/tmp/logs/test-{time:YYYY-MM-DD}.log",
                    "rotation": "1 day",
                    "retention": "10 days",
                    "log-level": "INFO",
                    "log-format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
                },
                {
                    "to": "/tmp/logs/error-{time:YYYY-MM-DD}.log",
                    "rotation": "1 day",
                    "retention": "10 days",
                    "log-level": "ERROR",
                    "log-format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
                }
            ],
  "magic-html-custom-rule": {
      "test.custom.com": {
                "clean": [
                  "//script",
                  "//style",
                  "//*[@id=\"post-219\"]/div[1]/div[2]/div"
                ],
                "title": {
                  "mode": "xpath",
                  "value": "//*[@id=\"post-219\"]/div[1]/div[1]/h1/text()"
                },
                "content": {
                  "mode": "xpath",
                  "value": "//*[@id=\"post-219\"]/div[1]/div[2]"
                }
          }
    }
}


```
