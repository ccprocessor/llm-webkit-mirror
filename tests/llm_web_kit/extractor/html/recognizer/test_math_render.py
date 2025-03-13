import unittest
from pathlib import Path

from llm_web_kit.extractor.html.recognizer.cc_math.render.render import \
    BaseMathRender

TEST_GET_MATH_RENDER = [
    {
        'input': [
            'assets/ccmath/stackexchange_1_span-math-container_latex_mathjax.html'
        ],
        'base_url': 'https://worldbuilding.stackexchange.com/questions/162264/is-there-a-safe-but-weird-distance-from-black-hole-merger',
        'expected': 'mathjax',
        'is_customized_options': False
    },
    {
        'input': [
            'assets/ccmath/libretexts_1_p_latex_mathjax.html',
        ],
        'base_url': 'https://math.libretexts.org/Under_Construction/Purgatory/Remixer_University/Username%3A_pseeburger/MTH_098_Elementary_Algebra/1%3A_Foundations/1.5%3A_Multiply_and_Divide_Integers',
        'expected': 'mathjax',
        'is_customized_options': True
    },
    {
        'input': [
            'assets/ccmath/math_katex_latex_2.html',
        ],
        'base_url': 'https://www.intmath.com/cg5/katex-mathjax-comparison.php',
        'expected': 'katex',
        'is_customized_options': False
    }
]
base_dir = Path(__file__).parent


class TestMathRender(unittest.TestCase):
    def setUp(self):
        self.render = BaseMathRender()

    def test_get_math_render(self):
        for test_case in TEST_GET_MATH_RENDER:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            raw_html = raw_html_path.read_text()
            output_render = self.render.get_math_render(raw_html)
            self.assertEqual(output_render.render_type, test_case['expected'])
