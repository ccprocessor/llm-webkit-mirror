
from llm_web_kit.model.html_lib.simplify import general_simplify_html_str


def test_general_simplify_html_str():
    # 测试用例1：简单的HTML字符串
    html_input = '<html><body><h1>Title</h1><p>Paragraph</p></body></html>'
    # 假设简化后不变
    expected_output = '<html><body><h1>Title</h1><p>Paragraph</p></body></html>'
    assert general_simplify_html_str(html_input) == expected_output

    # 测试用例2：空标签
    html_input = '<html><body><h1>Title</h1><p>Paragraph</p><p></p></body></html>'
    # 假设简化后删除空标签
    expected_output = '<html><body><h1>Title</h1><p>Paragraph</p></body></html>'
    assert general_simplify_html_str(html_input) == expected_output

    # 测试用例3：多个span
    html_input = '<html><body><h1>Title<p><span>First text</span><span>Second text</span></p></body></html>'
    # 拼成一个span
    expected_output = '<html><body><h1>Title</h1><p><span>First text Second text</span></p></body></html>'
    assert general_simplify_html_str(html_input) == expected_output
