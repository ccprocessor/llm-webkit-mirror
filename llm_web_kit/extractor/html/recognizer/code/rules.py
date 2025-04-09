from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.code.common import \
    replace_node_by_cccode

RULES_MAP = {
    'android.googlesource.com': {
        'code': {
            'content-xpath': './/table[contains(@class, "FileContents")]',
            'pre-formatted': True,
        },
    },
    'www.test-inline-code-rules.com': {
        'inline-code': {
            'content-xpath': './/p[contains(@class, "code-style")]',
        }
    },
}


def modify_tree(domain: str, root: HtmlElement):
    if 'code' in RULES_MAP[domain]:
        rule = RULES_MAP[domain]['code']
        for code_node in root.xpath(rule['content-xpath']):
            replace_node_by_cccode(code_node, 'preset_rules', rule.get('pre-formatted', False))

    if 'inline-code' in RULES_MAP[domain]:
        rule = RULES_MAP[domain]['inline-code']
        for code_node in root.xpath(rule['content-xpath']):
            replace_node_by_cccode(code_node, 'preset_rules', False, True)
