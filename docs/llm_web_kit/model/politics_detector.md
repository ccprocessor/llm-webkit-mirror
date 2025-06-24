## 作用

识别中文或英文文本中的涉政内容，目前包含了新旧两类接口，25m3_cpu模型接口接收单条数据，并返回该数据的涉政分数，分数接近1代表不涉政，分数接近0则代表涉政。目前25m3_cpu模型接口仅支持CPU模型。

25m3模型接口检测结果以ModelResponse类返回，该类包含is_remained和details两个字段，其中is_remained代表数据是否需要保留，details则是一个包含涉政分数等详细信息的字典。25m3模型接口支持GPU模型。

## 配置文件需要改动的部分

目前包含使用cpu的fasttext模型和使用gpu的gte模型，fasttext模型对应于下面配置中的political-24m7，gte模型则对应于下面配置中的political-25m3：

```json
"resources": {
        "common":{
            "cache_path": "~/.llm_web_kit_cache"
        },
        "political-25m3":{
            "download_path": "s3://web-parse-huawei/shared_resource/political/25m3.zip",
            "md5": "d0d14a561f987763d654165b536b5858",
        },
        "political-25m3_cpu":{
            "download_path": "s3://web-parse-huawei/shared_resource/political/25m3_cpu.zip",
            "md5": "926359a393de6a36c1b4be403711767f",
        },
    },
```

## 调用方法

1. 25m3_cpu模型接口调用方法如下：

```python
from llm_web_kit.model.politics_detector import *
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
print(political_filter_cpu(text, "en"))
# 输出结果为：{'political_prob': 1.0000100135803223}
```

2. 25m3模型接口调用方法如下：

```python
from llm_web_kit.model.model_impl import ModelFactory, ModelType, DeviceType
from llm_web_kit.model.model_interface import PoliticalRequest

predictor = ModelFactory.create_predictor(ModelType.POLITICAL, 'en', DeviceType.GPU)

requests = [
    PoliticalRequest(
        content='China is a beautiful country',
        language='en',
    ),
    PoliticalRequest(
        content='China is a bad country',
        language='en',
    ),
    # ...
]

batch_size = 1

for i in range(0, len(requests), batch_size):
    results = predictor.predict_batch(requests[i:i+batch_size])
    print(f"batch {i}:", results)
# 输出结果如下：
# batch 0: [PoliticalResponse(is_remained=True, details={'political_prob': 0.996094})]
# batch 1: [PoliticalResponse(is_remained=False, details={'political_prob': 0.020493})]
```

## 运行时间

1. 25m3_cpu模型接口（political_filter_cpu）

   使用型号为`AMD EPYC 7742`的cpu单核进行测试，测试集总共有 77861 条数据（均是中英文的数据），下面只统计了political_filter_cpu接口本身的耗时，排除了数据读取的时间。

   总字符数: 135617056

   平均每条数据的字符数: 1741.7842

   平均每条数据处理时间: 0.002402 秒

   总处理时间: 190.5865 秒

   每秒可处理: 416.3049条数据

2. 25m3模型接口（predictor.predict_batch）

   使用单卡NVIDIA A100测试涉政的GPU模型，测试集共有39111条数据，下面统计了不同batch_size下，predictor.predict_batch接口的速度，该接口内部包括tokenize和模型推理操作。

   2.1 使用xformers：

   注意：若要使用xformers，需要安装与torch版本对应的xformers包。当使用xformers时，模型支持的最大batch_size和qps会和输入数据的长度（即tokens数）有关。如果数据中短文本居多，则最大batch_size可以设置得更大，且qps也会比正常情况更高；如果数据中长文本居多，则最大batch_size需要减小，且qps也会比正常情况更低。经测试，当数据中的每一条文本都超过8192 tokens时，最大batch_size可以设置为256。下表的qps是在上述39111条数据的测试集上测试得到，如果实际数据的tokens长度与上述测试集显著不同，那么qps也会有较大差异。

   | batch_size | qps                |
   | ---------- | ------------------ |
   | 8          | 314.84969058400907 |
   | 16         | 320.8465052538487  |
   | 32         | 321.95824353893886 |
   | 64         | 305.97022201928917 |
   | 128        | 284.8440728889309  |
   | 256        | 266.4453421333349  |
   | 512        | 248.19387912927127 |
   | 1024       | 238.03487475066987 |
   | 1560       | 235.5055696206246  |
   | 2048       | cuda out of memory |

   2.2 不使用xformers

   | batch_size | qps                |
   | ---------- | ------------------ |
   | 8          | 101.8941881724654  |
   | 16         | 73.09307498984671  |
   | 32         | 53.73927136389652  |
   | 64         | 40.21807875617244  |
   | 128        | 31.580092769179686 |
   | 256        | 24.26296225431703  |
   | 512        | cuda out of memory |

## 性能说明

25m3_cpu模型（threshold=0.5）：

测试集路径：s3://xyz-process-ylk2/xyz-users/huyucheng1/political_data_202502/test/

| 指标          | 新模型值             | 旧模型值             |
| ------------- | -------------------- | -------------------- |
| **F1**        | 0.9089603520041284   | 0.8831507760632497   |
| **Accuracy**  | 0.8624864742896118   | 0.8013861609546715   |
| **Precision** | 0.9041776426882809   | 0.7913184992146802   |
| **Recall**    | 0.9137939273134369   | 0.999095513748191    |
| **TN**        | 68641                | 19820                |
| **FP**        | 28373                | 77194                |
| **FN**        | 25257                | 265                  |
| **TP**        | 267727               | 292719               |
| **Prec_Pos**  | 0.9041776426882809   | 0.7913184992146802   |
| **Recl_Pos**  | 0.9137939273134369   | 0.999095513748191    |
| **F1_Pos**    | 0.9089603520041284   | 0.8831507760632497   |
| **Prec_Neg**  | 0.7310166350720995   | 0.986806074184715    |
| **Recl_Neg**  | 0.7075370565073082   | 0.204300410250067    |
| **F1_Neg**    | 0.719085232986926    | 0.3385169813576546   |
| **qps**       | 1493.477337807 条/秒 | 1674.157845704 条/秒 |

注：上述指标均是在集群中得出，单核运行时间请参考运行时间第一小节
