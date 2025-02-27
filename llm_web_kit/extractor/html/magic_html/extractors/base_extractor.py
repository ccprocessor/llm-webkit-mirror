import re
from collections import defaultdict
from copy import deepcopy
from typing import Tuple

from lxml.etree import Comment, _Element, strip_elements, strip_tags
from lxml.html import Element, HtmlElement

from llm_web_kit.extractor.html.magic_html.config import (
    BODY_XPATH, CONTENT_EXTRACTOR_NOISE_XPATHS, CUT_EMPTY_ELEMS,
    DISCARD_IMAGE_ELEMENTS, MANUALLY_CLEANED, MANUALLY_STRIPPED,
    OVERALL_DISCARD_XPATH, PAYWALL_DISCARD_XPATH, REMOVE_COMMENTS_XPATH,
    TEASER_DISCARD_XPATH, USELESS_ATTR, Forum_XPATH, Unique_ID)
from llm_web_kit.extractor.html.magic_html.readability_plus import \
    Document as DocumentPlus
from llm_web_kit.extractor.html.magic_html.utils import (
    ancestor_node_check, density_of_a_text, img_div_check, iter_node,
    link_density_test, similarity_with_siblings, text_len, trim, uniquify_list)


class BaseExtractor:
    """抽取器."""

    def __init__(self, need_comment=False, precision=True):
        self.need_comment = need_comment
        self.precision = precision

    def xp_1_5(self, tree: HtmlElement) -> Tuple[_Element, str, bool]:
        """基于规则抽取1-5.

        Args:
            tree: HtmlElement

        Returns:
            Tuple. For example:
            Element("body"), "1", False
        """
        drop_list = False
        xp_num = 'others'
        result_body = Element('body')

        for idx, expr in enumerate(BODY_XPATH):
            try:
                subtree = tree.xpath(expr)[0]
                xp_num = str(idx + 1)
            except IndexError:
                continue

            subtree, drop_list = self.prune_unwanted_sections(subtree)

            if len(subtree) == 0:
                xp_num = 'others'
                continue

            ptest = subtree.xpath('.//text()[not(ancestor::a)]')
            ptest_len = text_len(''.join(ptest))
            all_text_len = text_len(
                ''.join(tree.xpath('//p//text()[not(ancestor::a)]'))
            )
            if drop_list:
                if ptest_len <= 50:
                    if all_text_len > 100:
                        xp_num = 'others'
                    continue
            else:
                if ptest_len <= 20:
                    if all_text_len > 100:
                        xp_num = 'others'
                    continue
            result_body.append(subtree)
            return result_body, xp_num, drop_list

        return result_body, xp_num, drop_list

    def get_content_html(self, cleaned_tree_backup, xp_num='others'):
        """基于readability_plus抽取.

        Args:
            cleaned_tree_backup:  HtmlElement
            xp_num: 命中正文区域规则id

        Returns:
            网页正文区域str. For example:
            "<body></body>"
        """
        doc = DocumentPlus(
            cleaned_tree_backup,
            xp_num=xp_num,
            need_comment=self.need_comment,
            precision=self.precision
        )
        body = doc.summary()

        return body

    def prune_unwanted_nodes(self, tree, nodelist, with_backup=False):
        if with_backup is True:
            old_len = len(tree.text_content())
            backup = deepcopy(tree)
        for expr in nodelist:
            for subtree in tree.xpath(expr):

                # DISCARD_IMAGE_ELEMENTS 需要特殊判断
                if '"caption"' in expr and subtree.xpath('.//img'):
                    continue
                # 有些出现hidden
                if 'hidden' in expr:
                    try:
                        if re.findall(
                                r'overflow-x:\s*hidden', subtree.attrib['style']
                        ) or re.findall(
                            r'overflow-y:\s*hidden', subtree.attrib['style']
                        ):
                            continue
                        if re.findall(
                                r'overflow:\s*hidden', subtree.attrib['style']
                        ) and re.findall('height:', subtree.attrib['style']):
                            height_px = re.findall(
                                r'height:\s*(\d+)', subtree.attrib['style']
                            )[0]
                            if int(height_px) >= 800:
                                continue
                    except Exception:
                        pass

                if ancestor_node_check(subtree, ['code', 'pre']):
                    continue
                self.remove_node(subtree)
        if with_backup is False:
            return tree
        # else:
        new_len = len(tree.text_content())
        if new_len > old_len / 7:
            return tree
        return backup

    def prune_html(self, tree: HtmlElement) -> HtmlElement:
        for element in tree.xpath('.//processing-instruction()|.//*[not(node())]'):
            if element.tag in CUT_EMPTY_ELEMS:
                self.remove_node(element)
        return tree

    def remove_node(self, element: HtmlElement):
        """删除节点.

        删除节点时，保留节点后的tail文本

        Args:
            element: HtmlElement
        """
        parent = element.getparent()
        if parent is None:
            return

        if element.tail:
            previous = element.getprevious()
            if previous is None:
                parent.text = (parent.text or '') + element.tail
            else:
                previous.tail = (previous.tail or '') + element.tail

        parent.remove(element)

    def convert_tags(self, element: HtmlElement) -> HtmlElement:
        """遍历节点，特定标签转换.

        此处预留math公式处理

        Args:
            element: HtmlElement

        Returns:
            HtmlElement
        """
        USELESS_ATTR_LIST = USELESS_ATTR
        if not self.need_comment:
            USELESS_ATTR_LIST = USELESS_ATTR_LIST + ['comment']
        for node in iter_node(element):
            # if node.tag.lower() == "div" and not node.getchildren():
            #     node.tag = "p"
            class_name = node.get('class')
            if class_name:
                if class_name.lower() in USELESS_ATTR_LIST:
                    if ancestor_node_check(node, ['code', 'pre']):
                        continue
                    self.remove_node(node)
        return element

    def clean_tags(self, tree: HtmlElement) -> HtmlElement:
        """清理特定样式的标签.

        Args:
            tree: HtmlElement

        Returns:
            HtmlElement
        """
        strip_elements(tree, Comment)

        xp_lists = []
        if not self.need_comment:
            xp_lists.append(REMOVE_COMMENTS_XPATH)
        xp_lists.append(CONTENT_EXTRACTOR_NOISE_XPATHS)
        for xp_list in xp_lists:
            tree = self.prune_unwanted_nodes(tree, xp_list)

        cleaning_list, stripping_list = MANUALLY_CLEANED.copy(), MANUALLY_STRIPPED.copy()
        for elem in tree.xpath('.//figure[descendant::table]'):
            elem.tag = 'div'

        strip_tags(tree, stripping_list)

        for expression in cleaning_list + ['form']:
            for element in tree.iter(expression):
                # 针对form 标签特殊处理
                if element.tag == 'form':
                    ptest = element.xpath('.//text()[not(ancestor::a)]')
                    if text_len(''.join(ptest)) <= 60:  # 50
                        self.remove_node(element)
                else:
                    self.remove_node(element)
        return self.prune_html(tree)

    def generate_unique_id(self, element):
        idx = 0
        for node in iter_node(element):
            l_tag = node.tag.lower()
            if l_tag not in ['html', 'body']:
                node.attrib[Unique_ID] = str(idx)
                idx += 1

    def delete_by_link_density(
            self, subtree, tagname, backtracking=False, favor_precision=False
    ):
        need_del_par = []
        skip_par = []
        drop_list = False
        for descendant in subtree.iter(tagname):
            pparent = descendant.getparent()
            if pparent in need_del_par or pparent in skip_par:
                continue
            siblings = descendant.xpath(f'following-sibling::{tagname}')

            if 'list' in descendant.get('class', '') and len(descendant.xpath('./a')) >= 5:
                need_del_par.append(descendant)
                need_del_par.extend(siblings)
                continue

            nn = [descendant]
            nn.extend(siblings)
            txt_max_num = 0
            if len(siblings) + 1 >= 4:
                pass
            else:
                txt_max_dict = {
                    'read': 0,
                    'more': 0,
                    '...': 0,
                    '阅读': 0,
                    '更多': 0,
                    '详细': 0,
                    'detail': 0,
                    'article': 0,
                    'blog': 0,
                    'news': 0,
                }
                if tagname == 'div' or tagname == 'article' or tagname == 'section':
                    for j in nn:
                        txt = ''.join(j.xpath('.//text()')).strip()
                        for x in [
                            'read',
                            'more',
                            '...',
                            '阅读',
                            '更多',
                            '详细',
                            'detail',
                            'article',
                            'blog',
                            'news',
                        ]:
                            if txt.lower().endswith(x):
                                txt_max_dict[x] += 1
                        txt_num = max(txt_max_dict.values())
                        if txt_max_num < txt_num:
                            txt_max_num = txt_num
                        if txt_max_num >= 3:
                            break
                if txt_max_num >= 3:
                    pass
                else:
                    continue
            skip_par.append(pparent)
            a_num = 0
            for j in siblings:
                if j.xpath('.//a'):
                    if tagname == 'p':
                        if density_of_a_text(j, pre=0.8):
                            a_num += 1
                    elif tagname in ['div', 'section', 'article']:
                        if density_of_a_text(j, pre=0.2):
                            a_num += 1
                    else:
                        if self.need_comment:
                            # 增加判断是否包含评论 再决定是否删除
                            break_flg = False
                            for c_xpath in Forum_XPATH[:-1]:
                                if j.xpath(c_xpath.replace('.//*', 'self::*')):
                                    break_flg = True
                                    break
                            if break_flg:
                                continue
                        if tagname == 'li':
                            if text_len(''.join(j.xpath('.//text()[not(ancestor::a)]'))) > 50:
                                continue
                        a_num += 1

            if a_num < len(siblings):
                if a_num >= 15 and (
                        tagname == 'div' or tagname == 'article' or tagname == 'section'
                ):
                    pass
                else:
                    continue

            similarity_with_siblings_nums = similarity_with_siblings(
                descendant, siblings
            )
            if tagname == 'article' or tagname == 'item':  # or tagname == "section"
                similarity_with_siblings_nums = similarity_with_siblings_nums * 1.5
            # 列表有个很特殊的地方 另一种情况就是 descendant和siblings 都包含title/h1 | h2 标签
            if tagname == 'div' or tagname == 'article' or tagname == 'section':
                title_max_num = 0
                for ll in [".//head[@rend='h2']", ".//head[@rend='h1']", './article']:
                    title_num = 0
                    for jj in nn:
                        if jj.xpath(ll):
                            title_num += 1
                    if title_max_num < title_num:
                        title_max_num = title_num
                if title_max_num >= 4:
                    similarity_with_siblings_nums = similarity_with_siblings_nums * 1.5

            if txt_max_num >= 3:
                pass
            elif similarity_with_siblings_nums < 0.84:
                if len(siblings) >= 15 and (
                        tagname == 'div' or tagname == 'article' or tagname == 'section'
                ):
                    pass
                else:
                    continue
            # 父div中包含多同级div 且div class post-时，删除其余节点，保留第一篇文章
            class_attr = descendant.get('class') if descendant.get('class') else ''
            if (
                    re.findall('post-', class_attr, re.I)
                    or re.findall('-post', class_attr, re.I)
                    or re.findall('blog|aricle', class_attr, re.I)
            ):
                drop_list = True
                sk_flg = True
                for dl in siblings:
                    if (
                            text_len(''.join(descendant.xpath('.//text()'))) * 2
                            < text_len(''.join(dl.xpath('.//text()')))
                            and sk_flg
                    ):
                        self.remove_node(descendant)
                        sk_flg = False
                    else:
                        self.remove_node(dl)
            else:
                need_del_par.append(descendant)
                need_del_par.extend(siblings)
        for node in need_del_par:
            drop_list = True
            try:
                self.remove_node(node)
            except Exception:
                pass

        myelems, deletions = defaultdict(list), []

        if tagname == 'div':
            for elem in subtree.iter(tagname):
                if density_of_a_text(elem, pre=0.8) and img_div_check(elem):
                    deletions.append(elem)

        for elem in subtree.iter(tagname):
            elemtext = trim(elem.text_content())
            result, templist = link_density_test(elem, elemtext, favor_precision)
            if result is True and img_div_check(elem):
                # 保留table中的链接
                if tagname in ['ul', 'li', 'div', 'p'] and ancestor_node_check(elem, ['td']):
                    continue
                deletions.append(elem)
            elif backtracking is True and len(templist) > 0:
                myelems[elemtext].append(elem)
        if backtracking is True:
            if favor_precision is False:
                threshold = 100
            else:
                threshold = 200
            for text, elem in myelems.items():
                if 0 < len(text) < threshold and len(elem) >= 3:
                    deletions.extend(elem)

        for elem in uniquify_list(deletions):
            try:
                if self.need_comment:
                    # 增加判断是否包含评论 再决定是否删除
                    break_flg = False
                    for c_xpath in Forum_XPATH[:-1]:
                        if elem.xpath(c_xpath):
                            break_flg = True
                            break
                    if break_flg:
                        continue

                # precision
                if not self.precision:
                    xpath_expr = """
                     boolean(
                       following-sibling::*[position() <= 2]/self::p |
                       preceding-sibling::*[position() <= 2]/self::p |
                       parent::*/following-sibling::*[position() <= 2]/self::p |
                       parent::*/preceding-sibling::*[position() <= 2]/self::p
                     )
                     """
                    if elem.xpath(xpath_expr):
                        continue

                self.remove_node(elem)
            except AttributeError:
                pass
        return subtree, drop_list

    def prune_unwanted_sections(self, tree: HtmlElement) -> Tuple[HtmlElement, bool]:
        """

        Args:
            tree: HtmlElement

        Returns:
            HtmlElement和是否删除列表. For example:
            HtmlElement, True
        """
        tmp_OVERALL_DISCARD_XPATH = OVERALL_DISCARD_XPATH
        if self.need_comment:
            tmp_OVERALL_DISCARD_XPATH = tmp_OVERALL_DISCARD_XPATH[:-1]
        tree = self.prune_unwanted_nodes(
            tree, tmp_OVERALL_DISCARD_XPATH, with_backup=True
        )
        for xp_list in [
            PAYWALL_DISCARD_XPATH,
            TEASER_DISCARD_XPATH,
            DISCARD_IMAGE_ELEMENTS,
        ]:
            tree = self.prune_unwanted_nodes(tree, xp_list)
        # remove elements by link density
        tree, drop_list_1 = self.delete_by_link_density(
            tree, 'div', backtracking=True, favor_precision=False
        )
        tree, drop_list_1_1 = self.delete_by_link_density(
            tree, 'article', backtracking=False, favor_precision=False
        )
        tree, drop_list_1_2 = self.delete_by_link_density(
            tree, 'section', backtracking=False, favor_precision=False
        )
        tree, drop_list_2_1 = self.delete_by_link_density(
            tree, 'ul', backtracking=False, favor_precision=False
        )
        tree, drop_list_2_2 = self.delete_by_link_density(
            tree, 'li', backtracking=False, favor_precision=False
        )
        tree, drop_list_3_1 = self.delete_by_link_density(
            tree, 'dl', backtracking=False, favor_precision=False
        )
        tree, drop_list_3_3 = self.delete_by_link_density(
            tree, 'dt', backtracking=False, favor_precision=False
        )
        tree, drop_list_3_2 = self.delete_by_link_density(
            tree, 'dd', backtracking=False, favor_precision=False
        )
        tree, drop_list_3 = self.delete_by_link_density(
            tree, 'p', backtracking=False, favor_precision=False
        )

        return (
            tree,
            drop_list_1
            or drop_list_2_1
            or drop_list_2_2
            or drop_list_3
            or drop_list_1_1
            or drop_list_1_2
            or drop_list_3_1
            or drop_list_3_2
            or drop_list_3_3,
        )
