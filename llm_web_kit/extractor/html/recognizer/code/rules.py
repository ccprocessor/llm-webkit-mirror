import regex
from lxml.html import HtmlElement

from llm_web_kit.extractor.html.recognizer.code.common import \
    replace_node_by_cccode

_RULES_MAP = {
    regex.compile(r'\w+\.googlesource\.com'): {
        'code': {
            'root-xpath': './/table[contains(@class, "Blame") or contains(@class, "FileContents")]',
            'content-xpath': './/td[contains(@class, "Blame-lineContent") or contains(@class, "FileContents-lineContents")]',
            'pre-formatted': True,
        },
    },
    regex.compile(r'www\.test-inline-code-rules\.com'): {
        'inline-code': {
            'content-xpath': './/p[contains(@class, "code-style")]',
        }
    },
}


def detect(domain: str) -> bool:
    if not domain:
        return False

    for domain_pattern in _RULES_MAP.keys():
        if domain_pattern.match(domain):
            return True

    return False


def remove_non_content_text(root: HtmlElement, stop: list[HtmlElement]):
    if root in stop:
        return

    if root.tail:
        root.tail = None

    if root.text:
        root.text = None

    for child in root.iterchildren(None):
        remove_non_content_text(child, stop)


def modify_tree(domain: str, root: HtmlElement):
    for domain_pattern, domain_rule in _RULES_MAP.items():
        if not domain_pattern.match(domain):
            continue

        if 'code' in domain_rule:
            rule = domain_rule['code']
            for code_node in root.xpath(rule['root-xpath']):
                if 'content-xpath' in rule:
                    content_nodes = root.xpath(rule['content-xpath'])
                    remove_non_content_text(root, content_nodes)

                replace_node_by_cccode(code_node, 'preset_rules', rule.get('pre-formatted', False))

        if 'inline-code' in domain_rule:
            rule = domain_rule['inline-code']
            for code_node in root.xpath(rule['content-xpath']):
                replace_node_by_cccode(code_node, 'preset_rules', False, True)
