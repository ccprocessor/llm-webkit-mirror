"""predefined simple user functions."""

import uuid
from datetime import datetime

from llm_web_kit.config.cfg_reader import load_pipe_tpl
from llm_web_kit.extractor.extractor_chain import ExtractSimpleFactory
from llm_web_kit.input.datajson import DataJson


class PipeType:
    HTML = 'html'
    NOCLIP = 'noclip_html'


class ExtractorType:
    HTML = 'html'
    PDF = 'pdf'
    EBOOK = 'ebook'


class ExtractorFactory:
    """factory class for extractor."""
    magic_html_extractor = None
    noclip_html_extractor = None
    pdf_extractor = None
    ebook_extractor = None

    @staticmethod
    def get_extractor(extractor_type: str, pipe_tpl_name: str):
        if extractor_type == ExtractorType.HTML:
            if pipe_tpl_name == PipeType.HTML:
                if ExtractorFactory.magic_html_extractor is None:
                    extractor_cfg = load_pipe_tpl(pipe_tpl_name)
                    chain = ExtractSimpleFactory.create(extractor_cfg)
                    ExtractorFactory.magic_html_extractor = chain
                return ExtractorFactory.magic_html_extractor
            if pipe_tpl_name == PipeType.NOCLIP:
                if ExtractorFactory.noclip_html_extractor is None:
                    extractor_cfg = load_pipe_tpl(pipe_tpl_name)
                    chain = ExtractSimpleFactory.create(extractor_cfg)
                    ExtractorFactory.noclip_html_extractor = chain
                return ExtractorFactory.noclip_html_extractor
        else:
            raise ValueError(f'Invalid extractor type: {extractor_type}')


def __extract_main_html_by_no_clip_html(url:str, html_content: str, raw_html:str) -> DataJson:
    extractor = ExtractorFactory.get_extractor(ExtractorType.HTML, PipeType.NOCLIP)
    if raw_html == '':
        raw_html = html_content
    input_data_dict = {
        'track_id': str(uuid.uuid4()),
        'url': url,
        'html': raw_html,
        'main_html': html_content,
        'dataset_name': 'llm-web-kit-pure-quickstart',
        'data_source_category': 'HTML',
        'file_bytes': len(html_content),
        'meta_info': {'input_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    }
    d = DataJson(input_data_dict)
    result = extractor.extract(d)
    return result


def __extract_html(url:str, html_content: str) -> DataJson:
    extractor = ExtractorFactory.get_extractor(ExtractorType.HTML, PipeType.HTML)
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


def extract_html_to_md(url:str, html_content: str, clip_html=True, raw_html='') -> str:
    """extract html to markdown without images."""
    if clip_html:
        result = __extract_html(url, html_content)
    else:
        result = __extract_main_html_by_no_clip_html(url, html_content, raw_html)
    return result.get_content_list().to_nlp_md()


def extract_html_to_mm_md(url:str, html_content: str, clip_html=True, raw_html='') -> str:
    """extract html to markdown with images."""
    if clip_html:
        result = __extract_html(url, html_content)
    else:
        result = __extract_main_html_by_no_clip_html(url, html_content, raw_html)
    return result.get_content_list().to_mm_md()


def extract_main_html(url:str, html_content: str, clip_html=True, raw_html='') -> str:
    if clip_html:
        result = __extract_html(url, html_content)
    else:
        result = __extract_main_html_by_no_clip_html(url, html_content, raw_html)
    main_html = result.get('main_html')
    return main_html
