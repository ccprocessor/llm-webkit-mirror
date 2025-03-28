## 作用

识别给定语句的语言种类，调用接口为update_language_by_str，有两个参数：

is_218e为True时使用lid218e模型，在多个小语种中有更好的表现，除个别容易使模型混淆的情况外，会返回正常的language_details字段，若该参数为False，则language_details字段为空，默认值为True

is_cn_specific为True时，会对文本中的中文文本进行细分，分为zho-Hans(简体中文)或zho-Hant(繁体中文)，结果在language_details字段中，默认值为False

## 配置文件需要改动的部分

huggingface版本：

```json
"resources": {
        "common":{
            "cache_path": "~/.llm_web_kit_cache"
        },
        "lang-id-218": {
            "download_path": "https://huggingface.co/facebook/fasttext-language-identification/resolve/main/model.bin?download=true",
            "sha256": "8ded5749a2ad79ae9ab7c9190c7c8b97ff20d54ad8b9527ffa50107238fc7f6a"
        },
        "lang-id-176": {
            "download_path": "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin",
            "md5": "01810bc59c6a3d2b79c79e6336612f65"
        }
    },
```

s3版本：

```json
"resources": {
        "common":{
            "cache_path": "~/.llm_web_kit_cache"
        },
        "lang-id-218": {
            "download_path": "s3://web-parse-huawei/shared_resource/language/lid218e.bin",
            "sha256": "8ded5749a2ad79ae9ab7c9190c7c8b97ff20d54ad8b9527ffa50107238fc7f6a"
        },
        "lang-id-176": {
            "download_path": "s3://web-parse-huawei/shared_resource/language/lid176.bin",
            "md5": "01810bc59c6a3d2b79c79e6336612f65"
        }
    },
```

## 调用方法

```python
from llm_web_kit.model.lang_id import *
text = 'hello world, this is a test. the language is english'
print(update_language_by_str(text))
{'language': 'en','language_details': ''}

text = 'Это русский текст.'
print(update_language_by_str(text))
{'language': 'ru', 'language_details': 'rus_Cyrl'}

text = 'Это русский текст.'
print(update_language_by_str(text, use_218e=False))
{'language': 'ru', 'language_details': ''}

text = '这是一段简体中文文本'
print(update_language_by_str(text))
{'language': 'zh', 'language_details': ''}

text = '这是一段简体中文文本'
print(update_language_by_str(text, is_cn_specific=True))
{'language': 'zh', 'language_details': 'zho_Hans'}
```

## 运行时间

使用单cpu进行推理

### 默认参数，使用lid176和lid218e模型（俄文文本）

共有 2099 条数据

总token数: 379375

平均token数: 180.74

载入数据时间: 0.0402 秒

语言识别时间: 5.2559 秒

总时间: 5.2962 秒

处理速度: 399.36 条/秒

### 仅使用lid176模型（中文文本）

共有 600 条数据

总token数: 8560

平均token数: 14.27

载入数据时间: 0.0022 秒

语言识别时间: 0.4747 秒

总时间: 0.4769 秒

处理速度: 1264.09 条/秒

### 使用lid176+判断简体中文和繁体中文（中文文本）

共有 600 条数据

总token数: 8560

平均token数: 14.27

载入数据时间: 0.0022 秒

语言识别时间: 1.3516 秒

总时间: 1.3538 秒

处理速度: 443.91 条/秒
