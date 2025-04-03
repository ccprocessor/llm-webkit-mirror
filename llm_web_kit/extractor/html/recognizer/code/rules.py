from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.code.common import \
    replace_node_by_cccode

RULES_MAP = {
    'android.googlesource.com': {
        'code': './/table[contains(@class, "FileContents")]',
        'pre-formatted': True,
    },
    'www.test-inline-code-rules.com': {
        'inline-code': './/p[contains(@class, "code-style")]',
    },
}


def modify_tree(domain: str, root: HtmlElement):
    if 'code' in RULES_MAP[domain]:
        for code_node in root.xpath(RULES_MAP[domain]['code']):
            replace_node_by_cccode(code_node, 'preset_rules', RULES_MAP[domain].get('pre-formatted', False))

    if 'inline-code' in RULES_MAP[domain]:
        for inline_code_node in root.xpath(RULES_MAP[domain]['inline-code']):
            replace_node_by_cccode(inline_code_node, 'preset_rules', False, True)
