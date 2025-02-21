from llm_web_kit.extractor.html.magic_html.extractors.base_extractor import \
    BaseExtractor
from llm_web_kit.extractor.html.magic_html.extractors.title_extractor import \
    TitleExtractor
from llm_web_kit.extractor.html.magic_html.utils import load_html


class ArticleExtractor(BaseExtractor):
    """文章类型抽取器."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract(self, html: str = '', base_url: str = '') -> dict:
        """抽取内容方法.

        Args:
            html: 网页str
            base_url: 网页对应的url

        Returns:
            抽取结果dict. For example:
            {
            "xp_num": "1",
            "drop_list": True,
            "html": "<html></html>",
            "title": "title",
            "base_url": "http://test.com/",
             }
        """
        tree = load_html(html)

        title = TitleExtractor().process(tree)

        # base_url
        base_href = tree.xpath('//base/@href')

        if base_href and 'http' in base_href[0]:
            base_url = base_href[0]

        if '://blog.csdn.net/' in base_url:
            for dtree in tree.xpath('//div[@id="content_views"]//ul[@class="pre-numbering"]'):
                self.remove_node(dtree)

        # 标签遍历&转换
        format_tree = self.convert_tags(tree)

        # 删除script style等标签及其内容
        normal_tree = self.clean_tags(format_tree)

        subtree, xp_num, drop_list = self.xp_1_5(normal_tree)
        if xp_num == 'others':
            subtree, drop_list = self.prune_unwanted_sections(normal_tree)
        body_html = self.get_content_html(subtree, xp_num)

        return {
            'xp_num': xp_num,
            'drop_list': drop_list,
            'html': body_html,
            'title': title,
            'base_url': base_url,
        }
