import re
from pathlib import Path
from typing import List

from llm_web_kit.libs.standard_utils import json_loads

base_dir = Path(__file__).parent


def __get_eg_data():
    eg_input_lst = []
    for i in range(3):
        eg_input_lst.append(base_dir.joinpath(f'assets/html{i}.html').read_text(encoding='utf-8'))

    eg_output = json_loads(base_dir.joinpath('assets/rule.json').read_text(encoding='utf-8'))
    return eg_input_lst, eg_output


output_format = '''[
    {
        "xpath": "XPath of the node of the non-core content body",
        "parent_tag": "The label name of the parent node of the node that is not the core content body",
        "parent_attributes": "The class and id attributes of the parent node of the node that is not the core content body",
        "reson": "Reasons for determining it as non-core content"
    }
]'''


def clean_json_data(md_text: str) -> dict:
    cleaned = re.sub(r'^```json|\```', '', md_text, flags=re.MULTILINE)
    try:
        json_data = json_loads(cleaned)
    except Exception:
        return None
    return json_data


def request_model(input_lst: List, api_key: str, url: str, model_name: str) -> str:
    from openai import OpenAI

    html_count = len(input_lst)
    eg_input_lst, eg_output = __get_eg_data()

    prompt = f"""
You are an expert in HTML semantics and will be assigned the following task:
Accept input:{input_lst}containing{html_count}HTML pages.
The input has the following characteristics:
1. These{html_count}HTML pages are from the same website.
2. These{html_count}pages use the same template, differing only in their main content.
################
The tasks you need to complete are:
Deeply understand the{html_count}HTML input and find the node information and node paths for the non-core content at the page header (top section) and page footer (bottom section) of the {html_count} HTML.
################
You need to follow the following rules when completing the task:
1. Identify and extract non-core content modules located in the page header (top section) and page footer (bottom section) of the HTML body. Do not identify the main title as non-core content. Non-core content includes breadcrumb navigation, related article links, advertisements, page turning, sharing, recommended content, etc.
2. If non-core content appears in the middle of the HTML, such as the time and author in a forum reply, it can be ignored.
3. If a node contains non-core content main nodes and core content main nodes, its internal elements need to be further analyzed; if a node is a wrapper for the entire page content or a container node containing multiple child elements, its internal elements need to be further analyzed.
4. Tables have semantic ambiguity. When analyzing table nodes, we need to consider the following: if they present structured data (such as product tables or data reports), they are classified as core content. If they are used for layout or display of simple lists (such as navigation menus or link lists), there are two cases: if it is a complete table structure, mark the entire table as non-core content. If it is an incomplete table structure or complex nesting, further analysis of its internal elements is required.
5. Non-core content should be carefully analyzed to prevent misjudgment. Uncertain elements should be excluded from non-core content.
6. It is necessary to consider the location of the HTML node of the non-core content body and the commonality of semantics in the web page.
7. When considering node paths, semantics should be prioritized. Avoid using indexes in node paths. Attribute values should be correct, especially those composed of multiple values. All attributes should be correctly matched.
8. Use '//' and '/' correctly when considering node paths. '//' is used for recursive searches, while '/' is used to locate direct children.
9. When considering node paths, always use the element's original tag name in the HTML source code.
10. Each node of the final non-core content body must have only one type of content, and the content of this node must be determined to be all non-core content bodies, without inclusion relationships or uncertain factors.
################
The return data needs to follow the following rules:
1. Both node attributes and parent node attributes only consider the id attribute and class attribute. If both the id attribute and the class attribute are empty, they are ignored.
2. The returned node path must be unique and no duplicates are allowed.
3. The result is returned in JSON array format, requiring all strings to be enclosed in double quotes and not containing any additional information. The output format is as follows:
{output_format}
################
Here are some examples for your reference:
<example-1>
input:{eg_input_lst}
return:{eg_output}
<end-example-1>
################
Now return your result:"""

    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key='sk-xxx',
        api_key=api_key,
        base_url=url,
    )

    completion = client.chat.completions.create(
        model=model_name,
        # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        extra_body={'enable_thinking': False},
        messages=[
            {'role': 'system', 'content': 'You are a HTML semantics expert.'},
            {'role': 'user', 'content': prompt}

        ],
    )

    rtn = completion.model_dump_json()
    return rtn


def get_llm_response(input_lst: List, api_key: str, url: str, model_name: str, is_llm: bool = True,
                     max_retry: int = 3) -> dict:
    from openai import BadRequestError

    if not is_llm:
        post_llm_response = base_dir.joinpath('assets/llm_res.json').read_text(encoding='utf-8')
        return json_loads(post_llm_response)

    try:
        rtn = request_model(input_lst, api_key, url, model_name)
        rtn_detail = json_loads(rtn)
        post_llm_response = rtn_detail.get('choices', [])[0].get('message', {}).get('content', '')
        return clean_json_data(post_llm_response)
    except BadRequestError as e:
        if 'Range of input length should be' in str(e):
            if len(input_lst) > 1 and max_retry > 0:
                return get_llm_response(input_lst[:len(input_lst) - 1], api_key, url, model_name, is_llm, max_retry - 1)
        return None
    except Exception:
        if max_retry > 0:
            return get_llm_response(input_lst, api_key, url, model_name, is_llm, max_retry - 1)
        else:
            return None
