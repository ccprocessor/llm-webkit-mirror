INVISIBLE_TAGS = [
    # url 匹配一级域名，* 指匹配所有网站
    {'url': '*', 'tag': '//div[starts-with(@class, "advert") or starts-with(@name, "advert") or starts-with(@id, "advert")]'},
    {'url': '*', 'tag': '//div[contains(@style, "display: none")]'},
    {'url': '*', 'tag': '//div[contains(@style, "display:none")]'},
    {'url': 'stackexchange.com', 'tag': '//*[contains(@class, "d-none")]'},  # 任意标签，class包含d-none，限制在stackexchange.com网站
    {'url': 'mathoverflow.net', 'tag': '//*[contains(@class, "d-none")]'},  # 任意标签，class包含d-none，限制在mathoverflow.net网站
]
