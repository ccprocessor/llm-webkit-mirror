from lxml import etree

from llm_web_kit.extractor.html.recognizer.cc_math.render import MathJaxRender
from llm_web_kit.libs.html_utils import html_to_element

# 测试[tex]...[/tex]格式的数学公式
print('\n测试[tex]...[/tex]格式的数学公式:')
text = '<p>where [tex]d^2(x_1,x_2)[/tex] is the squared distance between [tex]x_1[/tex] and [tex]x_2[/tex] in some metric space [tex]\\Theta[/tex]. All integrals are over [tex]\\Theta[/tex]</p>'
tree = html_to_element(text)
render = MathJaxRender()

# 处理前的HTML
print('处理前的HTML:')
print(etree.tostring(tree, encoding='unicode', pretty_print=True))

# 使用find_math处理数学公式
render.find_math(tree)

# 处理后的HTML
print('\n处理后的HTML:')
processed_html = etree.tostring(tree, encoding='unicode', pretty_print=True)
print(processed_html)

# 查找处理后的ccmath节点
ccmath_nodes = tree.xpath('.//*[self::ccmath-inline or self::ccmath-interline]')
print(f'\n找到 {len(ccmath_nodes)} 个数学公式节点:')
for i, node in enumerate(ccmath_nodes, 1):
    print(f'{i}. <{node.tag}> {node.text}')
