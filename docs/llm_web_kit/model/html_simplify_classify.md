# HTML simplify及分类

对HTML进行简化，并分类。

文件格式如下：

```
--llm_web_kit/
	--model/
		--html_layout_cls.py  # 自动下载模型并解压，调用model.py
		--html_classify/      # markuplm的inference代码实现
		--html_lib/			  # 简化html
```

## HTML simplify

该部分用于简化HTML从而提高网页布局分类的效果。在 `llm_web_kit/model/html_lib/html_lib` 目录下的 `simplify.py` 文件中的 `general_simplify_html_str` 函数实现了对html字符串的简化操作。

默认路径为`~/.llm-web-kit.jsonc`中需要使用如下配置，可以自动下载模型：

```json
{
    "resources": {
        "common":{
            "cache_path": "~/.llm_web_kit_cache"
        },
        "html_cls-25m2": {
            "download_path": "s3://web-parse-huawei/shared_resource/html_layout_cls/html_cls_25m2.zip",
            "md5": "e15ea22a9aa65aa8c7c3a0e3c2e0c98a"
        },
	}
}
```

使用方法如下：

```python
from llm_web_kit.model.html_lib.simplify import general_simplify_html_str

raw_html = "<html><head></meta attr=\"attr\"></head><body><nav>some nav content</nav><p>some main content</p></body></html>"
simp_html = general_simplify_html_str(raw_html)
print(simp_html)
# like <html><p class="">some main content</p></html>
```

**注意：** 在使用HTML layout分类功能之前一定要先对HTML进行简化操作，否则可能会影响分类效果。

## HTML 分类

将简化后的html分类article, forum, other三个类别。在`llm_web_kit/model/html_layout_cls.py`中，使用`HTMLLayoutClassifier`类完成自动下载checkpoint和推理过程。

使用方法如下：

```python
from llm_web_kit.model.html_layout_cls import HTMLLayoutClassifier

model = HTMLLayoutClassifier()
html_str_input = ['<html>layout1</html>', '<html>layout2</html>']
layout_type = model.predict(html_str_input)
print(layout_type)
```
