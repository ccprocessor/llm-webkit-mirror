"""predefined simple user functions."""

import uuid
from datetime import datetime

from llm_web_kit.config.cfg_reader import load_pipe_tpl
from llm_web_kit.exception.exception import InvalidOutputFormatException
from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
from llm_web_kit.input.datajson import DataJson


class PipeTpl:
    # 只执行第一阶段：选择main_html
    MAGIC_HTML = 'magic_html'
    LLM = 'llm_html'
    LAYOUT_BATCH = 'layout_batch_html'
    # 只执行第二阶段：html抽取为md
    NOCLIP = 'noclip_html'
    # 执行两个阶段：选择main_html，html抽取为md
    MAGIC_HTML_NOCLIP = 'magic_html_noclip_html'
    LLM_NOCLIP = 'llm_noclip_html'
    LAYOUT_BATCH_NOCLIP = 'layout_batch_noclip_html'


class ExtractorFactory:

    # 提取器缓存
    _extractors = {}

    @staticmethod
    def get_extractor(pipe_tpl_name: str):
        """获取指定类型的提取器（带缓存）

        Args:
            pipe_tpl_name: 管道模板名称，对应 PipeTpl 中的常量

        Returns:
            提取器链实例
        """
        if pipe_tpl_name not in ExtractorFactory._extractors:
            extractor_cfg = load_pipe_tpl(pipe_tpl_name)
            chain = ExtractSimpleFactory.create(extractor_cfg)
            ExtractorFactory._extractors[pipe_tpl_name] = chain

        return ExtractorFactory._extractors[pipe_tpl_name]


def extract_html(url: str, html_content: str, pipe_tpl: str, output_format: str = 'md') -> str:
    """统一的HTML提取方法，支持7种场景.

    Args:
        url: 网页URL
        html_content: 原始HTML内容（或main_html，取决于pipe_tpl）
        pipe_tpl: 处理类型，支持：
            # 只执行第一阶段：
            - PipeTpl.MAGIC_HTML: 使用magic_html提取main_html
            - PipeTpl.LLM: 使用LLM提取main_html
            - PipeTpl.LAYOUT_BATCH: 使用layout_batch提取main_html
            # 只执行第二阶段：
            - PipeTpl.NOCLIP: 从main_html转换为markdown
            # 执行两个阶段：
            - PipeTpl.MAGIC_HTML_NOCLIP: magic_html + markdown转换
            - PipeTpl.LLM_NOCLIP: LLM + markdown转换
            - PipeTpl.LAYOUT_BATCH_NOCLIP: layout_batch + markdown转换
        output_format: 输出格式，'md' 或 'mm_md'（仅当有第二阶段时有效）

    Returns:
        str: 根据pipe_tpl返回main_html或markdown内容
    """
    extractor = ExtractorFactory.get_extractor(pipe_tpl)

    input_data_dict = {
        'track_id': str(uuid.uuid4()),
        'url': url,
        'html': html_content,
        'dataset_name': f'llm-web-kit-{pipe_tpl}',
        'data_source_category': 'HTML',
        'file_bytes': len(html_content),
        'meta_info': {'input_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    }

    # 对于只执行第二阶段的场景，html_content实际是main_html
    if pipe_tpl == PipeTpl.NOCLIP:
        input_data_dict['main_html'] = html_content

    d = DataJson(input_data_dict)
    result = extractor.extract(d)

    # 根据pipe_tpl决定返回内容
    is_stage1_only = pipe_tpl in [PipeTpl.MAGIC_HTML, PipeTpl.LLM, PipeTpl.LAYOUT_BATCH]

    if is_stage1_only:
        # 只执行第一阶段，返回main_html
        return result.get('main_html', '')
    else:
        # 执行了第二阶段，返回markdown
        content_list = result.get_content_list()
        if output_format == 'mm_md':
            return content_list.to_mm_md()
        elif output_format == 'md':
            return content_list.to_nlp_md()
        elif output_format == 'json':
            return result.to_json()
        else:
            raise InvalidOutputFormatException(f'Invalid output format: {output_format}')


# ========================================
# 便利方法（三种使用场景）
# ========================================

def extract_main_html_only(url: str, html_content: str, parser_type: str = PipeTpl.MAGIC_HTML) -> str:
    """场景1: 只执行第一阶段，抽取main_html.

    Args:
        url: 网页URL
        html_content: 原始HTML内容
        parser_type: 解析器类型，可选：PipeTpl.MAGIC_HTML, PipeTpl.LLM, PipeTpl.LAYOUT_BATCH

    Returns:
        str: 提取的主要HTML内容
    """
    return extract_html(url, html_content, parser_type)


def extract_content_from_main_html(url: str, main_html: str, output_format: str = 'md') -> str:
    """场景2: 只执行第二阶段，从main_html抽取结构化内容.

    Args:
        url: 网页URL
        main_html: 已经抽取的主要HTML内容
        output_format: 输出格式，'md' 或 'mm_md'

    Returns:
        str: 结构化的内容（markdown格式）
    """
    return extract_html(url, main_html, PipeTpl.NOCLIP, output_format)


def extract_content_from_html_with_magic_html(url: str, html_content: str, output_format: str = 'md') -> str:
    """场景3: 执行两个阶段，从magic_html抽取main_html，再从main_html抽取结构化内容.

    Args:
        url: 网页URL
        main_html: 已经抽取的主要HTML内容
        output_format: 输出格式，'md' 或 'mm_md'

    Returns:
        str: 结构化的内容（markdown格式）
    """
    return extract_html(url, html_content, PipeTpl.MAGIC_HTML_NOCLIP, output_format)


def extract_content_from_html_with_llm(url: str, html_content: str, output_format: str = 'md') -> str:
    """场景3: 执行两个阶段，从llm抽取main_html，再从main_html抽取结构化内容.

    Args:
        url: 网页URL
        main_html: 已经抽取的主要HTML内容
        output_format: 输出格式，'md' 或 'mm_md'

    Returns:
        str: 结构化的内容（markdown格式）
    """
    return extract_html(url, html_content, PipeTpl.LLM_NOCLIP, output_format)


def extract_content_from_html_with_layout_batch(url: str, html_content: str, output_format: str = 'md') -> str:
    """场景3: 执行两个阶段，从layout_batch抽取main_html，再从main_html抽取结构化内容.

    Args:
        url: 网页URL
        main_html: 已经抽取的主要HTML内容
        output_format: 输出格式，'md' 或 'mm_md'

    Returns:
        str: 结构化的内容（markdown格式）
    """
    return extract_html(url, html_content, PipeTpl.LAYOUT_BATCH_NOCLIP, output_format)
