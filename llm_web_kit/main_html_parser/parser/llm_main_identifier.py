import json
import re
from typing import Dict, Tuple

from openai import OpenAI

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.input.pre_data_json import PreDataJson, PreDataJsonKey
from llm_web_kit.main_html_parser.parser.parser import BaseMainHtmlParser


class LlmMainIdentifierParser(BaseMainHtmlParser):
    def __init__(self, model_name: str = None):
        self.model_name = model_name

    def parse(self, pre_data: PreDataJson) -> PreDataJson:
        """结合prompt提示词，对精简后的html网页进行正文内容（即main_html）框定，输出item_id结构的页面判定结果.

        Args:
            pre_data (PreDataJson): 包含精简HTML的PreDataJson对象

        Returns:
            PreDataJson: 包含LLM抽取结果的PreDataJson对象
        """
        resource_config = load_config()['resources']
        if self.model_name in resource_config:
            llm_model_cfg = resource_config[self.model_name]
            api_key = llm_model_cfg['api_key']
            api_url = llm_model_cfg['api_url']
        else:
            pre_data['llm_error'] = f'未找到{self.model_name}对应的大模型配置'
            return pre_data

        simplified_html = pre_data['simplified_html']
        xpath_mapping = pre_data['xpath_mapping']
        llm_result = self.process(api_key, api_url, simplified_html, xpath_mapping)
        pre_data[PreDataJsonKey.LLM_RESPONSE] = llm_result.get('llm_response', {})
        pre_data['llm_error'] = llm_result.get('llm_error', '')
        return pre_data

    def process(
        self,
        api_key: str,
        api_url: str,
        simplified_html: str,
        xpath_mapping: Dict,
    ) -> Dict:
        system_prompt, user_prompt = self.html_to_prompt(simplified_html)
        response_str = self.chat_with_model(
            api_key, api_url, system_prompt, user_prompt
        )
        llm_result = self.check_model_response(response_str, xpath_mapping)
        return llm_result

    def html_to_prompt(self, simplified_html: str) -> Tuple[str, str]:
        system_prompt = """
你是一位网页正文抽取专家，你能阅读HTML的每个带有item_id的节点，联系前后节点内容，判断每个节点里的文字是否围绕着某个正文主题，并进一步判断该节点是否是该页面的主要内容还是其他内容。
具有以下特征的元素通常是主要内容：
  - 对于新闻，博客，文章，信息发布类网页，正文，正文中的配图，正文中需要被发布的信息属于主要内容，
  - 对于论坛，论坛的每一层，以及每一层的回复属于主要内容，
  - 对于问答类网站，问题和回答，以及针对问题的回复与每一个回答的回复等元素通常是主要内容。
  - 对于列表页，列表的每一项及其描述为主要内容。
  - 对于商品页，商品图片、描述、价格、库存等属于主要内容。
具有以下特征的元素通常是补充信息：
  - 导航栏、侧边栏、页脚，相关文章，导航链接列表等元素通常属于其它信息。
  - 文章标题、正文的编者信息，评论内容的用户信息，点赞数，发布时间等元素通常是补充信息。注意，评论内容本身属于主要内容。

请针对每一个具有"_item_id"属性的元素，判断该元素的功能，并给出该元素是否是该页面的主要内容，补充信息，其他内容。
如果是主要内容，你可以将元素记为1，如果是其他内容，你可以将元素记为0。

以下会提供一个经过简化的网页HTML代码，你需要判断出具有"_item_id"属性所在位置的元素的功能，并给出该元素是否是该页面的主要内容或是其他内容。
回答的格式例如：
{
    "item_id 1": 0,
    "item_id 2": 1,
    "item_id 3": 0
}"""
        user_prompt = f"""以下是HTML代码：
    ```html
    {simplified_html}
    ```
    注意不要输出解释性内容，json里也不要有注释"""
        return system_prompt, user_prompt

    def chat_with_model(
        self, api_key: str, api_url: str, system_prompt: str, user_prompt: str
    ) -> str:
        client = OpenAI(
            api_key=api_key,
            base_url=api_url,
        )
        completion = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
        )

        response_str = completion.model_dump_json()
        return response_str

    def parse_json_smartly(self, response_str: str) -> Dict:
        # match "{" and "}" greedily and use the first match
        try:
            json_str = re.search(r'\{.*\}', response_str, re.DOTALL).group()
            result_dict = json.loads(json_str)
        except Exception:
            result_dict = {'ERROR_RESULT': response_str}
        return result_dict

    def check_model_response(
        self, response_str: str, xpath_mapping: Dict
    ) -> Dict[str, str]:
        try:
            response_json = json.loads(response_str)
            response_content = response_json['choices'][0]['message']['content']
        except Exception:
            return {'llm_error': f'llm响应失败:{response_str}'}

        response = self.parse_json_smartly(response_content)
        if 'ERROR_RESULT' in response:
            return {'llm_error': f'response解析失败:{response_content}'}

        response_key = sorted([''.join(re.findall(r'\d', item)) for item in response])
        xpath_key = sorted(list(xpath_mapping.keys()))
        if response_key == xpath_key:
            return {'llm_response': response}
        return {'llm_error': 'response与item_id不能一一对应', 'llm_response': response}


if __name__ == '__main__':
    llm_id = LlmMainIdentifierParser('Qwen2.5-72b')
    html_str = "<html> <body> <div _item_id='1'>菜单 首页</div> <div _item_id='2'>文章标题</div> <div _item_id='3'>文章内容</div> </body> </html>"
    xpath_mapping = {'1': {'//div'}, '2': {'//div'}, '3': {'//div'}}
    d = {'simplified_html': html_str, 'xpath_mapping': xpath_mapping}
    labeled_d = llm_id.parse(d)
    print(labeled_d)
    print(labeled_d['llm_error'])
