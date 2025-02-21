from magic_html import GeneralExtractor


def eval_magic_html(html: str, url: str) -> str:
    # 初始化提取器
    extractor = GeneralExtractor()

    # 文章类型HTML提取数据
    data = extractor.extract(html, base_url=url)

    # 论坛类型HTML提取数据
    # data = extractor.extract(html, base_url=url, html_type="forum")

    # 微信文章HTML提取数据
    # data = extractor.extract(html, base_url=url, html_type="weixin")

    return data.get('html', '')
