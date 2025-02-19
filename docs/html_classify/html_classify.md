# HTML分类

将简化后的html分类article, forum, other三个类别。

## 文件格式

```
--llm_web_kit/
	--model/
		--html_layout_cls.py  # 自动下载模型并解压，调用model.py
		--html_classify/
			-model.py		 # markuplm的inference代码实现
```

## 数据格式

简化后的html，为batch格式。

样例：

```
[
"""<html><body><img class=\"safum-vpn-status\" id=\"ehjolcpljogfgggnkddgefpecllepcba-img\" src=\"chrome-extension:\/\/ehjolcpljogfgggnkddgefpecllepcba\/web_accessible_resources\/status_on.png\" alt=\"status\"><article class=\"event-content athanasius noskim\"><div class...""",

"""<html><div class=\"antialiased|jsx-2324231005 duet--app\"><span>Skip to main content<\/span><span class=\"duet--navigation--navigation|absolute h-[64px] w-full overflow-x-hidden md:h-[150px]|relative h-[64px] w-full max-w-container-lg md:left-1\/2 md:h-[150px] md:-translate-x-1\/2\">The Verge homepage<\/span><div class=...""",
]
```

输出：

```
[
{"pred_prob": "0.997419", "pred_label": "article"},
{"pred_prob": "0.532363", "pred_label": "other"},
]
```

## 调用html分类

```python
from llm_web_kit.model.html_layout_cls import HTMLLayoutClassifier

model = HTMLLayoutClassifier()
html_str_input = ['<html>layout1</html>', '<html>layout2</html>']
layout_type = model.predict(html_str_input)
print(layout_type)
```
