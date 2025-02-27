import re

from lxml.html import Element, fromstring

from llm_web_kit.extractor.html.magic_html.config import Forum_XPATH, Unique_ID
from llm_web_kit.extractor.html.magic_html.extractors.base_extractor import \
    BaseExtractor
from llm_web_kit.extractor.html.magic_html.extractors.title_extractor import \
    TitleExtractor
from llm_web_kit.extractor.html.magic_html.utils import _tostring, load_html


class ForumExtractor(BaseExtractor):
    """论坛类型抽取器."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.need_comment = True

    def extract(self, html='', base_url='') -> dict:
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
        if tree is None:
            raise ValueError

        # 获取title
        title = TitleExtractor().process(tree)

        # base_url
        base_href = tree.xpath('//base/@href')

        if base_href and 'http' in base_href[0]:
            base_url = base_href[0]
        self.generate_unique_id(tree)

        format_tree = self.convert_tags(tree)

        normal_tree = self.clean_tags(format_tree)

        subtree, xp_num, drop_list = self.xp_1_5(normal_tree)
        if xp_num == 'others':
            subtree, drop_list = self.prune_unwanted_sections(normal_tree)
        body_html = self.get_content_html(subtree, xp_num)

        # 论坛等独有
        body_html_tree = fromstring(body_html)
        try:
            body_tree = body_html_tree.body
        except Exception:
            body_tree = Element('body')
            body_tree.extend(body_html_tree)
        main_ids = body_tree.xpath(f'.//@{Unique_ID}')

        for main_id in main_ids:
            main_tree = normal_tree.xpath(
                f'.//*[@{Unique_ID}={main_id}]'
            )
            if main_tree:
                self.remove_node(main_tree[0])
        if not main_ids:
            main_ids = [-1]

        if xp_num != 'others':
            normal_tree, _ = self.prune_unwanted_sections(normal_tree)
        for c_xpath in Forum_XPATH:
            while normal_tree.xpath(c_xpath):
                x = normal_tree.xpath(c_xpath)[0]
                self.remove_node(x)
                if "'post-'" in c_xpath:
                    if not (re.findall(r'post-\d+', x.attrib.get('id', '').lower()) or re.findall(r'post_\d+',
                                                                                                  x.attrib.get('id',
                                                                                                               '').lower())):
                        continue
                if (
                        'header' in x.attrib.get('class', '').lower()
                        or 'header' in x.attrib.get('id', '').lower()
                ):
                    continue
                try:
                    if int(x.attrib.get(Unique_ID, '0')) > int(
                            main_ids[-1]
                    ):
                        body_tree.append(x)
                    else:
                        prefix_div = Element('div')
                        suffix_div = Element('div')
                        need_prefix = False
                        need_suffix = False
                        while x.xpath(
                                f'.//*[number(@{Unique_ID}) > {int(main_ids[-1])}]'
                        ):
                            tmp_x = x.xpath(
                                f'.//*[number(@{Unique_ID}) > {int(main_ids[-1])}]'
                            )[0]
                            self.remove_node(tmp_x)
                            suffix_div.append(tmp_x)
                            need_suffix = True
                        while x.xpath(
                                f'.//*[number(@{Unique_ID}) < {int(main_ids[-1])}]'
                        ):
                            tmp_x = x.xpath(
                                f'.//*[number(@{Unique_ID}) < {int(main_ids[-1])}]'
                            )[0]
                            self.remove_node(tmp_x)
                            prefix_div.append(tmp_x)
                            need_prefix = True
                        if need_prefix:
                            body_tree.insert(0, prefix_div)
                        if need_suffix:
                            body_tree.append(suffix_div)

                except Exception:
                    pass

        body_html = re.sub(
            fr' {Unique_ID}="\d+"',
            '',
            _tostring(body_tree),
        )

        return {
            'xp_num': xp_num,
            'drop_list': drop_list,
            'html': body_html,
            'title': title,
            'base_url': base_url
        }
