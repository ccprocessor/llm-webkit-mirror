## 作用

识别文本中的代码内容，使用基于fasttext的分类模型结合jieba分词预处理。该模型能够检测文本中是否包含编程代码，并返回代码存在的概率分数。分数接近1代表包含代码，分数接近0则代表不包含代码。目前仅支持CPU模型。

## 配置文件需要改动的部分

代码检测模型使用fasttext模型，对应于下面配置中的code_detect_v4_0409：

```json
"resources": {
        "common":{
            "cache_path": "~/.llm_web_kit_cache"
        },
        "code_detect_v4_0409":{
            "download_path": "s3://web-parse-huawei/shared_resource/code/code_detect_v4_0409.bin",
            "md5": "2257ad8fc23ef574626b428b6e99df48",
        },
    },
```

## 调用方法

1. 直接使用CodeClassification类：

```python
from llm_web_kit.model.code_detector import CodeClassification

# 初始化模型
classifier = CodeClassification()

# 预测代码内容
text = "import pandas as pd\ndf = pd.read_csv('data.csv')\nprint(df.head())"
result = classifier.predict(text)
print(result)
# 输出结果为：{'has_code_prob_0409': 0.95}
```

2. 使用单例模式接口：

```python
from llm_web_kit.model.code_detector import get_singleton_code_detect, update_code_prob_by_str

# 使用单例模式获取模型实例
classifier = get_singleton_code_detect()
result = classifier.predict("def hello_world():\n    print('Hello, World!')")
print(result)

# 或者直接使用便捷函数
result = update_code_prob_by_str("SELECT * FROM users WHERE age > 18;")
print(result)
# 输出结果为：{'has_code_prob_0409': 0.87}
```

3. 测试不同类型的文本：

```python
from llm_web_kit.model.code_detector import update_code_prob_by_str

# 测试代码文本
code_samples = [
    "import numpy as np\narray = np.zeros((10, 10))",
    "function calculateSum(a, b) { return a + b; }",
    "SELECT name, age FROM users ORDER BY age DESC;",
    "git clone https://github.com/user/repo.git"
]

# 测试非代码文本
non_code_samples = [
    "这是一段普通的中文文本，没有任何代码内容。",
    "The quick brown fox jumps over the lazy dog.",
    "今天天气很好，适合出去散步。"
]

print("代码文本检测结果：")
for text in code_samples:
    result = update_code_prob_by_str(text)
    print(f"文本: {text[:30]}... -> 代码概率: {result['has_code_prob_0409']:.3f}")

print("\n非代码文本检测结果：")
for text in non_code_samples:
    result = update_code_prob_by_str(text)
    print(f"文本: {text[:30]}... -> 代码概率: {result['has_code_prob_0409']:.3f}")
```

## 运行时间

使用服务器cpu单线程进行测试，CPU max MHz 2600，测试集总共有1万条数据，下面统计了代码检测接口本身的耗时，排除了数据读取/写入的时间。进行3次测试，处理时间分别为：40.3019秒、39.8865秒、40.0666秒。

样本数: 10000

Token数: 11762484 (平均 1176.2)

QPS: 249.47 条/秒

延迟: 4.01 毫秒/条

检测: 4798 代码, 5202 非代码

总处理时间: 约40秒

## 性能说明

code_detect_v4_0409模型

## 代码检测器性能评估结果

### 数据分布

| 指标         | 类别 0 | 类别 1 |
| ------------ | ------ | ------ |
| GT标签数量   | 221    | 165    |
| 预测标签数量 | 249    | 137    |

### 性能指标

| 指标               | 类别 0 | 类别 1 |
| ------------------ | ------ | ------ |
| 精确率 (Precision) | 0.888  | 1.000  |
| 召回率 (Recall)    | 1.000  | 0.830  |

### 整体性能

| 指标  | 数值   |
| ----- | ------ |
| AUC值 | 0.9910 |

### 不同阈值下的性能表现

| 阈值 | TPR  | FPR  |
| ---- | ---- | ---- |
| 0.10 | 0.98 | 0.06 |
| 0.20 | 0.92 | 0.05 |
| 0.30 | 0.88 | 0.02 |
| 0.40 | 0.87 | 0.00 |
| 0.50 | 0.83 | 0.00 |

## 技术细节

### 文本预处理

模型使用jieba分词对输入文本进行预处理：

1. 使用jieba.lcut()进行分词
2. 过滤停用词（包括空格、换行符等）
3. 限制最大词数为20480个词
4. 移除标点符号和特殊字符
5. 转换为小写并去除多余空格

### 模型架构

- 基础模型：FastText
- 版本：v4_0409
- 输入：预处理后的分词文本
- 输出：代码存在概率（0-1之间的浮点数）
