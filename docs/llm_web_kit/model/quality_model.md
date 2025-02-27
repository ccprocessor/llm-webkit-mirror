## 作用

对输入数据进行质量清洗。

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
from llm_web_kit.model.quality_model import *
data = {
    "track_id": "1e07f144-b290-4bcc-b6eb-37fc9a7f15ca",
    "content_list": [
        [
            {
                "type": "paragraph",
                "raw_content": "<div><div class=\"abstract-content selected\" id=\"eng-abstract\"><p><strong class=\"sub-title\">\n          Objective:\n        </strong>\n      \n      This study analyzed the cost-effectiveness of delivering alcohol screening, brief intervention, and referral to treatment (SBIRT) in emergency departments (ED) when compared to outpatient medical settings.\n    </p></div></div>",
                "content": [
                    {
                        "c": "Objective: This study analyzed the cost-effectiveness of delivering alcohol screening, brief intervention, and referral to treatment (SBIRT) in emergency departments (ED) when compared to outpatient medical settings.",
                        "t": "text"
                    }
                ]
            },
            {
                "type": "paragraph",
                "raw_content": "<div><div class=\"abstract-content selected\" id=\"eng-abstract\"><p><strong class=\"sub-title\">\n          Methods:\n        </strong>\n      \n      A probabilistic decision analytic tree categorized patients into health states. Utility weights and social costs were assigned to each health state. Health outcome measures were the proportion of patients not drinking above threshold levels at follow-up, the proportion of patients transitioning from above threshold levels at baseline to abstinent or below threshold levels at follow-up, and the quality-adjusted life years (QALYs) gained. Expected costs under a provider perspective were the marginal costs of SBIRT, and under a societal perspective were the sum of SBIRT cost per patient and the change in social costs. Incremental cost-effectiveness ratios were computed.\n    </p></div></div>",
                "content": [
                    {
                        "c": "Methods: A probabilistic decision analytic tree categorized patients into health states. Utility weights and social costs were assigned to each health state. Health outcome measures were the proportion of patients not drinking above threshold levels at follow-up, the proportion of patients transitioning from above threshold levels at baseline to abstinent or below threshold levels at follow-up, and the quality-adjusted life years (QALYs) gained. Expected costs under a provider perspective were the marginal costs of SBIRT, and under a societal perspective were the sum of SBIRT cost per patient and the change in social costs. Incremental cost-effectiveness ratios were computed.",
                        "t": "text"
                    }
                ]
            },
            {
                "type": "paragraph",
                "raw_content": "<div><div class=\"abstract-content selected\" id=\"eng-abstract\"><p><strong class=\"sub-title\">\n          Results:\n        </strong>\n      \n      When considering provider costs only, compared to outpatient, SBIRT in ED cost $8.63 less, generated 0.005 more QALYs per patient, and resulted in 13.8% more patients drinking below threshold levels. Sensitivity analyses in which patients were assumed to receive a fixed number of treatment sessions that met clinical sites' guidelines made SBIRT more expensive in ED than outpatient; the ED remained more effective. In this sensitivity analysis, the ED was the most cost-effective setting if decision makers were willing to pay more than $1500 per QALY gained.\n    </p></div></div>",
                "content": [
                    {
                        "c": "Results: When considering provider costs only, compared to outpatient, SBIRT in ED cost $8.63 less, generated 0.005 more QALYs per patient, and resulted in 13.8% more patients drinking below threshold levels. Sensitivity analyses in which patients were assumed to receive a fixed number of treatment sessions that met clinical sites' guidelines made SBIRT more expensive in ED than outpatient; the ED remained more effective. In this sensitivity analysis, the ED was the most cost-effective setting if decision makers were willing to pay more than $1500 per QALY gained.",
                        "t": "text"
                    }
                ]
            },
            {
                "type": "paragraph",
                "raw_content": "<div><div class=\"abstract-content selected\" id=\"eng-abstract\"><p><strong class=\"sub-title\">\n          Conclusions:\n        </strong>\n      \n      Alcohol SBIRT generates costs savings and improves health in both ED and outpatient settings. EDs provide better effectiveness at a lower cost and greater social cost reductions than outpatient.\n    </p></div></div>",
                "content": [
                    {
                        "c": "Conclusions: Alcohol SBIRT generates costs savings and improves health in both ED and outpatient settings. EDs provide better effectiveness at a lower cost and greater social cost reductions than outpatient.",
                        "t": "text"
                    }
                ]
            }
        ]
    ]
}
# 支持article, paper, book三种文体，其中article使用的是上述配置文件中的`zh_en_article`模型，paper和book使用的是上述配置文件中的`zh_en_long_article`模型。
# `zh_en_long_article`模型适用于长文本，并支持提取文本中公式的特征，适用于清洗带公式的文本。
print(quality_filter(data, "en", "article"))
# {'quality_prob': 0.8930529675838833}
print(quality_filter(data, "en", "paper"))
# {'quality_prob': 0.9265140423831497}
print(quality_filter(data, "en", "book"))
# {'quality_prob': 0.9265140423831497}
```

## 运行时间

在s集群的10.140.24.131机器上，用cpu单核跑，测试样本位于s3://xyz-llm-users/xyz-users/minrui/junk_information_filter/second_largest_cluster_extract/1/part-67adb46f3b43-000053.jsonl

总共有 77856 条数据（排除第一条数据、非中英文的数据和被启发式规则提前拒绝的数据），下面只统计了`quality_filter`接口本身的耗时，排除了数据读取的时间。

总字符数: 135616946

平均每条数据的字符数: 1741.8946

**`zh_en_article`模型:**

平均每条数据处理时间: 0.005748 秒

总处理时间: 447.5430 秒

每秒可处理: 173.9632条数据

**`zh_en_long_article`模型：**

平均每条数据处理时间: 0.005473 秒

总处理时间: 426.1312 秒

每秒可处理: 182.7043条数据
