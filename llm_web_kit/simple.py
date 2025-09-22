"""predefined simple user functions."""

import threading
import uuid
from datetime import datetime

from llm_web_kit.config.cfg_reader import load_pipe_tpl
from llm_web_kit.exception.exception import InvalidOutputFormatException
from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
from llm_web_kit.input.datajson import DataJson


class PipeTpl:
    # 只执行第一阶段：选择main_html
    MAGIC_HTML = 'magic_html'  # 输入html，输出main_html（magic_html）
    LLM = 'llm_html'  # 输入html，输出main_html（llm）
    LAYOUT_BATCH = 'layout_batch_html'  # 输入html，输出main_html（layout_batch）
    # 只执行第二阶段：html抽取为md
    NOCLIP = 'noclip_html'  # 输入main_html，输出markdown
    # 执行两个阶段：选择main_html，html抽取为md
    MAGIC_HTML_NOCLIP = 'magic_html_noclip_html'  # 输入html，输出markdown（magic_html）
    LLM_NOCLIP = 'llm_noclip_html'  # 输入html，输出markdown（llm）
    LAYOUT_BATCH_NOCLIP = 'layout_batch_noclip_html'  # 输入html，输出markdown（layout_batch）


class ExtractorFactory:
    """线程安全的提取器工厂."""

    # 提取器缓存
    _extractors = {}
    # 线程锁，保证多线程安全
    _lock = threading.Lock()

    @staticmethod
    def get_extractor(pipe_tpl_name: str):
        """获取指定类型的提取器（带缓存，线程安全）

        Args:
            pipe_tpl_name: 管道模板名称，对应 PipeTpl 中的常量

        Returns:
            提取器链实例
        """
        # 双重检查锁定模式，避免不必要的锁竞争
        if pipe_tpl_name not in ExtractorFactory._extractors:
            with ExtractorFactory._lock:
                # 再次检查，防止在获取锁期间其他线程已经创建了实例
                if pipe_tpl_name not in ExtractorFactory._extractors:
                    extractor_cfg = load_pipe_tpl(pipe_tpl_name)
                    chain = ExtractSimpleFactory.create(extractor_cfg)
                    ExtractorFactory._extractors[pipe_tpl_name] = chain

        return ExtractorFactory._extractors[pipe_tpl_name]


def _extract_html(url: str, html_content: str, pipe_tpl: str, language: str = 'en') -> DataJson:
    """内部使用的统一HTML提取方法，返回处理后的DataJson对象.

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
        language: 语言，可选：'en' 或 'zh'

    Returns:
        DataJson: 处理后的DataJson对象，包含main_html和content_list等信息
    """
    extractor = ExtractorFactory.get_extractor(pipe_tpl)

    input_data_dict = {
        'track_id': str(uuid.uuid4()),
        'url': url,
        'html': html_content,
        'dataset_name': f'llm-web-kit-{pipe_tpl}',
        'data_source_category': 'HTML',
        'file_bytes': len(html_content),
        'language': language,
        'meta_info': {'input_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    }

    d = DataJson(input_data_dict)
    return extractor.extract(d)


# ========================================
# SDK方法（三种使用场景）
# ========================================

def extract_main_html_only(url: str, html_content: str, parser_type: str = PipeTpl.MAGIC_HTML,
                           language: str = 'en') -> str:
    """场景1: 只执行第一阶段，抽取main_html.

    Args:
        url: 网页URL
        html_content: 原始HTML内容
        parser_type: 解析器类型，可选：PipeTpl.MAGIC_HTML, PipeTpl.LLM, PipeTpl.LAYOUT_BATCH
        language: 语言，可选：'en' 或 'zh'

    Returns:
        str: 提取的主要HTML内容
    """
    result = _extract_html(url, html_content, parser_type, language)
    return result.get('main_html', '')


def extract_content_from_main_html(url: str, main_html: str, output_format: str = 'md', language: str = 'en', use_raw_image_url: bool = False) -> str:
    """场景2: 只执行第二阶段，从main_html抽取结构化内容.

    Args:
        url: 网页URL
        main_html: 已经抽取的主要HTML内容
        output_format: 输出格式，'md' 或 'mm_md' 或 'plain_md'
        language: 语言，可选：'en' 或 'zh'
        use_raw_image_url: 是否使用原始图片URL（仅对mm_md格式有效）

    Returns:
        str: 结构化的内容（markdown格式）
    """
    result = _extract_html(url, main_html, PipeTpl.NOCLIP, language)
    content_list = result.get_content_list()

    if output_format == 'md':
        return content_list.to_nlp_md()
    elif output_format == 'mm_md':
        return content_list.to_mm_md(use_raw_image_url=use_raw_image_url)
    elif output_format == 'plain_md':
        return content_list.to_plain_md()
    elif output_format == 'json':
        return result.to_json()
    else:
        raise InvalidOutputFormatException(f'Invalid output format: {output_format}')


def extract_content_from_html_with_magic_html(url: str, html_content: str, output_format: str = 'md',
                                              language: str = 'en', use_raw_image_url: bool = False) -> str:
    """场景3: 执行两个阶段，从magic_html抽取main_html，再从main_html抽取结构化内容.

    Args:
        url: 网页URL
        html_content: 原始HTML内容
        output_format: 输出格式，'md' 或 'mm_md' 或 'plain_md'
        language: 语言，可选：'en' 或 'zh'
        use_raw_image_url: 是否使用原始图片URL（仅对mm_md格式有效）

    Returns:
        str: 结构化的内容（markdown格式）
    """
    result = _extract_html(url, html_content, PipeTpl.MAGIC_HTML_NOCLIP, language)
    content_list = result.get_content_list()

    if output_format == 'md':
        return content_list.to_nlp_md()
    elif output_format == 'mm_md':
        return content_list.to_mm_md(use_raw_image_url=use_raw_image_url)
    elif output_format == 'plain_md':
        return content_list.to_plain_md()
    elif output_format == 'json':
        return result.to_json()
    else:
        raise InvalidOutputFormatException(f'Invalid output format: {output_format}')


def extract_content_from_html_with_llm(url: str, html_content: str, output_format: str = 'md',
                                       language: str = 'en', use_raw_image_url: bool = False) -> str:
    """场景3: 执行两个阶段，从llm抽取main_html，再从main_html抽取结构化内容.

    Args:
        url: 网页URL
        html_content: 原始HTML内容
        output_format: 输出格式，'md' 或 'mm_md' 或 'plain_md'
        language: 语言，可选：'en' 或 'zh'
        use_raw_image_url: 是否使用原始图片URL（仅对mm_md格式有效）

    Returns:
        str: 结构化的内容（markdown格式）
    """
    result = _extract_html(url, html_content, PipeTpl.LLM_NOCLIP, language)
    content_list = result.get_content_list()

    if output_format == 'md':
        return content_list.to_nlp_md()
    elif output_format == 'mm_md':
        return content_list.to_mm_md(use_raw_image_url=use_raw_image_url)
    elif output_format == 'plain_md':
        return content_list.to_plain_md()
    elif output_format == 'json':
        return result.to_json()
    else:
        raise InvalidOutputFormatException(f'Invalid output format: {output_format}')


def extract_content_from_html_with_layout_batch(url: str, html_content: str, output_format: str = 'md',
                                                language: str = 'en', use_raw_image_url: bool = False) -> str:
    """场景3: 执行两个阶段，从layout_batch抽取main_html，再从main_html抽取结构化内容.

    Args:
        url: 网页URL
        html_content: 原始HTML内容
        output_format: 输出格式，'md' 或 'mm_md' 或 'plain_md'
        language: 语言，可选：'en' 或 'zh'
        use_raw_image_url: 是否使用原始图片URL（仅对mm_md格式有效）

    Returns:
        str: 结构化的内容（markdown格式）
    """
    result = _extract_html(url, html_content, PipeTpl.LAYOUT_BATCH_NOCLIP, language)
    content_list = result.get_content_list()

    if output_format == 'md':
        return content_list.to_nlp_md()
    elif output_format == 'mm_md':
        return content_list.to_mm_md(use_raw_image_url=use_raw_image_url)
    elif output_format == 'plain_md':
        return content_list.to_plain_md()
    elif output_format == 'json':
        return result.to_json()
    else:
        raise InvalidOutputFormatException(f'Invalid output format: {output_format}')
