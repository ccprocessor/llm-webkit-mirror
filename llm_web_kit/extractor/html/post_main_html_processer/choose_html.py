from collections import Counter
from typing import List

from lxml import etree

from llm_web_kit.libs.html_utils import html_to_element

IGNORE_TAGS = {'script', 'style', 'meta', 'link', 'br', 'noscript'}
# 语义化标签
SEMANTIC_TAGS = {
    'header', 'nav', 'main', 'article', 'section', 'aside',
    'footer', 'figure', 'figcaption', 'time', 'mark', 'summary',
    'details', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
}
# 交互标签
INTERACTIVE_TAGS = {'a', 'button', 'input', 'select', 'textarea', 'img', 'audio', 'video'}
# 各项指标的权重
WEIGHTS = {
    'tag_diversity': 0.25,  # 标签多样性权重
    'total_elements': 0.2,  # 元素总数权重
    'max_depth': 0.15,  # 嵌套深度权重
    'semantic_tags': 0.25,  # 语义标签权重
    'styled_elements': 0.1,  # 样式元素权重
    'interactive_elements': 0.05  # 交互元素权重
}


def select_typical_htmls(html_strings: List[dict], select_n: int = 3) -> List[dict]:
    """从多个HTML中选择最具代表性的select_n个HTML.

    Args:
        html_strings:
        {
            "html": "html字符串",
            "filename": "html路径"
        }
        select_n: 需要选择的HTML数量，默认为3

    Returns:
        选中的HTML字符串列表
    """
    if not html_strings:
        return []

    # 分析每个HTML
    html_analysis = []
    for htmlstr_file in html_strings:
        try:
            analysis = __analyze_html_structure(htmlstr_file['html'])
            if analysis:
                analysis['html'] = htmlstr_file['html']
                analysis['filename'] = htmlstr_file['filename']
                html_analysis.append(analysis)
        except Exception:
            continue

    # 根据多个维度评分并排序
    scored_htmls = []
    for analysis in html_analysis:
        score = __calculate_representativeness_score(analysis)
        scored_htmls.append({
            'html': analysis['html'],
            'filename': analysis['filename'],
            'score': score,
            'analysis': analysis
        })

    # 按分数排序并选择前select_n个
    scored_htmls.sort(key=lambda x: x['score'], reverse=True)
    return scored_htmls[:select_n] if scored_htmls else []


def __analyze_html_structure(html_str: str) -> dict:
    """分析HTML结构特征.

    Args:
        html_str: HTML字符串

    Returns:
        包含分析结果的字典
    """
    try:
        tree = html_to_element(html_str)
    except Exception:
        return None

    # 获取所有元素
    all_elements = list(tree.iter())

    # 过滤有效标签
    valid_elements = [elem for elem in all_elements if __is_valid_tag(elem.tag)]

    if not valid_elements:
        return None

    # 统计标签类型
    tag_counter = Counter(elem.tag for elem in valid_elements)

    # 计算结构复杂度指标
    metrics = {
        # 标签多样性
        'tag_diversity': len(tag_counter),

        # 总元素数
        'total_elements': len(valid_elements),

        # 嵌套深度
        'max_depth': __calculate_max_depth(tree),

        # 结构化语义标签使用情况
        'semantic_tags': __count_semantic_tags(valid_elements),

        # CSS类和ID的使用
        'styled_elements': __count_styled_elements(valid_elements),

        # 链接和媒体元素
        'interactive_elements': __count_interactive_elements(valid_elements),
    }

    return metrics


def __is_valid_tag(tag: str) -> bool:
    """检查是否为有效的HTML标签."""
    return (tag and isinstance(tag, str) and
            tag not in IGNORE_TAGS and
            not tag.startswith('<cyfunction'))


def __calculate_max_depth(element: etree.Element) -> int:
    """计算DOM树的最大深度.

    Args:
        element: 根元素

    Returns:
        最大深度
    """
    if not element.getchildren():
        return 1

    max_child_depth = 0
    for child in element.getchildren():
        if __is_valid_tag(child.tag):
            child_depth = __calculate_max_depth(child)
            max_child_depth = max(max_child_depth, child_depth)

    return max_child_depth + 1


def __count_semantic_tags(elements: List[etree.Element]) -> int:
    """计算语义化标签的数量.

    Args:
        elements: 元素列表

    Returns:
        语义化标签数量
    """
    return len([elem for elem in elements if elem.tag in SEMANTIC_TAGS])


def __count_styled_elements(elements: List[etree.Element]) -> int:
    """计算有样式属性的元素数量.

    Args:
        elements: 元素列表

    Returns:
        有样式属性的元素数量
    """
    count = 0
    for elem in elements:
        if 'class' in elem.attrib or 'id' in elem.attrib:
            count += 1
    return count


def __count_interactive_elements(elements: List[etree.Element]) -> int:
    """计算交互元素数量.

    Args:
        elements: 元素列表

    Returns:
        交互元素数量
    """

    return len([elem for elem in elements if elem.tag in INTERACTIVE_TAGS])


def __calculate_representativeness_score(analysis: dict) -> float:
    """计算HTML的代表性分数.

    Args:
        analysis: HTML分析结果

    Returns:
        代表性分数
    """
    if not analysis:
        return 0.0

    # 归一化各项指标（避免某些指标过大影响结果）
    normalized_scores = {}

    # 标签多样性得分 (通常10-30种标签)
    normalized_scores['tag_diversity'] = min(analysis.get('tag_diversity', 0) / 20.0, 1.0)

    # 元素总数得分 (通常几十到几百个元素)
    normalized_scores['total_elements'] = min(analysis.get('total_elements', 0) / 100.0, 1.0)

    # 嵌套深度得分 (通常2-10层)
    normalized_scores['max_depth'] = min(analysis.get('max_depth', 0) / 8.0, 1.0)

    # 语义标签得分
    normalized_scores['semantic_tags'] = min(analysis.get('semantic_tags', 0) / 10.0, 1.0)

    # 样式元素得分
    normalized_scores['styled_elements'] = min(analysis.get('styled_elements', 0) / 20.0, 1.0)

    # 交互元素得分
    normalized_scores['interactive_elements'] = min(analysis.get('interactive_elements', 0) / 10.0, 1.0)

    # 计算加权总分
    total_score = sum(normalized_scores[key] * WEIGHTS[key] for key in WEIGHTS)

    return total_score
