import os

import pytest

from llm_web_kit.pipeline.extractor.html.magic_html import GeneralExtractor


def test_general_extractor():
    """Test GeneralExtractor."""
    general_extractor = GeneralExtractor(
        custom_rule_path=f'{os.path.dirname(os.path.abspath(__file__))}/assets/custom_config.json')

    # custom
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/custom.html', 'r', encoding='utf-8') as f:
        html = f.read()
        general_extractor.extract(html, base_url='http://test.custom.com')

    # xp1-5
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/xp1_5.html', 'r', encoding='utf-8') as f:
        html = f.read()
        general_extractor.extract(html, base_url='http://test.com')

    # others
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/others.html', 'r', encoding='utf-8') as f:
        html = f.read()
        general_extractor.extract(html, base_url='http://test.com')

    # weixin
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/weixin.html', 'r', encoding='utf-8') as f:
        html = f.read()
        general_extractor.extract(html, base_url='https://mp.weixin.qq.com', html_type='weixin')

    # forum
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/forum.html', 'r', encoding='utf-8') as f:
        html = f.read()
        general_extractor.extract(html, base_url='http://test.com', html_type='forum')

    # precision
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/forum.html', 'r', encoding='utf-8') as f:
        html = f.read()
        general_extractor.extract(html, base_url='http://test.com', html_type='forum', precision=False)


def main():
    test_general_extractor()


pytest.main()
