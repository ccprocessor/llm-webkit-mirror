# `lxml` 标准操作

## `lxml`库的组成

- `lxml.etree`: 包含`Element`和`ElementTree`两个类，用于构建和操作DOM树。算是lxml库的核心。
- `lxml.html`: 包含`HTMLParser`类，用于解析HTML。
  1. 可以处理标签不闭合的情况，而lmxl.etree则是严格模式。
  2. 支持一些html友好的操作，例如链接变绝对链接；css选择器等。
  3. 支持猜测html编码
- `lxml.html5lib parser`: python的html5lib库的解析器，支持html5规范校验。但是速度慢。
- `lxml.objectify`: 包含`ObjectifyElement`类，用于将XML数据转换为Python对象。这里基本用不上。
- `lxml.cssselect`: 包含`CSSSelector`类，用于CSS选择节点。

## 几个重要的概念

- lxml.etree.\_Element: 代表单个节点，节点既可以是HTML，也可以是XML。例如`<div>text <span>span</span></div>`, 一个Element可以包含子Element,可以包含属性。
- lxml.etree.\_ElementTree: 代表整个文档的一个wrapper，他也是`parser()`的返回值。

## `lxml.etree` 的常用方法

### 从字符串/文件/流/URL构建DOM树

总结起来一共有4个方法：

- `etree.fromstring(html_string, parser)`
- `etree.parse(file_path, parser)`
- `etree.XML(xml_string, parser)`
- `etree.HTML(html_string, parser)`

无论哪个方法，parser对象可选，可以通过parser对象控制解析行文。

- `collect_ids=False`: 是否收集元素的id属性
- `encoding='utf-8'`: 指定编码
- `remove_comments=True`: 是否移除注释
- `remove_pis=True`: 是否移除处理指令

parser类有以下几个可选择：

- `etree.XMLParser`: 用于解析XML,对格式要求严格
- `etree.HTMLParser`: 用于解析HTML，对格式要求不严格，例如标签不闭合，单双引号等。

方法1：`etree.fromstring(html_string, parser)`

```python
from lxml import etree
def use_etree_fromstring():
    html_string = "<div><p>Test</p></div>"
    tree = etree.fromstring(html_string)
    return tree

el = use_etree_fromstring()
source = etree.tostring(el)
print(source)

>> b'<div><p>Test</p></div>'
```

方法2：`etree.parse(file_path, parser)`

```python
from io import BytesIO

def use_etree_parse():
    stream = BytesIO(b"<div><p>Test</p></div>")
    tree = etree.parse(stream)
    return tree

el = use_etree_parse()
source = etree.tostring(el)
print(source)

>> b'<div><p>Test</p></div>'
```

方法3：`etree.XML(xml_string, parser)`

```python
def use_etree_xml():
    xml_string = "<div><p>Test</p></div>"
    tree = etree.XML(xml_string)
    return tree

el = use_etree_xml()
source = etree.tostring(el)
print(source)

>> b'<div><p>Test</p></div>'
```

方法4：`etree.HTML(html_string, parser)`

```python
def use_etree_html():
    html_string = "<div><p>Test</p></div>"
    tree = etree.HTML(html_string)
    return tree

el = use_etree_html()
source = etree.tostring(el)
print(source)

>> b'<html><body><div><p>Test</p></div></body></html>'
```

> ⚠️ 注意，`etree.HTML` 会自动添加`<html>`和`<body>`标签。因为他的默认解析器是`HTMLParser`，后者会自动添加这些标签。

此时通过更换parser对象，可以控制是否添加`<html>`和`<body>`标签。

```python
parser = etree.XMLParser(remove_pis=True)
html_string = "<div><p>Test</p></div>"
tree = etree.HTML(html_string, parser)
print(etree.tostring(tree))

>> b'<div><p>Test</p></div>'
```

## 2. 将节点转换为HTML字符串

```python

>>> root = etree.XML(
...    '<html><head/><body><p>Hello<br/>World</p></body></html>')

>>> etree.tostring(root)  # default: method = 'xml'
b'<html><head/><body><p>Hello<br/>World</p></body></html>'

>>> etree.tostring(root, method='xml')  # same as above
b'<html><head/><body><p>Hello<br/>World</p></body></html>'

>>> etree.tostring(root, method='html')
b'<html><head></head><body><p>Hello<br>World</p></body></html>'

>>> prettyprint(root, method='html')
<html>
<head></head>
<body><p>Hello<br>World</p></body>
</html>

>>> etree.tostring(root, method='text')
b'HelloWorld'
```

## 3. 复制一个DOM树/一个元素 deepcopy

## `lxml` FAQ

1. 读入的HTML字符串(非完整的HTML文档）中，如果包含注释，如何去掉。

```python
from lxml import etree

html_string = "<div><!-- comment --><p>Test</p></div>"
parser = etree.XMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
tree = etree.fromstring(html_string, parser)
print(etree.tostring(tree))

>> b'<div><p>Test</p></div>'
```

2. 整片HTML文档中，如果包含注释，如何去掉。

```python
from lxml import etree

html_string = "<html><body><!-- comment --><p>Test</p></body></html>"
parser = etree.HTMLParser(collect_ids=False, encoding='utf-8', remove_comments=True, remove_pis=True)
tree = etree.HTML(html_string, parser)
print(etree.tostring(tree))

>> b'<html><body><p>Test</p></body></html>'
```

## `lxml.html` 的常用方法

> 💚推荐这种，因为`lxml.html` 的解析器是`HTMLParser`，而`lxml.etree` 的解析器是`ETCompatHTMLParser`，后者是前者的子类。

- `lxml.html.parse(filename_url_or_file)`
- `lxml.html.document_fromstring(string)`
- `fragment_fromstring(string, create_parent=False)`
- `fragments_fromstring(string)`
- `fromstring(string)`

以上方法 返回值都是`lxml.html.HtmlElement`，

```python
from lxml import html
html_string = "<div><!-- comment --><p>Test</p></div>"

el = html.document_fromstring(html_string)
type(el)

>> <class 'lxml.html.HtmlElement'>

print(html.tostring(el))

b'<html><body><div><!-- comment --><p>Test</p></div></body></html>'

el2 = html.fragment_fromstring(html_string, create_parent=True)
print(html.tostring(el2))

b'<div><!-- comment --><p>Test</p></div>'

parser = html.HTMLParser(encoding='utf-8', remove_comments=True, remove_pis=True)
el3 = html.fragment_fromstring(html_string, parser=parser)
print(html.tostring(el3))

>> b'<div><p>Test</p></div>'

el4 = html.fragment_fromstring(html_string, parser=parser, create_parent=True)
print(html.tostring(el4))

>> b'<div><div><p>Test</p></div></div>'

el5 = html.fragment_fromstring(html_string, parser=parser, create_parent="ccelement")
print(html.tostring(el5))

>> b'<ccelement><div><p>Test</p></div></ccelement>'


```

## Ref

- [lxml 官方教程](https://lxml.de/tutorial.html)
- [lxml.html 官方教程](https://lxml.de/lxmlhtml.html)
