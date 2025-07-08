## 作用

识别文本中的数学内容，使用基于HuggingFace Transformers的E5ScoreModel模型。该模型能够检测文本中是否包含数学公式、方程式或数学概念，并返回数学内容的分数（0-5范围）以及原始概率分数。模型使用GPU运行，默认使用HuggingFaceTB/finemath-classifier预训练模型。

## 配置文件需要改动的部分

数学检测模型使用transformer模型，对应于下面配置中的math_detector_25m7：

```json
"resources": {
        "common":{
            "cache_path": "~/.llm_web_kit_cache"
        },
        "math_detector_25m7":{
            "download_path": "s3://web-parse-huawei/shared_resource/math/math_detector_25m7.zip",
            "md5": "70404024b808ed47bc06411cc1832f67",
        },
    },
```

## 调用方法

1. 基本使用方法：

```python
from llm_web_kit.model.math_detector import E5ScoreModel

# 初始化模型（自动检测GPU/CPU）
model = E5ScoreModel()

# 单个文本检测
text = "The quadratic formula is x = (-b ± √(b²-4ac)) / 2a"
result = model.predict(text)
print(result)
# 输出结果为：[{'text': 'The quadratic formula is x = (-b ± √(b²-4ac)) / 2a', 'score': 4.2, 'int_score': 4, 'score': 4.2, 'int_score': 4}]
```

2. 批量文本检测：

```python
from llm_web_kit.model.math_detector import E5ScoreModel

# 初始化模型
model = E5ScoreModel()

# 批量检测
texts = [
    "The area of a circle is πr²",
    "Today is a beautiful day for a walk",
    "Solve for x: 2x + 5 = 15",
    "Machine learning is a subset of artificial intelligence"
]

results = model.predict(texts)
for result in results:
    print(f"文本: {result['text'][:30]}...")
    print(f"数学分数: {result['score']:.2f}, 整数分数: {result['int_score']}")
    print("---")
```

3. 自定义配置：

```python
from llm_web_kit.model.math_detector import E5ScoreModel

# 自定义配置
config = {
    'model_name': 'HuggingFaceTB/finemath-classifier',
    'max_tokens': 512,
    'batch_size': 16,
    'device': 'cuda',
    'use_flash_attn': False
}

model = E5ScoreModel(config=config)

# 检测数学内容
math_texts = [
    "∫₀¹ x² dx = 1/3",
    "The derivative of sin(x) is cos(x)",
    "Matrix multiplication: C = AB where C[i,j] = Σₖ A[i,k] * B[k,j]"
]

for text in math_texts:
    result = model.predict(text)
    print(f"数学内容: {text}")
    print(f"检测结果: 分数={result[0]['score']:.2f}, 等级={result[0]['int_score']}")
```

4. 通过模型工厂使用：

```python
from llm_web_kit.model.model_impl import ModelFactory, ModelType, DeviceType
from llm_web_kit.model.model_interface import MathRequest

# 创建数学检测器
predictor = ModelFactory.create_predictor(ModelType.MATH, 'en', DeviceType.GPU)

# 创建请求，多语言模型language可初始化为''或[]
requests = [
    MathRequest(
        content='Calculate the limit: lim(x→0) sin(x)/x = 1',
        language='en',
    ),
    MathRequest(
        content='This is just regular text without math',
        language='en',
    ),
]

# 批量预测
batch_size = 2
for i in range(0, len(requests), batch_size):
    results = predictor.predict_batch(requests[i:i+batch_size])
    print(f"batch {i}:", results)
```

## 运行时间

使用NVIDIA A100测试数学检测的GPU模型，测试集共约1.1亿条数据，下面统计模型的处理速度。

### GPU性能（使用CUDA）

在slurm app使用file based模型，使用118505481条html数据进行测试，html字段的cbytes为223.4GB，设置batch_size=1000，8卡A100，处理时间为3小时25分，平均每卡QPS为1198.

## 性能说明

math_detector_25m7模型：

Loss: 0.4478
Precision: 0.8771
Recall: 0.8769
F1 Macro: 0.8770
Accuracy: 0.8770

## 技术细节

### 模型架构

- 基础模型：HuggingFaceTB/finemath-classifier
- 框架：HuggingFace Transformers
- 输入：原始文本（最大512 tokens）
- 输出：数学内容分数（浮点数）和整数分数（0-5范围）

### 设备支持

模型支持自动设备检测：

- **GPU模式**：使用CUDA加速，支持float16精度
- **批处理**：支持批量处理以提高效率

### 输出格式

每个预测结果包含以下字段：

- `text`: 输入的原始文本
- `score`: 原始数学内容分数（浮点数）
- `int_score`: 整数化分数（0-5范围，四舍五入）
- 兼容性字段：同时包含带前缀/后缀的输出键

### 自动下载机制

模型支持自动下载和缓存：

- 优先使用本地配置的模型路径
- 如果本地不存在，自动从S3下载并解压
- 下载失败时回退到HuggingFace Hub直接加载
- 支持MD5校验确保文件完整性
