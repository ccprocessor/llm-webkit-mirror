from loguru import logger
from openai import BadRequestError, OpenAI

from llm_web_kit.libs.standard_utils import json_loads

html_str = """<html lang="en-GB" dir="ltr" _item_id="1">
<body class="gantry site com_content view-article no-layout no-task dir-ltr itemid-118 outline-141 g-offcanvas-left g-home-positions g-style-preset1"
      _item_id="2">
<div id="g-page-surround" _item_id="3">
    <section id="g-utility" _item_id="4">
        <div class="g-grid" _item_id="5">
            <div class="g-block size-100" _item_id="6">
                <div class="g-content" _item_id="7">
                    <div class="platform-content row-fluid" _item_id="8">
                        <div class="span12" _item_id="9">
                            <div class="item-page" itemscope itemtype="https://schema.org/Article" _item_id="10">
                                <div itemprop="articleBody" _item_id="11">
                                    <p _item_id="12">All right... We have returned from Romania again! It was a pleasure
                                        to slash you
                                        with quality metal once again. Thanks to <b _item_id="13">Manu</b>, the
                                        beginning of the
                                        performance at <b _item_id="14">TATTOO &amp; MUSIC FEST II</b> in Iasi could be
                                        seen below...
                                        <br _item_id="15">
                                        Thanks to all, who managed to attend the events, meet us and help us on the way!
                                        You know who you are! <br _item_id="16">
                                        Stay tuned! News coming soon...</p>

                                    <p _item_id="17"><img src="/home/images/posters/06.08.2011.jpg" alt="" width="340"
                                                          _item_id="18"></p>
                                </div>

                                <ul class="pager pagenav" _item_id="19">
                                    <li class="previous" _item_id="20">
                                        <a class="hasTooltip" title="Metal In Your Face"
                                           aria-label="Previous article: Metal In Your Face"
                                           href="/home/index.php/news/36-metal-in-your-face.html" rel="prev"
                                           _item_id="21">
                                            <span class="icon-chevron-left" aria-hidden="true" _item_id="22"></span>
                                            <span aria-hidden="true" _item_id="23">Prev</span>
                                        </a>
                                    </li>

                                    <li class="next" _item_id="24">
                                        <a class="hasTooltip" title="Romania, Vengeance is Near!"
                                           aria-label="Next article: Romania, Vengeance is Near!"
                                           href="/home/index.php/news/38-romania-vengeance-is-near.html" rel="next"
                                           _item_id="25">
                                            <span aria-hidden="true" _item_id="26">Next</span>
                                            <span class="icon-chevron-right" aria-hidden="true" _item_id="27"></span>
                                        </a>
                                    </li>

                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</div>
</body>
</html>"""

promtp = f"""你是文本识别专家，输入一个html字符串，且每个标签都有一个属性值不同的属性_item_id，你通过识别html能够解析出每个_item_id对应的内容是否是主体内容，主要在于去除以下两部分的内容：
1.去除头部导航栏、时间、作者、广告、推荐等非正文主体内容；
2.去除尾部链接、分享、翻页、广告、推荐等非正文主体内容。
注意，主体内容链接保留
识别出主体内容之后根据_item_id生成字典作为返回结果，无需解释生成依据，其中0代表非主体内容需要去除，1代表是主体内容要保留。示例如下：
输入: {html_str}
返回结果: {{'item_id 1': 1, 'item_id 2': 1, 'item_id 3': 1, 'item_id 4': 1, 'item_id 5': 1, 'item_id 6': 1, 'item_id 7': 1, 'item_id 8': 1, 'item_id 9': 1, 'item_id 10': 1, 'item_id 11': 1, 'item_id 12': 1, 'item_id 13': 1, 'item_id 14': 1, 'item_id 15': 1, 'item_id 16': 1, 'item_id 17': 1, 'item_id 18': 1, 'item_id 19': 0, 'item_id 20': 0, 'item_id 21': 0, 'item_id 22': 0, 'item_id 23': 0, 'item_id 24': 0, 'item_id 25': 0, 'item_id 26': 0, 'item_id 27': 0}}
"""


def get_llm_response(api_key: str, url: str, html_id_str: str, model_name: str) -> dict:
    # Set OpenAI's API key and API base to use vLLM's API server.
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key='sk-xxx',
        api_key=api_key,
        base_url=url,
    )

    content = f"""{promtp}以下是需要判断的html代码：
        ```
        {html_id_str}
        ```
        返回结果：
    """
    try:
        completion = client.chat.completions.create(
            model=model_name,
            extra_body={'enable_thinking': False},
            messages=[
                {'role': 'system', 'content': 'You are a text recognition expert.'},
                {'role': 'user', 'content': content}

            ],
        )

        rtn = completion.model_dump_json()
        rtn_detail = json_loads(rtn)
        post_llm_response = rtn_detail.get('choices', [])[0].get('message', {}).get('content', '')
        if '}' not in post_llm_response:
            logger.exception(f'post_llm_response more than token limit, post_llm_response: {post_llm_response}')
            return None
        return post_llm_response
    except BadRequestError as e:
        logger.exception(e)
        return None
