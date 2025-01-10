import unittest
from pathlib import Path

from llm_web_kit.pipeline.extractor.html.recognizer.image import \
    ImageRecognizer

TEST_CASES_HTML = [
    {
        'input': ['assets/ccimage/figure_iframe.html'],
        'base_url': 'http://15.demooo.pl/produkt/okulary-ochronne/',
        'expected': 35,
    },
    {
        'input': ['assets/ccimage/picture_img.html'],
        'base_url': 'http://yuqiaoli.cn/Shop/List_249.html',
        'expected': 53,
    },
    {
        'input': ['assets/ccimage/svg_base64.html'],
        'base_url': 'https://www.terrasoleil.com/collections/bestsellers/products/luna-soleil-tarot-deck',
        'expected': 215,
    },
    {
        'input': ['assets/ccimage/svg_img.html'],
        'base_url': 'https://villarichic.com/collections/dresses/products/dont-hang-up-faux-suede-shirt-dress1?variant=45860191863029',
        'expected': 44,
    },
    {
        'input': ['assets/ccimage/table_img.html'],
        'base_url': 'http://www.99ja.cn/products/product-86-401.html',
        'expected': 1,
    },
    {
        'input': ['assets/ccimage/unescape_img.html'],
        'base_url': 'http://www.aspengreencbd.net/category.php?id=47',
        'expected': 62,
    },
    {
        'input': ['assets/ccimage/no_parent_img.html'],
        'base_url': 'https://orenburg.shtaketniki.ru/evroshtaketnik-uzkij.html',
        'expected': 4,
    },
    {
        'input': ['assets/ccimage/object_pdf.html'],
        'base_url': 'https://bukoda.gov.ua/npas/pro-nadannia-zghody-na-podil-zemelnoi-dilianky-derzhavnoi-vlasnosti-chernivetskomu-fakhovomu-koledzhu-tekhnolohii-ta-dyzainu',
        'expected': 3,
    },
]

TEST_CC_CASE = [
    {
        'url': 'xxx',
        'parsed_content': """<ccimage by="img" html='&lt;img border="0" src="http://wpa.qq.com/pa?p=2:122405331:41" alt="qq" title="qq"&gt;' src="http://wpa.qq.com/pa?p=2:122405331:41" alt="qq" title="qq">http://wpa.qq.com/pa?p=2:122405331:41</ccimage>""",
        'html': '...',
        'expected': {'type': 'image', 'raw_content': '...',
                     'content': {'image_content': 'http://wpa.qq.com/pa?p=2:122405331:41', 'language': 'python',
                                 'by': 'img'}},
    },

]
base_dir = Path(__file__).parent


class TestImageRecognizer(unittest.TestCase):
    def setUp(self):
        self.img_recognizer = ImageRecognizer()

    def test_recognize(self):
        for test_case in TEST_CASES_HTML:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            base_url = test_case['base_url']
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.img_recognizer.recognize(base_url, [(raw_html, raw_html)], raw_html)
            self.assertEqual(len(parts), test_case['expected'])

    def test_to_content_list_node(self):
        for test_case in TEST_CC_CASE:
            res = self.img_recognizer.to_content_list_node(test_case['url'], test_case['parsed_content'],
                                                           test_case['html'])
            self.assertEqual(res, test_case['expected'])
