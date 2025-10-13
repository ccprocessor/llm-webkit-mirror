INVISIBLE_TAGS = [
    # url 匹配一级域名，* 指匹配所有网站
    {'url': '*', 'tag': '//div[starts-with(@class, "advert") or starts-with(@name, "advert") or starts-with(@id, "advert")]'},
    {'url': '*', 'tag': '//div[contains(@style, "display: none")]'},
    {'url': '*', 'tag': '//div[contains(@style, "display:none")]'},
    {'url': '*', 'tag': '//*[@hidden and not(@hidden="false")]'},
    {'url': 'stackexchange.com', 'tag': '//*[contains(@class, "d-none")]'},  # 任意标签，class包含d-none，限制在stackexchange.com网站
    {'url': 'mathoverflow.net', 'tag': '//*[contains(@class, "d-none")]'},  # 任意标签，class包含d-none，限制在mathoverflow.net网站
    {'url': 'blog.csdn.net', 'tag': '//span[contains(@class, "katex-html")]'},  # 仅针对 blog.csdn.net 域名，删除所有 class 包含 katex-html 的 <span> 标签及其内容（用于移除数学公式渲染的 HTML 部分）
    {'url': 'math.libretexts.org', 'tag': '//div[contains(@class, "Headertext")]'},  # 仅针对 bmath.libretexts.org 域名，删除所有 class 包含 Headertext 的 <div> 标签及其内容
]
