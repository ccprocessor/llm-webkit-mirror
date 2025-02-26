# html 分割方法（以code为例）

原始html

```html
<html>
<span>这是python</span>
<pre lang="python" class="code-highlight">
  <code>
    print("Hello, World!")
  </code>
</pre>
<span>例子结束</span>
</html>
```

经过cccode.py内部的代码识别处理之后，得到的html

```html
<html>
<span>这是python</span>
  <cccode language='python' by="codehilight">
    print("Hello, World!")
  </cccode>
<span>例子结束</span>
</html>
```

调用html分割：

```python
from llm_web_kit.extractor.html.recognizer.recognizer import
    BaseHTMLElementRecognizer

html = """<html>
    <span>这是python</span>
      <cccode language='python' by="codehilight">
        print("Hello, World!")
      </cccode>
    <span>例子结束</span>
    </html>"""
html_parts = BaseHTMLElementRecognizer.html_split_by_tags(html, 'cccode')
assert len(html_parts) == 3
```

得到的html_parts为：

```text
[
   "<span>这是python</span>",
    "
    <cccode language="python" by="codehilight">
        print("Hello, World!")
      </cccode>
    ",
    "<span>例子结束</span>"
]
```
