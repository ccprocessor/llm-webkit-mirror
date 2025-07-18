import math
import re
from collections import defaultdict
from io import StringIO

from lxml import html

REQUIRED_TAGS = {'<body', '</body>'}


def remove_xml_declaration(html_string):
    # 正则表达式匹配 <?xml ...?> 或 <?xml ...>（没有问号结尾的情况）
    pattern = r'<\?xml\s+.*?\??>'
    return re.sub(pattern, '', html_string, flags=re.DOTALL)


def has_essential_tags(html_str):
    """检查是否包含关键标签."""
    lower_html = html_str.lower()
    return all(tag in lower_html for tag in REQUIRED_TAGS)


def select_representative_html(html_strings):
    """从多个HTML字符串中选择最具代表性的一个（仅计算body内内容）"""
    # 存储所有页面的XPath和复杂度信息
    page_data = []
    global_xpaths = set()

    # 第一遍：收集所有页面的XPath和基本复杂度（仅body内）
    for html_dict in html_strings:
        try:
            html_str = remove_xml_declaration(html_dict['html'])
            track_id = html_dict['track_id']

            if not has_essential_tags(html_str):
                continue

            if len(html_str) < 100:
                continue

            # 将字符串转换为文件对象
            file_obj = StringIO(html_str)
            tree = html.parse(file_obj)

            # 找到body元素
            body_element = tree.find('.//body')
            if body_element is None:
                continue

            # 收集body内所有XPath
            page_xpaths = set()
            total_tags = 0
            tag_types = set()
            max_depth = 0
            current_depth = 0
            depth_stack = []
            total_width = 0  # 总标签宽度（所有元素的子元素数量之和）
            max_width = 0  # 最大单个标签宽度
            width_counts = defaultdict(int)  # 各宽度级别的计数

            for element in body_element.iter():
                # 计算当前深度
                if depth_stack and element in depth_stack[-1].getchildren():
                    current_depth += 1
                else:
                    while depth_stack and element not in depth_stack[-1].getchildren():
                        depth_stack.pop()
                        current_depth -= 1
                    if depth_stack:
                        current_depth += 1
                depth_stack.append(element)

                # 更新最大深度
                if current_depth > max_depth:
                    max_depth = current_depth

                # 计算标签宽度（子元素数量）
                children = list(element.getchildren())
                width = len(children)
                total_width += width
                if width > max_width:
                    max_width = width
                # 记录宽度分布
                width_level = min(width, 10)  # 将宽度分组，大于10的算作同一组
                width_counts[width_level] += 1

                xpath = tree.getpath(element)
                page_xpaths.add(xpath)
                total_tags += 1
                tag_types.add(element.tag)

            # 计算宽度多样性（使用熵来衡量）
            width_entropy = 0
            total_elements = sum(width_counts.values())
            if total_elements > 0:
                for count in width_counts.values():
                    probability = count / total_elements
                    if probability > 0:
                        width_entropy -= probability * (probability and math.log(probability, 2))

            # 记录页面数据
            page_data.append({
                'track_id': track_id,
                'xpaths': page_xpaths,
                'tag_count': total_tags,
                'max_depth': max_depth,
                'tag_types': tag_types,
                'tag_diversity': len(tag_types),  # 标签多样性
                'total_width': total_width,  # 总宽度
                'avg_width': total_width / total_tags if total_tags > 0 else 0,  # 平均宽度
                'max_width': max_width,  # 最大宽度
                'width_entropy': width_entropy,  # 宽度分布熵
                'original_data': html_dict,
            })

            # 更新全局XPath集合（仅body内）
            global_xpaths.update(page_xpaths)

        except Exception:
            # import traceback
            # print(f'Error processing HTML: {traceback.format_exc()}')
            continue

    if not page_data:
        return None

    # 第二遍：计算每个页面的代表得分（仅基于body内内容）
    best_score = -1
    best_base_score = -1  # 用于存储最佳基础得分
    representative_html = None

    # 获取最大值用于归一化
    max_depth_all = max(p['max_depth'] for p in page_data) if page_data else 1
    max_tags_all = max(p['tag_count'] for p in page_data) if page_data else 1
    max_diversity_all = max(p['tag_diversity'] for p in page_data) if page_data else 1
    max_avg_width = max(p['avg_width'] for p in page_data) if page_data else 1
    max_max_width = max(p['max_width'] for p in page_data) if page_data else 1
    max_width_entropy = max(p['width_entropy'] for p in page_data) if page_data else 1

    for page in page_data:
        # 计算XPath覆盖率（该页面body包含的全局XPath比例）
        coverage = len(page['xpaths'] & global_xpaths) / len(global_xpaths) if global_xpaths else 0

        # 计算复杂度得分（基于body内标签数量）
        complexity = page['tag_count'] / max_tags_all

        # 计算标签多样性得分
        diversity = page['tag_diversity'] / max_diversity_all

        # 计算深度得分
        depth_score = page['max_depth'] / max_depth_all if max_depth_all > 0 else 0

        # 计算宽度相关得分
        avg_width_score = page['avg_width'] / max_avg_width if max_avg_width > 0 else 0
        max_width_score = page['max_width'] / max_max_width if max_max_width > 0 else 0
        width_entropy_score = page['width_entropy'] / max_width_entropy if max_width_entropy > 0 else 0

        # 计算基础得分（覆盖率和多样性）
        base_score = 0.7 * coverage + 0.3 * diversity

        # 计算结构得分（复杂度、深度和宽度特征）
        structure_score = 0.2 * complexity + 0.1 * depth_score + 0.4 * avg_width_score + 0.3 * max_width_score

        # 计算分布得分（宽度分布的均匀性）
        distribution_score = width_entropy_score

        # 综合得分
        total_score = 0.4 * base_score + 0.3 * structure_score + 0.3 * distribution_score

        # 选择得分最高的页面，如果得分相同则选择基础得分更高的
        if (total_score > best_score) or \
                (total_score == best_score and base_score > best_base_score):
            best_score = total_score
            best_base_score = base_score
            representative_html = page['original_data']

    return representative_html
