import re
from operator import attrgetter
from typing import Dict

from lxml.html import HtmlElement, fragment_fromstring

from llm_web_kit.extractor.html.magic_html.config import Unique_ID
from llm_web_kit.extractor.html.magic_html.utils import (_tostring,
                                                         ancestor_node_check,
                                                         text_len, trim)

DOT_SPACE = re.compile(r'\.( |$)')


def text_length(i):
    return len(trim(i.text_content() or ''))


class Candidate:
    def __init__(self, score: float, elem: HtmlElement) -> None:
        self.score: float = score
        self.elem: HtmlElement = elem


class Document:
    """readability_plus 正文抽取器.

    Attributes:
        html: 自定义抽取规则文件
        min_text_length: 最小文本长度
        xp_num: 命中正文区域规则id
        need_comment: 是否需要评论
        precision: 精确提取
    """

    def __init__(
            self,
            html: HtmlElement,
            min_text_length=25,
            xp_num='others',
            need_comment=False,
            precision=True
    ):
        self.html = html
        self.min_text_length = min_text_length
        self.xp_num = xp_num
        self.need_comment = need_comment
        self.precision = precision
        if not need_comment:
            self.REGEXES = {
                'unlikelyCandidatesRe': re.compile(
                    (r'combx|comment|community|disqus|extra|foot|header|menu|remark|rss|shoutbox|sidebar|sponsor|'
                     r'ad-break|agegate|pagination|pager|popup|tweet|twitter'),
                    re.I,
                ),
                'okMaybeItsACandidateRe': re.compile(
                    r'and|article|body|column|main|shadow', re.I
                ),
                'positiveRe': re.compile(
                    r'article|body|content|entry|hentry|main|page|pagination|post|text|blog|story',
                    re.I,
                ),
                'negativeRe': re.compile(
                    (r'combx|comment|com-|contact|foot|footer|footnote|masthead|media|meta|outbrain|promo|related|'
                     r'scroll|shoutbox|sidebar|sponsor|shopping|tags|tool|widget'),
                    re.I,
                ),
                'divToPElementsRe': re.compile(
                    r'<(a|blockquote|dl|div|img|ol|p|pre|table|ul)', re.I
                ),
                'videoRe': re.compile(r'https?:\/\/(www\.)?(youtube|vimeo)\.com', re.I),
            }
        else:
            self.REGEXES = {
                'unlikelyCandidatesRe': re.compile(
                    (r'combx|community|disqus|extra|foot|header|menu|remark|rss|shoutbox|sidebar|sponsor|ad-break|'
                     r'agegate|pagination|pager|popup|tweet|twitter'),
                    re.I,
                ),
                'okMaybeItsACandidateRe': re.compile(
                    r'and|article|body|column|main|shadow', re.I
                ),
                'positiveRe': re.compile(
                    r'article|body|content|entry|hentry|main|page|pagination|post|text|blog|story',
                    re.I,
                ),
                'negativeRe': re.compile(
                    (r'combx|com-|contact|foot|footer|footnote|masthead|media|meta|outbrain|promo|related|scroll|'
                     r'shoutbox|sidebar|sponsor|shopping|tags|tool|widget'),
                    re.I,
                ),
                'divToPElementsRe': re.compile(
                    r'<(a|blockquote|dl|div|img|ol|p|pre|table|ul)', re.I
                ),
                'videoRe': re.compile(r'https?:\/\/(www\.)?(youtube|vimeo)\.com', re.I),
            }

    def summary(self) -> str:
        if self.xp_num == 'others':
            self.remove_unlikely_candidates()
        self.transform_misused_divs_into_paragraphs()
        if self.xp_num == 'others':
            candidates = self.score_paragraphs()
            best_candidate = self.select_best_candidate(candidates)
            if best_candidate:
                article = self.get_article(candidates, best_candidate)
            else:
                article = self.html.find('body')
                if article is None:
                    article = self.html
        else:
            article = self.html
            candidates = {}
        self.sanitize(article, candidates)
        result = _tostring(self.html)
        body_html = re.sub(
            f' {Unique_ID}_oritag=".*?"',
            '', result
        )
        return body_html

    def get_article(self, candidates, best_candidate):
        sibling_score_threshold = max([10, best_candidate.score * 0.2])
        output = fragment_fromstring('<div/>')
        parent = best_candidate.elem.getparent()
        siblings = list(parent) if parent is not None else [best_candidate.elem]
        for sibling in siblings:
            append = False
            if sibling == best_candidate.elem or (
                    sibling in candidates
                    and candidates[sibling].score >= sibling_score_threshold
            ):
                append = True
            elif sibling.tag == 'p':
                link_density = self.get_link_density(sibling)
                node_content = sibling.text or ''
                node_length = len(node_content)

                if (
                        node_length > 80
                        and link_density < 0.25
                        or (
                        node_length <= 80
                        and link_density == 0
                        and DOT_SPACE.search(node_content)
                        )
                ):
                    append = True
            if append:
                output.append(sibling)
        return output

    def select_best_candidate(self, candidates):
        if not candidates:
            return None

        sorted_candidates = sorted(
            candidates.values(), key=attrgetter('score'), reverse=True
        )

        return next(iter(sorted_candidates))

    def get_link_density(self, elem):
        link_length = 0
        for i in elem.findall('.//a'):
            link_length += text_length(i)
        total_length = text_length(elem)
        return float(link_length) / max(total_length, 1)

    def score_paragraphs(self) -> Dict[HtmlElement, Candidate]:
        candidates = {}
        for elem in self.tags(self.html, 'p', 'pre', 'td'):
            parent_node = elem.getparent()
            if parent_node is None:
                continue
            grand_parent_node = parent_node.getparent()

            inner_text = trim(elem.text_content() or '')
            inner_text_len = len(inner_text)

            if inner_text_len < self.min_text_length:
                continue

            for node in (parent_node, grand_parent_node):
                if node is not None and node not in candidates:
                    candidates[node] = self.score_node(node)

            content_score = 1 + len(inner_text.split(',')) + len(inner_text.split('，')) + min((inner_text_len / 100), 3)

            candidates[parent_node].score += content_score
            if grand_parent_node is not None:
                candidates[grand_parent_node].score += content_score / 2

        for elem, candidate in candidates.items():
            candidate.score *= 1 - self.get_link_density(elem)

        return candidates

    def class_weight(self, e):
        weight = 0
        for feature in [e.get('class', None), e.get('id', None)]:
            if feature:
                if self.xp_num == 'others':
                    if self.REGEXES['negativeRe'].search(feature):
                        weight -= 25

                    if self.REGEXES['positiveRe'].search(feature):
                        weight += 25
                else:
                    if self.REGEXES['positiveRe'].search(feature):
                        weight += 25

        return weight

    def score_node(self, elem: HtmlElement) -> Candidate:
        content_score = self.class_weight(elem)
        name = elem.tag.lower()
        if name in ['div', 'article']:
            content_score += 5
        elif name in ['pre', 'td', 'blockquote']:
            content_score += 3
        elif name in ['address', 'ol', 'ul', 'dl', 'dd', 'dt', 'li', 'form', 'aside']:
            content_score -= 3
        elif name in [
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
            'th',
            'header',
            'footer',
            'nav',
        ]:
            content_score -= 5
        return Candidate(content_score, elem)

    def remove_unlikely_candidates(self):
        for elem in self.html.findall('.//*'):
            s = '%s %s' % (elem.get('class', ''), elem.get('id', ''))
            if len(s) < 2:
                continue
            if (
                    self.REGEXES['unlikelyCandidatesRe'].search(s)
                    and (not self.REGEXES['okMaybeItsACandidateRe'].search(s))
                    and elem.tag not in ['html', 'body']
            ):
                if ancestor_node_check(elem, ['code', 'pre']):
                    continue
                elem.drop_tree()

    def transform_misused_divs_into_paragraphs(self):
        for elem in self.tags(self.html, 'div'):
            if not self.REGEXES['divToPElementsRe'].search(
                    ''.join(map(_tostring, list(elem)))
            ):
                elem.attrib[f'{Unique_ID}_oritag'] = elem.tag
                elem.tag = 'p'

        for elem in self.tags(self.html, 'div'):
            if elem.text and elem.text.strip():
                p = fragment_fromstring('<p/>')
                p.attrib[f'{Unique_ID}_oritag'] = 'None'
                p.text = elem.text
                elem.text = None
                elem.insert(0, p)

            for pos, child in reversed(list(enumerate(elem))):
                if child.tail and child.tail.strip():
                    p = fragment_fromstring('<p/>')
                    p.attrib[f'{Unique_ID}_oritag'] = 'None'
                    p.text = child.tail
                    child.tail = None
                    elem.insert(pos + 1, p)
                # if child.tag == "br":
                #     child.drop_tree()

    def tags(self, node, *tag_names):
        for tag_name in tag_names:
            for e in node.findall('.//%s' % tag_name):
                yield e

    def reverse_tags(self, node, *tag_names):
        for tag_name in tag_names:
            for e in reversed(node.findall('.//%s' % tag_name)):
                yield e

    def sanitize(self, node, candidates):
        for header in self.tags(node, 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            if self.class_weight(header) < 0 or self.get_link_density(header) > 0.33:
                header.drop_tree()

        for elem in self.tags(node, 'iframe'):
            if 'src' in elem.attrib and self.REGEXES['videoRe'].search(
                    elem.attrib['src']
            ):
                elem.text = 'VIDEO'
            else:
                elem.drop_tree()

        allowed = set()

        for el in self.reverse_tags(
                node, 'table', 'ul', 'div', 'aside', 'header', 'footer', 'section'
        ):
            if el in allowed:
                continue
            weight = self.class_weight(el)
            content_score = candidates[el].score if el in candidates else 0

            tag = el.tag

            if weight + content_score < 0:
                el.drop_tree()
            elif el.text_content().count(',') + el.text_content().count('，') < 10:
                counts = {}
                for kind in ['p', 'img', 'li', 'a', 'embed', 'input']:
                    counts[kind] = len(el.findall('.//%s' % kind))
                counts['li'] -= 100
                counts['input'] -= len(el.findall('.//input[@type="hidden"]'))
                content_length = text_length(el)
                link_density = self.get_link_density(el)
                to_remove = False

                # 更多兼容多模态
                if el.tag == 'div' and counts['img'] >= 1:
                    continue

                if counts['input'] > (counts['p'] / 3):
                    to_remove = True
                elif content_length < self.min_text_length and counts['img'] == 0:
                    # 代码块内容过短，导致删除
                    if ancestor_node_check(el, ['code', 'pre']):
                        continue
                    # 保留table中的链接
                    if el.tag in ['ul', 'div'] and ancestor_node_check(el, ['td']):
                        continue
                    # precision
                    if not self.precision:
                        continue
                    to_remove = True
                elif content_length < self.min_text_length and counts['img'] > 2:
                    # precision
                    if not self.precision:
                        continue
                    to_remove = True
                elif weight < 25 and link_density > 0.2:
                    if tag in ['div', 'ul', 'table']:
                        ptest = el.xpath('.//text()[not(ancestor::a)]')
                        ptest_len = text_len(''.join(ptest))
                        if ptest_len >= self.min_text_length and link_density <= 0.3:
                            continue
                    if tag == 'table':
                        if len(el.xpath('.//tr[1]/td')) >= 2:
                            continue
                    if tag == 'div':
                        if el.xpath('.//table'):
                            continue
                    # precision
                    if not self.precision:
                        continue
                    to_remove = True
                elif weight >= 25 and link_density > 0.5:
                    if tag == 'table':
                        if len(el.xpath('.//tr[1]/td')) >= 2:
                            continue
                    if tag == 'div':
                        if el.xpath('.//table'):
                            continue
                    to_remove = True
                elif (counts['embed'] == 1 and content_length < 75) or counts[
                    'embed'
                ] > 1:
                    to_remove = True
                elif not content_length:
                    to_remove = True

                    siblings = []
                    for sib in el.itersiblings():
                        sib_content_length = text_length(sib)
                        if sib_content_length:
                            siblings.append(sib_content_length)
                            break
                    limit = len(siblings) + 1
                    for sib in el.itersiblings(preceding=True):
                        sib_content_length = text_length(sib)
                        if sib_content_length:
                            siblings.append(sib_content_length)
                            if len(siblings) >= limit:
                                break
                    if siblings and sum(siblings) > 1000:
                        to_remove = False
                        allowed.update(el.iter('table', 'ul', 'div', 'section'))

                if to_remove:
                    el.drop_tree()

        # 将transform_misused_divs_into_paragraphs还原
        for x in node.xpath(f'//p[@{Unique_ID}_oritag]'):
            ori_tag = x.attrib[f'{Unique_ID}_oritag']
            if ori_tag == 'None':
                x.drop_tag()
            else:
                x.tag = ori_tag

        self.html = node
