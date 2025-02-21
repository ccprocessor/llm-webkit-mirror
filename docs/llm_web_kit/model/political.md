## 作用

识别中文或英文文本中的涉政内容，返回值介于0~1.01之间，其中0代表涉政内容，1.01代表非涉政内容。

## 配置文件需要改动的部分

```json
"resources": {
        "common":{
            "cache_path": "~/.llm_web_kit_cache"
        },
        "political-24m7":{
            "download_path": "s3://web-parse-huawei/shared_resource/political/24m7.zip",
            "md5": "97eabb56268a3af3f68e8a96a50d5f80",
        },
    },
```

## 调用方法

```python
from llm_web_kit.model.policical import *
text = {
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
print(safety_filter_cpu(text, "en"))
#{'safety_prob': 1.0000100135803223}
```

## 运行时间

总共有 77862 条数据
总字符数: 135618737
平均每条数据的字符数: 1741.7833
平均每条数据处理时间: 0.00245 秒
总处理时间: 190.5865 秒
每秒可处理: 408.1633条数据
