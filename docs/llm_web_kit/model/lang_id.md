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

## 性能说明

测试集路径：https://huggingface.co/facebook/fasttext-language-identification

| 级联方案  |          | lid176   |          | lid218e   |          |
| --------- | -------- | -------- | -------- | --------- | -------- |
| 真实语言  | 错误次数 | 真实语言 | 错误次数 | 真实语言  | 错误次数 |
| bos       | 1079     | zho_trad | 2009     | bos       | 1079     |
| kam       | 767      | ful      | 2009     | kam       | 765      |
| zho_trad  | 18       | lug      | 2009     | zho_trad  | 623      |
| hrv       | 197      | hau      | 2009     | zho_simpl | 229      |
| nya       | 165      | ibo      | 2009     | hrv       | 197      |
| kea       | 145      | kea      | 2009     | nya       | 161      |
| msa       | 145      | kam      | 2009     | kea       | 145      |
| ful       | 67       | lin      | 2009     | msa       | 145      |
| xho       | 51       | luo      | 2009     | ful       | 56       |
| umb       | 46       | mri      | 2009     | umb       | 46       |
| zul       | 38       | nso      | 2009     | jpn       | 46       |
| fas       | 38       | nya      | 2009     | fas       | 38       |
| ind       | 37       | orm      | 2009     | ind       | 37       |
| mri       | 27       | sna      | 2009     | xho       | 32       |
| wol       | 22       | umb      | 2009     | zul       | 16       |
| ast       | 16       | wol      | 2009     | ast       | 16       |
| dan       | 13       | xho      | 2009     | dan       | 13       |
| nob       | 13       | zul      | 2009     | wol       | 13       |
| nso       | 12       | bos      | 1879     | nob       | 13       |
| luo       | 11       | ast      | 1373     | nso       | 11       |
| lug       | 11       | som      | 1184     | luo       | 8        |
| jav       | 9        | msa      | 1131     | lug       | 7        |
| sna       | 9        | yor      | 943      | pus       | 7        |
| ibo       | 8        | oci      | 753      | glg       | 6        |
| afr       | 7        | hrv      | 609      | jav       | 6        |
| pus       | 7        | jav      | 590      | mri       | 5        |
| glg       | 6        | afr      | 574      | hin       | 4        |
| som       | 4        | glg      | 294      | swe       | 3        |
| swh       | 4        | uzb      | 188      | yor       | 3        |
| hin       | 4        | ltz      | 151      | lin       | 3        |
| yor       | 4        | ceb      | 144      | lao       | 2        |
| lin       | 4        | nob      | 137      | oci       | 2        |
| ceb       | 3        | swh      | 118      | som       | 2        |
| swe       | 3        | mlt      | 109      | ceb       | 2        |
| lao       | 2        | dan      | 90       | khm       | 2        |
| oci       | 2        | slv      | 56       | slv       | 1        |
| uzb       | 2        | ind      | 48       | uzb       | 1        |
| orm       | 2        | slk      | 41       | npi       | 1        |
| nld       | 2        | pus      | 37       | tgl       | 1        |
| hau       | 2        | gle      | 26       | bul       | 1        |
| slv       | 1        | npi      | 18       | fra       | 1        |
| zho_simpl | 1        | azj      | 17       | hau       | 1        |
| npi       | 1        | asm      | 14       | ita       | 1        |
| eng       | 1        | tgk      | 13       | ltz       | 1        |
| tgl       | 1        | isl      | 13       | kaz       | 1        |
| est       | 1        | est      | 12       | por       | 1        |
| bul       | 1        | snd      | 12       | afr       | 1        |
| fra       | 1        | cym      | 11       | spa       | 1        |
| ita       | 1        | cat      | 11       |           |          |
| khm       | 1        | srp      | 11       |           |          |
| ltz       | 1        | kir      | 10       |           |          |
| kaz       | 1        | nld      | 5        |           |          |
| por       | 1        | por      | 5        |           |          |
| spa       | 1        | swe      | 4        |           |          |
|           |          | mkd      | 4        |           |          |
|           |          | lav      | 4        |           |          |
|           |          | urd      | 3        |           |          |
|           |          | tgl      | 3        |           |          |
|           |          | kaz      | 2        |           |          |
|           |          | ron      | 2        |           |          |
|           |          | ita      | 2        |           |          |
|           |          | bel      | 2        |           |          |
|           |          | bul      | 2        |           |          |
|           |          | lit      | 2        |           |          |
|           |          | lao      | 1        |           |          |
|           |          | ckb      | 1        |           |          |
