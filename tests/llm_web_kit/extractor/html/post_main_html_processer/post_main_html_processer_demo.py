import time
from pathlib import Path
from typing import Dict, Generator, List, Union

from loguru import logger
from lxml import html

from llm_web_kit.extractor.html.post_main_html_processer.choose_html import \
    select_typical_htmls
from llm_web_kit.extractor.html.post_main_html_processer.post_llm import \
    get_llm_response
from llm_web_kit.extractor.html.post_main_html_processer.post_mapping import \
    mapping_html_by_rules
from llm_web_kit.libs.html_utils import element_to_html, html_to_element


def get_post_html(html_files: List[Union[Path, str]], api_key: str, llm_url: str, model_name: str,
                  choose_html_n: int = 10) -> Generator[Dict, None, None]:
    """对main html进行后处理，旨在清洗html头部和尾部的噪声内容.

    Args:
        html_files: 元素结构为 object or str
        api_key: 模型的api_key
        llm_url: 模型url
        model_name: 模型name
        choose_html_n: 选择choose_html_n个html进行html代表的选择

    Returns:
        迭代器
        {
            "post_llm_response":[{}，{}],  # 模型返回的结果
            "post_llm_spend_time":0,  # 请求模型耗时
            "post_llm_paths":["", "", ""],  # 代表html的path
            "main_html":"<html> ... </html>",   # 原始 main html
            "post_html":"<html> ... </html>",  # 后处理结果 post html
            "post_map_successful":true,  # bool, 后处理是否成功
            "marked_html":"<html> ... </html>"  # 用于测试的标记html，其中红色框中灰度的内容为后处理删除的内容
        }
    """
    if not html_files:
        return
    # 这里随机选择choose_html_n个html
    html_strings = [
        {'html': f.read_text(encoding='utf-8'), 'filename': str(f)}
        for idx, f in enumerate(html_files)
        if idx < choose_html_n
    ]

    post_llm_response = []
    line = {}

    try:
        # 获取典型html
        selected_htmls = select_typical_htmls(html_strings, select_n=3)
        post_llm_paths = [f['filename'] for f in selected_htmls]
        # 获取llm响应
        start_post_llm_time = time.time()
        # is_llm 表示llm request的开关，True，表示请求llm, False，表示使用默认模型response，仅用于测试
        post_llm_response = get_llm_response([f['html'] for f in selected_htmls], api_key, llm_url, model_name,
                                             is_llm=False)
        post_llm_spend_time = int(time.time() - start_post_llm_time)
        line.update({'post_llm_response': post_llm_response, 'post_llm_spend_time': post_llm_spend_time,
                     'post_llm_paths': post_llm_paths})
    except Exception as e:
        logger.error(f'The error is {e}, input path: {html_files}')

    # 进行推广处理
    yield from get_data_to_map(html_files, post_llm_response, line)


def get_data_to_map(html_files: List, post_llm_response: List[dict], line: Dict) -> Generator[dict, None, None]:
    """获取数据进行推广处理.

    Args:
        html_files: 元素结构为 object or str
        post_llm_response: 模型返回的结果
        line: 需要保留的字段字典

    Returns:
        迭代器
        {
            "post_llm_response":[{}，{}],  # 模型返回的结果
            "post_llm_spend_time":0,  # 请求模型耗时
            "post_llm_paths":["", "", ""],  # 代表html的path
            "main_html":"<html> ... </html>",   # 原始 main html
            "post_html":"<html> ... </html>",  # 后处理结果 post html
            "post_map_successful":true,  # bool, 后处理是否成功
            "marked_html":"<html> ... </html>"  # 用于测试的标记html，其中红色框中灰度的内容为后处理删除的内容
        }
    """
    for idx, html_file in enumerate(html_files):
        html_str = html_file.read_text(encoding='utf-8')
        if post_llm_response:
            post_html, post_map_successful = mapping_html_by_rules(html_str, post_llm_response)
        else:
            post_html, post_map_successful = html_str, False
        line['main_html'] = html_str
        line['post_html'] = post_html
        line['post_map_successful'] = post_map_successful

        # 获取对比结果，这里只有测试使用，生产不需要这个内容
        # ------start-----
        xpath_list = [i['xpath'] for i in post_llm_response]
        marker = HTMLMarker(html_str)
        marked_html = marker.process(
            xpath_list,
            # output_html=f'./assets/marked_{idx}.html'  # 标注结果保存地址，默认不保存
        )
        line['marked_html'] = marked_html
        # -----end-----

        # 返回最终结果
        yield line


class HTMLMarker:
    def __init__(self, html_source):
        """初始化HTML标记器.

        Args:
            html_source: HTML内容(字符串)
        """
        self.tree = html_to_element(html_source)

    def __calculate_node_content_ratio(self, tree: html.HtmlElement, node: html.HtmlElement) -> float:
        """计算节点内容占比.

        Args:
            tree(html.HtmlElement): 根节点对象
            node(html.HtmlElement): 节点对象

        Returns:
            float: 节点内容占比
        """
        # 获取节点的文本内容
        text_content = node.text_content()

        total_contents = tree.text_content()
        content_rate = len(text_content) / len(total_contents) if total_contents else 0
        return content_rate

    def __analyze_node_position(self, all_elements: List[html.HtmlElement], target_node: html.HtmlElement) -> str:
        # 计算总节点数
        total_nodes = len(all_elements)

        # 新增逻辑：检查元素是否在<header>或<footer>标签内
        parent = target_node.getparent()
        while parent is not None:
            if parent.tag == 'header':
                return 'start'
            elif parent.tag == 'footer':
                return 'end'
            parent = parent.getparent()

        # 查找当前节点在全部节点中的索引
        node_index = -1
        for idx, element in enumerate(all_elements):
            if element == target_node:
                node_index = idx
                break

        if node_index == -1:
            # 无法定位节点在文档中的位置
            return None

        # 计算位置比例
        position_ratio = (node_index + 1) / total_nodes

        # 判断位置
        if position_ratio < 0.4:
            position = 'start'
        elif position_ratio > 0.7:
            position = 'end'
        else:
            position = 'middle'

        return position

    def __set_child_styles(self, element: html.HtmlElement):
        """递归设置元素及其所有子元素的文本颜色.

        Args:
            element(html.HtmlElement): 当前元素
        """
        # 设置当前元素的文本颜色（如果不是img标签）
        if element.tag.lower() != 'img':
            style = element.get('style', '')
            if 'color:' not in style:  # 避免覆盖已有的颜色设置
                element.set('style', f'{style}; color: #888888;')

        # 特殊处理图片元素
        if element.tag.lower() == 'img':
            style = element.get('style', '')
            element.set('style', f'{style}; filter: grayscale(100%);')

        # 递归处理所有子元素
        for child in element.iterchildren():
            self.__set_child_styles(child)

    def __mark_elements(self, xpath_list: List[str]) -> str:
        """标记XPath对应的元素.

        Args:
            xpath_list: XPath表达式列表

        Returns:
            标记后的html字符串
        """
        # 获取所有元素节点
        all_elements = [element for element in self.tree.iter() if isinstance(element, html.HtmlElement)]

        for xpath in xpath_list:
            try:
                elements = self.tree.xpath(xpath)
                for element in elements:
                    content_rate = self.__calculate_node_content_ratio(self.tree, element)
                    if content_rate > 0.4:
                        continue

                    # 获取节点的位置
                    node_position = self.__analyze_node_position(all_elements, element)
                    if node_position == 'middle':
                        continue

                    # 添加红色边框和灰色内容样式
                    style = element.get('style', '')
                    new_style = f'{style}; border: 2px solid red; color: #888888;'

                    # 特殊处理：对于某些元素可能需要额外样式
                    if element.tag.lower() in ['div', 'section', 'article']:
                        new_style += ' background-color: #f8f8f8;'  # 浅灰背景

                    element.set('style', new_style)
                    self.__set_child_styles(element)

            except Exception:
                continue

        # 返回处理后的HTML
        return element_to_html(self.tree)

    def process(self, xpath_list: List[str], output_html=None) -> str:
        """标记html流程.

        Args:
            xpath_list: XPath表达式列表
            output_html: 可选，保存标记后HTML的路径

        Returns:
            str, 标记后的HTML字符串
        """
        marked_html = self.__mark_elements(xpath_list)

        if output_html:
            Path(output_html).parent.mkdir(parents=True, exist_ok=True)
            with open(output_html, 'w', encoding='utf-8') as f:
                f.write(marked_html)

        return marked_html


if __name__ == '__main__':
    # 同一个layoutid的html path
    base_dir = Path(__file__).parent
    html_files = [base_dir.joinpath(f'assets/html{i}.html') for i in range(3)]

    # 模型参数
    model_name = ''
    api_key = ''
    url = ''
    # 获取后处理结果
    for post_detail in get_post_html(html_files, api_key, url, model_name, choose_html_n=10):
        # 最终结果可写入文件
        pass
