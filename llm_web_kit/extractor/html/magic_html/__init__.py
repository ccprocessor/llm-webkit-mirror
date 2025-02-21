from urllib.parse import urlparse

from llm_web_kit.extractor.html.magic_html.extractors.article_extractor import \
    ArticleExtractor
from llm_web_kit.extractor.html.magic_html.extractors.custom_extractor import \
    CustomExtractor
from llm_web_kit.extractor.html.magic_html.extractors.forum_extractor import \
    ForumExtractor
from llm_web_kit.extractor.html.magic_html.extractors.weixin_extractor import \
    WeixinExtractor


class GeneralExtractor:
    """通用抽取器.

    Attributes:
        custom_rule_path: 自定义抽取规则文件
        rule: 自定规则
    """

    def __init__(self, custom_rule=None):
        """初始化通用抽取器.

        Args:
            custom_rule:
        """
        if custom_rule is None:
            custom_rule = {}
        self.rule = custom_rule

    def extract(self, html='', **kwargs) -> dict:
        """聚合抽取内容方法.

        Args:
            html: 网页str
            **kwargs: base_url, html_type, precision

        Returns:
            抽取结果dict. For example:
            {
            "xp_num": "1",
            "drop_list": True,
            "html": "<html></html>",
            "title": "title",
            "base_url": "http://test.com/",
             }
        """
        base_url = kwargs.get('base_url', '')
        html_type = kwargs.pop('html_type', None)
        precision = kwargs.pop('precision', True)
        if html_type:
            if html_type == 'forum':
                return ForumExtractor(precision=precision).extract(html=html, **kwargs)
            elif html_type == 'weixin':
                return WeixinExtractor(precision=precision).extract(html=html, **kwargs)
        if base_url:
            netloc = urlparse(base_url).netloc
            if netloc in self.rule:
                try:
                    new_kwargs = dict()
                    new_kwargs['rule'] = self.rule[netloc]
                    new_kwargs.update(kwargs)
                    return CustomExtractor(precision=precision).extract(html=html, **new_kwargs)
                except Exception:
                    # 当自定义规则不能覆盖站点所有板块时
                    return ArticleExtractor(precision=precision).extract(html=html, **kwargs)
            if netloc == 'mp.weixin.qq.com':
                return WeixinExtractor(precision=precision).extract(html=html, **kwargs)
        return ArticleExtractor(precision=precision).extract(html=html, **kwargs)
