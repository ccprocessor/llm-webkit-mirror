from io import StringIO

from lxml import html

REQUIRED_TAGS = {'<html', '</html>', '<body', '</body>'}


def has_essential_tags(html_str):
    """检查是否包含关键标签."""
    lower_html = html_str.lower()
    return all(tag in lower_html for tag in REQUIRED_TAGS)


def select_representative_html(html_content_list):
    """从多个HTML文件中选择最具代表性的一个."""
    # 存储所有页面的XPath和复杂度信息
    page_data = []
    global_xpaths = set()

    # 第一遍：收集所有页面的XPath和基本复杂度
    for item in html_content_list:
        try:
            html_str = item['html']
            track_id = item['track_id']

            if not has_essential_tags(html_str):
                continue

            if len(html_str) < 100:
                continue

            file_obj = StringIO(html_str)
            tree = html.parse(file_obj)

            # 收集本页所有XPath
            page_xpaths = set()
            total_tags = 0
            for element in tree.iter():
                xpath = tree.getpath(element)
                page_xpaths.add(xpath)
                total_tags += 1

            # 记录页面数据
            page_data.append({
                'track_id': track_id,
                'xpaths': page_xpaths,
                'tag_count': total_tags,
                'original_data': item,
            })

            # 更新全局XPath集合
            global_xpaths.update(page_xpaths)

        except Exception:
            continue

    if not page_data:
        return None

    # 第二遍：计算每个页面的代表得分
    best_score = -1
    representative_path = None

    for page in page_data:
        # 计算XPath覆盖率（该页面包含的全局XPath比例）
        coverage = len(page['xpaths'] & global_xpaths) / len(global_xpaths)

        # 计算复杂度得分（基于标签数量）
        complexity = page['tag_count'] / max(p['tag_count'] for p in page_data)

        # 综合得分（可根据需要调整权重）
        score = 0.6 * coverage + 0.4 * complexity

        if score > best_score:
            best_score = score
            representative_path = page['original_data']

    return representative_path
