"""predefined simple user functions."""

import uuid
from datetime import datetime

from llm_web_kit.config.cfg_reader import load_pipe_tpl
from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
from llm_web_kit.extractor.html.extractor import (
    HTMLPageLayoutType, MagicHTMLFIleFormatorExtractor,
    NoClipHTMLFIleFormatorExtractor)
from llm_web_kit.input.datajson import DataJson


class ExtractorType:
    HTML = 'html'
    PDF = 'pdf'
    EBOOK = 'ebook'


class ExtractorFactory:
    """factory class for extractor."""
    html_extractor = None
    pdf_extractor = None
    ebook_extractor = None

    @staticmethod
    def get_extractor(extractor_type: str):
        if extractor_type == ExtractorType.HTML:
            if ExtractorFactory.html_extractor is None:
                extractor_cfg = load_pipe_tpl('html')
                chain = ExtractSimpleFactory.create(extractor_cfg)
                ExtractorFactory.html_extractor = chain
            return ExtractorFactory.html_extractor
        else:
            raise ValueError(f'Invalid extractor type: {extractor_type}')


def __extract_main_html_by_no_clip_html(url:str, html_content: str) -> DataJson:
    extractor = NoClipHTMLFIleFormatorExtractor(load_pipe_tpl('noclip_html'))
    input_data_dict = {
        'track_id': str(uuid.uuid4()),
        'url': url,
        'html': html_content,
        'main_html': html_content,
        'dataset_name': 'llm-web-kit-pure-quickstart',
        'data_source_category': 'HTML',
        'file_bytes': len(html_content),
        'meta_info': {'input_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    }
    d = DataJson(input_data_dict)
    result = extractor.extract(d)
    return result


def __extract_main_html_by_maigic_html(url:str, html_str: str, page_layout_type:str) -> DataJson:
    magic_html_extractor = MagicHTMLFIleFormatorExtractor(load_pipe_tpl('html'))
    main_html, method, title = magic_html_extractor._extract_main_html(html_str, url, page_layout_type)
    return main_html, title


def __extract_html(url:str, html_content: str) -> DataJson:
    extractor = ExtractorFactory.get_extractor(ExtractorType.HTML)
    input_data_dict = {
        'track_id': str(uuid.uuid4()),
        'url': url,
        'html': html_content,
        'dataset_name': 'llm-web-kit-quickstart',
        'data_source_category': 'HTML',
        'file_bytes': len(html_content),
        'meta_info': {'input_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    }
    d = DataJson(input_data_dict)
    result = extractor.extract(d)
    return result


def extract_html_to_md(url:str, html_content: str, clip_html=True) -> str:
    """extract html to markdown without images."""
    if clip_html:
        result = __extract_html(url, html_content)
    else:
        result = __extract_main_html_by_no_clip_html(url, html_content)
    return result.get_content_list().to_nlp_md()


def extract_html_to_mm_md(url:str, html_content: str, clip_html=True) -> str:
    """extract html to markdown with images."""
    if clip_html:
        result = __extract_html(url, html_content)
    else:
        result = __extract_main_html_by_no_clip_html(url, html_content)
    return result.get_content_list().to_mm_md()


def extract_main_html_by_maigic_html(url:str, html_str: str, page_layout_type:str = HTMLPageLayoutType.LAYOUT_ARTICLE) -> str:
    """extract main html."""
    result = __extract_main_html_by_maigic_html(url, html_str, page_layout_type)
    return result[0], result[1]
