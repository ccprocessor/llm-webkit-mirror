<div align="center" xmlns="http://www.w3.org/1999/html">
<!-- logo -->
<p align="center">
  <img src="docs/images/llm-web-kit_logo.jpeg" width="200px" style="vertical-align:middle;">
</p>

<!-- icon -->

[![stars](https://img.shields.io/github/stars/opendatalab/llm-web-kit.svg)](https://github.com/opendatalab/llm-web-kit)
[![forks](https://img.shields.io/github/forks/opendatalab/llm-web-kit.svg)](https://github.com/opendatalab/llm-web-kit)
[![open issues](https://img.shields.io/github/issues-raw/opendatalab/llm-web-kit)](https://github.com/opendatalab/llm-web-kit/issues)
[![issue resolution](https://img.shields.io/github/issues-closed-raw/opendatalab/llm-web-kit)](https://github.com/opendatalab/llm-web-kit/issues)
[![PyPI version](https://badge.fury.io/py/llm-web-kit.svg)](https://badge.fury.io/py/llm-web-kit)
[![codecov](https://codecov.io/gh/ccprocessor/llm-webkit-mirror/graph/badge.svg?token=U4RY0R6JUV)](https://codecov.io/gh/ccprocessor/llm-webkit-mirror)

<!-- language -->

[English](README.md) | [简体中文](README_zh-CN.md)

</div>

# Changelog

- 2024/11/25: Project Initialization

<!-- TABLE OF CONTENT -->

<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#llm-web-kit">llm-web-kit</a>
      <ul>
        <li><a href="#project-introduction">Project Introduction</a></li>
        <li><a href="#key-features">Key Features</a></li>
        <li><a href="#quick-start">Quick Start</a>
            <ul>
            <li><a href="#online-demo">Online Demo</a></li>
            <li><a href="#quick-cpu-demo">Quick CPU Demo</a></li>
            <li><a href="#using-gpu">Using GPU</a></li>
            </ul>
        </li>
        <li><a href="#usage">Usage</a>
            <ul>
            <li><a href="#command-line">Command Line</a></li>
            <li><a href="#api">API</a></li>
            <li><a href="#deploy-derived-projects">Deploy Derived Projects</a></li>
            <li><a href="#development-guide">Development Guide</a></li>
            </ul>
        </li>
      </ul>
    </li>
    <li><a href="#todo">TODO</a></li>
    <li><a href="#known-issues">Known Issues</a></li>
    <li><a href="#faq">FAQ</a></li>
    <li><a href="#contributors">All Thanks To Our Contributors</a></li>
    <li><a href="#license-information">License Information</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#citation">Citation</a></li>
    <li><a href="#star-history">Star History</a></li>
    <li><a href="#links">Links</a></li>
  </ol>
</details>

# llm-web-kit

## Project Introduction

llm-web-kit is a python library that ..

## Key Features

- Remove headers, footers, footnotes, page numbers, etc., to ensure semantic coherence.
- Output text in human-readable order, suitable for single-column, multi-column, and complex layouts.

## Quick Start

![extract_method picture](/docs/images/extract_method.png)

This diagram shows three main HTML content extraction methods:

1. **extract by magic_html+recognize**: Two-stage complete extraction that first uses magic-html to extract main content, then converts it to structured markdown.

2. **only extract by recognize**: Direct content recognition that converts main_html to structured format without main content identification.

3. **only extract main_html by magic-html**: First-stage only extraction that identifies and extracts main content area while preserving HTML structure.

### extract by magic_html+recognize

```python
from llm_web_kit.simple import extract_content_from_html_with_magic_html
from loguru import logger

def extract(url:str, html:str) -> str:
    try:
        nlp_md = extract_content_from_html_with_magic_html(url, html)
        # or mm_nlp_md = extract_content_from_html_with_magic_html(url, html, 'mm_md')
        # or nlp_md = extract_content_from_html_with_magic_html(url, html, language='zh')
        return nlp_md
    except Exception as e:
        logger.exception(e)
    return None

if __name__=="__main__":
    url = ""
    raw_html = '''<html><body>
    <div class="options-div-0-0 option-box__items" style="display: none;">
        <span class="bedroom-rate__title">Room Only Rate</span>
        <span class="bedroom-rate__price">£1,230.00</span>
    </div>
    <p>正常内容</p>
    </body></html>'''
    markdown = extract(url, raw_html)
    print(markdown)
```

### only extract by recognize

```python
from llm_web_kit.simple import extract_content_from_main_html
from loguru import logger

def extract(url:str, raw_html: str, main_html:str) -> str:
    try:
        nlp_md = extract_content_from_main_html(url = url, raw_html = raw_html, main_html = main_html)
        # or mm_nlp_md = extract_content_from_main_html(url = url, raw_html = raw_html, main_html = main_html, 'mm_md')
        # or nlp_md = extract_content_from_main_html(url = url, raw_html = raw_html, main_html = main_html, language='zh')
        return nlp_md
    except Exception as e:
        logger.exception(e)
    return None

if __name__=="__main__":
    url = ""
    raw_html = '''<html>
    <meta charset="utf-8"><meta content="IE=edge" http-equiv="X-UA-Compatible"><meta content="width=device-width,initial-scale=1,shrink-to-fit=no" name="viewport">
    <script>MathJax={tex:{inlineMath:[["$","$"],["\\(","\\)"]],processEscapes:!0},svg:{fontCache:"global"}}</script><script async="" id="MathJax-script" src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-svg.js" type="text/javascript"></script>
    <body>
    <div class="options-div-0-0 option-box__items" style="display: none;">
        <span class="bedroom-rate__title">Room Only Rate</span>
        <span class="bedroom-rate__price">£1,230.00</span>
    </div>
    <p cc-select="true" class="mark-selected" data-anno-uid="anno-uid-wygjielbjln" style="">Are the filtrations after these steps. Why only these? Looking at $\mathcal{F}_1$, we can obtain probabilities for the following events:</p>
    <p>正常内容</p>
    </body></html>'''
    main_html = '''<html><body>
    <div class="options-div-0-0 option-box__items" style="display: none;">
        <span class="bedroom-rate__title">Room Only Rate</span>
        <span class="bedroom-rate__price">£1,230.00</span>
    </div>
    <p cc-select="true" class="mark-selected" data-anno-uid="anno-uid-wygjielbjln" style="">Are the filtrations after these steps. Why only these? Looking at $\mathcal{F}_1$, we can obtain probabilities for the following events:</p>
    <p>正常内容</p>
    </body></html>'''
    markdown = extract(url, raw_html, main_html)
    print(markdown)
```

### only extract main_html by magic-html

```python
from llm_web_kit.simple import extract_main_html_only
from loguru import logger

def extract(url:str, html:str) -> str:
    try:
        main_html = extract_main_html_only(url, html)
        return main_html
    except Exception as e:
        logger.exception(e)
    return None

if __name__=="__main__":
    url = ""
    raw_html = '''<html><body>
    <div class="options-div-0-0 option-box__items" style="display: none;">
        <span class="bedroom-rate__title">Room Only Rate</span>
        <span class="bedroom-rate__price">£1,230.00</span>
    </div>
    <p>正常内容</p>
    </body></html>'''
    main_html = extract(url, raw_html)
    print(main_html)
```

### extract main_html by model response

```python
import traceback
from loguru import logger
from llm_web_kit.main_html_parser.simplify_html.simplify_html import simplify_html
from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.tag_mapping import MapItemToHtmlTagsParser

def extract(response_json: dict, html:str) -> str:
    try:
        _, typical_raw_tag_html, _ = simplify_html(html)
        pre_data = PreDataJson({})
        pre_data[PreDataJsonKey.TYPICAL_RAW_TAG_HTML] = typical_raw_tag_html
        pre_data[PreDataJsonKey.TYPICAL_RAW_HTML] = html
        pre_data['success_label_enable'] = True
        pre_data[PreDataJsonKey.LLM_RESPONSE] = response_json
        parser = MapItemToHtmlTagsParser({})
        pre_data = parser.parse_single(pre_data)
        main_html = pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML]
        is_success = pre_data[PreDataJsonKey.TYPICAL_MAIN_HTML_SUCCESS]
        return main_html, is_success
    except Exception as e:
        logger.exception(e)
    return None

if __name__=="__main__":
    response_json =  {'item_id 1': 0, 'item_id 2': 1, 'item_id 3': 1}
    html = ""
    main_html, is_success = extract(response_json, html)
```

### extract plain text from html source

```python
from llm_web_kit.libs.html_utils import get_plain_text_fast
html_source = ""
text = get_plain_text_fast(html_source)
# language = detect_lang(text)

```

## Pipeline

1. [HTML pre-dedup](jupyter/html-pre-dedup/main.ipynb)
2. [domain clustering](jupyter/domain_clustering/README.md)
3. [layout clustering](jupyter/layout-clustering/main.ipynb)
4. [typical layout node selection](jupyter/typical-html-select/main.ipynb)
5. [HTML node select by LLM](jupyter/html-node-select-llm/main.ipynb)
6. [html parse layout by layout](jupyter/html-parse-by-layout/main.ipynb)

## Usage

# TODO

# Known Issues

# FAQ

# contributors

![contributors](https://contrib.rocks/image?repo=ccprocessor/llm-webkit-mirror)

# License Information

# Acknowledgments

# Citation

# Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ccprocessor/llm-webkit-mirror&type=Date)](https://star-history.com/#ccprocessor/llm-webkit-mirror&Date)

# links
