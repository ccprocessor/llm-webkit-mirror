## HTML解析流程

![](../../../docs/images/HTMLExtractor.png)
https://aicarrier.feishu.cn/wiki/PyMEwtTguiPtALkb5XDcYH20nYd

## 各元素转换后的标准定义

<table>
    <thead><td>标签</td><td>描述</td></thead>
    <tr>
        <td>&lt;ccmath&gt;</td>
        <td>
            &lt;cccode language="text|python|java|cpp"  by="codehilighter|fasttext_model|rule_xxx">def func():xxxxx&lt;/cccode&gt;<br/>
            - language：  什么编程语言<br/>
            - by： 用的什么方式识别的, 用于后期统计分析<br/>
        </td>
    </tr>
    <tr>
        <td>&lt;ccmath&gt;</td>
        <td>
            <ccmath type="kelatx|mathjax|mathml|??"  by=""> a=c^3</ccmath>
            - type： 什么标准的公式<br/>
            - by: 例如mathjax渲染的，mathml, rule等，根据对开源渲染框架调研定义<br/>
        </td>
    </tr>
    <tr>
        <td>&lt;ccimage&gt;</td>
        <td>
            &lt;ccimage type=""  by="img-src, img-embeded,  figure, object, canvas, svg"   title=""  alt=""  caption=""&gt;http://www.google.com/logo.jpg &lt;/ccimage&gt;<br/>
            - by: img-src代表从img的src里找到图片url, img-embeded代表从base64编码的内容里找到的...以此类推<br/>
            - title,   &lt;img 标签的title字段<br/>
            - alt: &lt;img  标签的alt字段<br/>
            - caption: 页面上描述字段，或者属性里的文字，如果能解析的话<br/>
        </td>
    </tr>
    <tr>
        <td>&lt;ccaudio&gt;</td>
        <td>
            暂时忽略
        </td>
    </tr>
    <tr>
        <td>&lt;ccvideo&gt;</td>
        <td>
            暂时忽略
        </td>
    </tr>
    <tr>
        <td>&lt;cctable&gt;</td>
        <td>
            &lt;cctable type="simple|complex"&gt; &lt;table&gt;xxxx ...&lt;/table&gt;&lt;/cctable&gt;<br/>
            - type<br/>
              - simple :代表没有跨行、跨列的简单表格，可被md渲染<br/>
              - complex: 代表有跨行、跨列的表格，不能被md渲染<br/>
        </td>
    </tr>
    <tr>
        <td>&lt;cclist&gt;</td>
        <td>
            &lt;cclist ordered="True|False"&gt;[{"c":"这里是一个列表项", "t":"text"}] &lt;cclist&gt;<br/>
            - ordered<br/>
              - True: 有序列表<br/>
              - False: 无序列表<br/>
        </td>
    </tr>
    <tr>
        <td>&lt;cctitle&gt;</td>
        <td>
            &lt;cctitle  level="1|2|3|4"&gt;标题&lt;/cctitle&gt;<br/>
            - level: 层级，最高标题层级（字最大）为1<br/>
        </td>
    </tr>
    <tr>
        <td>&lt;cctext&gt;</td>
        <td>
            &lt;cctext&gt;this is a para\n line 2.&lt;/cctext&gt;<br/>
        </td>
    </tr>
</table>

## 已知问题

**关于元素的解析顺序**<br>
理论上table, list里可以放图片、代码、公式、段落。由于关系复杂，标准不明。现在决定采取的解析策略如下：

1. 优先保证code, 因为目前发现有代码独占一个table的情况，因此code第一个解析。
2. 表格里的公式、图片、列表不做考虑。只考虑表格里的文字。对于图片直接丢弃，对于公式当成文本处理。
