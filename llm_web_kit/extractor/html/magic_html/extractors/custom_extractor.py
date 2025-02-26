from lxml.html import HtmlElement

from llm_web_kit.extractor.html.magic_html.extractors.base_extractor import \
    BaseExtractor
from llm_web_kit.extractor.html.magic_html.extractors.title_extractor import \
    TitleExtractor
from llm_web_kit.extractor.html.magic_html.utils import _tostring, load_html


class CustomExtractor(BaseExtractor):
    """自定义规则类型抽取器."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def use_clean_rule(self, tree: HtmlElement, clean_rules: dict) -> HtmlElement:
        for clean_rule in clean_rules:
            for x in tree.xpath(clean_rule):
                self.remove_node(x)
        return tree

    def use_extract_rule(self, tree: HtmlElement, extract_rule: dict) -> HtmlElement | str:
        if '/text()' in extract_rule['value']:
            return ''.join(tree.xpath(extract_rule['value'])).strip()
        return tree.xpath(extract_rule['value'])[0]

    def extract(self, html: str = '', base_url: str = '', rule: dict = dict) -> dict:
        """抽取内容方法.

        Args:
            html: 网页str
            base_url: 网页对应的url
            rule: 自定义抽取规则

        Returns:
            抽取结果dict. For example:
            {
            "xp_num": "custom",
            "drop_list": True,
            "html": "<html></html>",
            "title": "title",
            "base_url": "http://test.com/",
             }
        """
        tree = load_html(html)
        if tree is None:
            raise ValueError

        # base_url
        base_href = tree.xpath('//base/@href')

        if base_href and 'http' in base_href[0]:
            base_url = base_href[0]

        if 'clean' in rule:
            tree = self.use_clean_rule(tree, rule['clean'])

        # 获取title
        if 'title' not in rule:
            title = TitleExtractor().process(tree)
        else:
            title = self.use_extract_rule(tree, rule['title'])

        # 文章区域
        try:
            body_tree = self.use_extract_rule(tree, rule['content'])
        except Exception:
            raise ValueError
        body_html = _tostring(body_tree)

        return {
            'xp_num': 'custom',
            'drop_list': False,
            'html': body_html,
            'title': title,
            'base_url': base_url
        }
