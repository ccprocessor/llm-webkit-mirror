import unittest
from pathlib import Path

from llm_web_kit.extractor.html.recognizer.image import ImageRecognizer
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag

TEST_CASES_HTML = [
    {
        'input': 'assets/ccimage/figure_iframe.html',
        'base_url': 'http://15.demooo.pl/produkt/okulary-ochronne/',
        'expected': 33,
        'ccimg_html': """<html lang="pl-PL" prefix="og: https://ogp.me/ns#"><body class="product-template-default single single-product postid-2386 theme-starter woocommerce woocommerce-page woocommerce-no-js tinvwl-theme-style"><header class="Header bg-white py-8 lg:py-0 sticky lg:fixed lg:w-full left-0 top-0 transition-all duration-300 z-50"><div class="Container flex justify-between items-center"><div class="Header__logo"><a href="http://15.demooo.pl"><ccimage by="img" html=\'&lt;img src="http://15.demooo.pl/wp-content/themes/starter/dist/images/logos/janser-logo.svg" alt="Janser Logo"&gt;\' format="url" alt="Janser Logo">http://15.demooo.pl/wp-content/themes/starter/dist/images/logos/janser-logo.svg</ccimage></a></div></div></header></body></html>"""
    },
    {
        'input': 'assets/ccimage/picture_img.html',
        'base_url': 'http://yuqiaoli.cn/Shop/List_249.html',
        'expected': 53,
        'ccimg_html': """<html lang="en"><body><div id="page_container"><div id="header_nav"><header><div id="header" class="table"><section id="logo" class="tablecell"><div id="header_logo"><a href="https://www.bonty.net/"><ccimage by="img" html=\'&lt;img src="https://www.bonty.net/templates/darkmode/images/logo.webp?v=Y2024M07D12" width="180" height="180" alt="bonty" id="header_logo_img"&gt;\' format="url" alt="bonty" width="180" height="180">https://www.bonty.net/templates/darkmode/images/logo.webp?v=Y2024M07D12</ccimage></a></div></section></div></header></div></div></body></html>"""
    },
    {
        'input': 'assets/ccimage/svg_base64.html',
        'base_url': 'https://www.terrasoleil.com/collections/bestsellers/products/luna-soleil-tarot-deck',
        'expected': 179,
        'ccimg_html': """<html class="no-js" lang="en"><body><ccimage by="img" html=\'&lt;img alt="icon" width="9999" height="9999" style="pointer-events: none; position: absolute; top: 0; left: 0; width: 99vw; height: 99vh; max-width: 100%; max-height: 100%;" src="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c3ZnIHdpZHRoPSI5OTk5OXB4IiBoZWlnaHQ9Ijk5OTk5cHgiIHZpZXdCb3g9IjAgMCA5OTk5OSA5OTk5OSIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIj48ZyBzdHJva2U9Im5vbmUiIGZpbGw9Im5vbmUiIGZpbGwtb3BhY2l0eT0iMCI+PHJlY3QgeD0iMCIgeT0iMCIgd2lkdGg9Ijk5OTk5IiBoZWlnaHQ9Ijk5OTk5Ij48L3JlY3Q+IDwvZz4gPC9zdmc+"&gt;\n \' format="base64" alt="icon" width="9999" height="9999">data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c3ZnIHdpZHRoPSI5OTk5OXB4IiBoZWlnaHQ9Ijk5OTk5cHgiIHZpZXdCb3g9IjAgMCA5OTk5OSA5OTk5OSIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIj48ZyBzdHJva2U9Im5vbmUiIGZpbGw9Im5vbmUiIGZpbGwtb3BhY2l0eT0iMCI+PHJlY3QgeD0iMCIgeT0iMCIgd2lkdGg9Ijk5OTk5IiBoZWlnaHQ9Ijk5OTk5Ij48L3JlY3Q+IDwvZz4gPC9zdmc+</ccimage></body></html>"""
    },
    {
        'input': 'assets/ccimage/svg_img.html',
        'base_url': 'https://villarichic.com/collections/dresses/products/dont-hang-up-faux-suede-shirt-dress1?variant=45860191863029',
        'expected': 32,
        'ccimg_html': """<html lang="en" class="no-js"><body class="gridlock template-product product theme-features__header-border-style--solid theme-features__header-horizontal-alignment--bottom theme-features__header-border-weight--3 theme-features__header-border-width--10 theme-features__header-edges--none theme-features__h2-size--28 theme-features__header-vertical-alignment--center theme-features__rounded-buttons--enabled theme-features__display-options--image-switch theme-features__product-align--center theme-features__product-border--disabled theme-features__product-info--sizes theme-features__price-bold--disabled theme-features__product-icon-position--top-left theme-features__ultra-wide--disabled js-slideout-toggle-wrapper js-modal-toggle-wrapper"><main id="main-content" class="site-wrap" role="main" tabindex="-1"><div class="js-header-group"><div id="shopify-section-sections--18000509272309__header" class="shopify-section shopify-section-group-header-group js-site-header"><theme-header><header class="header__wrapper  above_center js-theme-header stickynav" data-section-id="sections--18000509272309__header" data-section-type="header-section" data-overlay-header-enabled="false"><nav class="header__nav-container   bottom-border js-nav"><div class="header__nav-above grid__wrapper  device-hide"><div class="span-6 push-3 a-center v-center"><div id="logo" class="header__logo-image"><a href="/"><ccimage by="img" html=\'&lt;img src="//villarichic.com/cdn/shop/files/Dark_Blue_Villari_Chic_Logo.png?v=1725465655&amp;amp;width=600" alt="" srcset="//villarichic.com/cdn/shop/files/Dark_Blue_Villari_Chic_Logo.png?v=1725465655&amp;amp;width=352 352w, //villarichic.com/cdn/shop/files/Dark_Blue_Villari_Chic_Logo.png?v=1725465655&amp;amp;width=600 600w" width="600" height="106" loading="eager" fetchpriority="high"&gt;\n                                    \' format="url" width="600" height="106">https://villarichic.com/cdn/shop/files/Dark_Blue_Villari_Chic_Logo.png?v=1725465655&amp;width=600</ccimage></a></div></div></div></nav></header></theme-header></div></div></main></body></html>"""
    },
    {
        'input': 'assets/ccimage/table_img.html',
        'base_url': 'http://www.99ja.cn/products/product-86-401.html',
        'expected': 1,
    },
    {
        'input': 'assets/ccimage/unescape_img.html',
        'base_url': 'http://www.aspengreencbd.net/category.php?id=47',
        'expected': 60,
        'ccimg_html': """<html xmlns="http://www.w3.org/1999/xhtml"><body><div class="header-main"><div class="block"><div class="header-logo header-logo-index"><a href="index.php"><ccimage by="img" html=\'&lt;img src="themes/ecmoban_kaola2016/images/logo.gif" alt=""&gt;\' format="url">http://www.aspengreencbd.net/themes/ecmoban_kaola2016/images/logo.gif</ccimage></a></div></div></div></body></html>"""
    },
    {
        'input': 'assets/ccimage/no_parent_img.html',
        'base_url': 'https://orenburg.shtaketniki.ru/evroshtaketnik-uzkij.html',
        'expected': 2,
        'ccimg_html': """<htmllang="ru"><body><ccimageby="img"html=\'&lt;imgclass="lazyload"data-src="/work/img/Screenshot_608.png"src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="title="Видеозаборовизметаллоштакетника"alt="Видеозаборовизметаллоштакетника"&gt;\'format="url"alt="В идеозаборовизметаллоштакетника"title="Видеозаборовизметаллоштакетника">https://orenburg.shtaketniki.ru/work/img/Screenshot_608.png</ccimage></body></html>"""
    },
    {
        'input': 'assets/ccimage/object_pdf.html',
        'base_url': 'https://bukoda.gov.ua/npas/pro-nadannia-zghody-na-podil-zemelnoi-dilianky-derzhavnoi-vlasnosti-chernivetskomu-fakhovomu-koledzhu-tekhnolohii-ta-dyzainu',
        'expected': 3,
        'ccimg_html': """<html lang="ua"><body><div class="wrapper"><footer class="footer" id="layout-footer"><div class="footer_top row justify-content-md-between"><div class="col-md-6 col-lg-5"><div class="item first"><ccimage by="img" html=\'&lt;img src="/storage/app/sites/23/logo.svg" alt="" class="footer_logo lowvision_image_filter"&gt;\n\n                    \' format="url">https://bukoda.gov.ua/storage/app/sites/23/logo.svg</ccimage></div></div></div></footer></div></body></html>"""
    },
]

TEST_CC_CASE = [
    {
        'url': 'xxx',
        'parsed_content': """<ccimage by="img" html='&lt;img src="http://15.demooo.pl/wp-content/themes/starter/dist/images/logos/janser-logo.svg" alt="Janser Logo"&gt;' format="url" alt="Janser Logo">http://15.demooo.pl/wp-content/themes/starter/dist/images/logos/janser-logo.svg</ccimage>""",
        'html': '...',
        'expected': {'type': 'image', 'raw_content': '...', 'content': {
            'url': 'http://15.demooo.pl/wp-content/themes/starter/dist/images/logos/janser-logo.svg', 'data': None,
            'alt': 'Janser Logo', 'title': None, 'caption': None}},
        'alt': 'Janser Logo',
        'img_url': 'http://15.demooo.pl/wp-content/themes/starter/dist/images/logos/janser-logo.svg'
    },
    {
        'url': 'xxx',
        'parsed_content': """<ccimage by="figure" html='&lt;figure&gt;&lt;img src="http://15.demooo.pl/wp-content/uploads/2022/08/ukladanie-wykladzin.svg" alt="Układanie wykładzin"&gt;&lt;/figure&gt;

                                    ' format="url" alt="Układanie wykładzin">http://15.demooo.pl/wp-content/uploads/2022/08/ukladanie-wykladzin.svg</ccimage>""",
        'html': '...',
        'expected': {'type': 'image', 'raw_content': '...',
                     'content': {'url': 'http://15.demooo.pl/wp-content/uploads/2022/08/ukladanie-wykladzin.svg',
                                 'data': None, 'alt': 'Układanie wykładzin', 'title': None, 'caption': None}},
        'alt': 'Układanie wykładzin',
        'img_url': 'http://15.demooo.pl/wp-content/uploads/2022/08/ukladanie-wykladzin.svg'
    }

]
base_dir = Path(__file__).parent


class TestImageRecognizer(unittest.TestCase):
    def setUp(self):
        self.img_recognizer = ImageRecognizer()

    def test_recognize(self):
        for test_case in TEST_CASES_HTML:
            raw_html_path = base_dir.joinpath(test_case['input'])
            base_url = test_case['base_url']
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.img_recognizer.recognize(base_url, [(raw_html, raw_html)], raw_html)
            self.assertEqual(len(parts), test_case['expected'])
            ccimg_datas = [ccimg[0] for ccimg in parts if CCTag.CC_IMAGE in ccimg[0] and 'by="svg"' not in ccimg[0]]
            if ccimg_datas:
                ccimg_data = ccimg_datas[0].replace('\n', '').replace(' ', '')
                ccimg_html = test_case.get('ccimg_html').replace('\n', '').replace(' ', '')
                self.assertEqual(ccimg_data, ccimg_html)

    def test_to_content_list_node(self):
        for test_case in TEST_CC_CASE:
            res = self.img_recognizer.to_content_list_node(test_case['url'], test_case['parsed_content'],
                                                           test_case['html'])
            self.assertEqual(res, test_case['expected'])
            self.assertEqual(res['content']['alt'], test_case['alt'])
            self.assertEqual(res['content']['url'], test_case['img_url'])
