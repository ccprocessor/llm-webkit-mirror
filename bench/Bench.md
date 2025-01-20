# 概要

`bench`目录是用于评估不同网页抽取仓库的抽取效果，比如`llm-webkit-mirror`，`unstructured`，`magic_html`等。原始网页在`bench/html`目录下，按数学公式(`ccmath`)，代码图片(`cccode`)，表格(`cctable`)等分类。抽取结果默认保存在`bench/output`目录下。

# 使用方法

```
python eval.py
```

# 评估指标
