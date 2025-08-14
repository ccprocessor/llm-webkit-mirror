import unittest
from pathlib import Path

from llm_web_kit.exception.exception import HtmlMathRecognizerException
from llm_web_kit.extractor.html.pre_extractor import \
    HTMLFileFormatCleanTagsPreExtractor
from llm_web_kit.extractor.html.recognizer.cc_math.common import (
    CCMATH_INLINE, CSDN, ZHIHU)
from llm_web_kit.extractor.html.recognizer.cc_math.tag_script import (
    process_katex_mathml, process_zhihu_custom_tag)
from llm_web_kit.extractor.html.recognizer.ccmath import CCMATH, MathRecognizer
from llm_web_kit.extractor.html.recognizer.recognizer import CCTag
from llm_web_kit.libs.html_utils import element_to_html, html_to_element

TEST_CASES = [
    # 基本公式测试用例
    {
        'input': [
            (
                ('<p>这是p的text<span class="mathjax_display">'
                 '$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>'
                 '这是b的tail</p>'),
                ('<p>这是p的text<span class="mathjax_display">'
                 '$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>'
                 '这是b的tail</p>')
            )
        ],
        'raw_html': (
            '<head> '
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js'
            '?config=TeX-MML-AM_CHTML"> </script> '
            '</head> '
            '<p>这是p的text<span class="mathjax_display">$$a^2 + b^2 = c^2$$</span>这是span的tail<b>这是b的text</b>这是b的tail</p>'
        ),
        'expected': [
            (
                '<p>这是p的text<span class="mathjax_display"></span></p>',
                '<p>这是p的text<span class="mathjax_display"></span></p>'
            ),
            (
                '<p><span class="mathjax_display"><ccmath-interline type="latex" by="mathjax" html="$$a^2 + b^2 = c^2$$">a^2 + b^2 = c^2</ccmath-interline></span></p>',
                '<p><span class="mathjax_display"><ccmath-interline type="latex" by="mathjax" html="$$a^2 + b^2 = c^2$$">a^2 + b^2 = c^2</ccmath-interline></span></p>'
            ),
            (
                '<p><span class="mathjax_display"></span>这是span的tail<b>这是b的text</b>这是b的tail</p>',
                '<p><span class="mathjax_display"></span>这是span的tail<b>这是b的text</b>这是b的tail</p>'
            )
        ]
    },
    {
        'input': [
            ('<p>$x = 5$,$$x=6$$</p>',
             '<p>$x = 5$,$$x=6$$</p>')
        ],
        'raw_html': '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"> </script><p>$x = 5$,$$x=6$$</p>',
        'expected': [
            ('<p><ccmath-inline type="latex" by="mathjax" html="$x = 5$">x = 5</ccmath-inline>,</p>',
             '<p><ccmath-inline type="latex" by="mathjax" html="$x = 5$">x = 5</ccmath-inline>,</p>'),
             ('<p><ccmath-interline type="latex" by="mathjax" html="$$x=6$$">x=6</ccmath-interline></p>',
              '<p><ccmath-interline type="latex" by="mathjax" html="$$x=6$$">x=6</ccmath-interline></p>')
        ]
    },
    {
        'input': [
            ('<p>$x = 5$,$$x=6$$,$x=4$</p>',
             '<p>$x = 5$,$$x=6$$,$x=4$</p>')
        ],
        'raw_html': '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"> </script> <p>$x = 5$,$$x=6$$,$x=4$</p>',
        'expected': [
            ('<p><ccmath-inline type="latex" by="mathjax" html="$x = 5$">x = 5</ccmath-inline>,</p>', '<p><ccmath-inline type="latex" by="mathjax" html="$x = 5$">x = 5</ccmath-inline>,</p>'),
            ('<p><ccmath-interline type="latex" by="mathjax" html="$$x=6$$">x=6</ccmath-interline></p>', '<p><ccmath-interline type="latex" by="mathjax" html="$$x=6$$">x=6</ccmath-interline></p>'),
            ('<p>,<ccmath-inline type="latex" by="mathjax" html="$x=4$">x=4</ccmath-inline></p>', '<p>,<ccmath-inline type="latex" by="mathjax" html="$x=4$">x=4</ccmath-inline></p>')
        ]
    },
    {
        'input': [
            ('<p>By substituting $$x$$ with $$t - \\dfrac{b}{3a}$$, the general</p>',
             '<p>By substituting $$x$$ with $$t - \\dfrac{b}{3a}$$, the general</p>')
        ],
        'raw_html': '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"> </script> <p>By substituting $$x$$ with $$t - \\dfrac{b}{3a}$$, the general</p>',
        'expected': [
            ('<p>By substituting </p>',
             '<p>By substituting </p>'),
            ('<p><ccmath-interline type="latex" by="mathjax" html="$$x$$">x</ccmath-interline></p>',
             '<p><ccmath-interline type="latex" by="mathjax" html="$$x$$">x</ccmath-interline></p>'),
            ('<p> with </p>',
             '<p> with </p>'),
            ('<p><ccmath-interline type="latex" by="mathjax" html="$$t - \\dfrac{b}{3a}$$">t - \\dfrac{b}{3a}</ccmath-interline></p>',
             '<p><ccmath-interline type="latex" by="mathjax" html="$$t - \\dfrac{b}{3a}$$">t - \\dfrac{b}{3a}</ccmath-interline></p>'),
            ('<p>, the general</p>',
             '<p>, the general</p>')
        ]
    },
    {
        'input': [
            ('<script type="math/tex">x^2 + y^2 = z^2</script>', '<script type="math/tex">x^2 + y^2 = z^2</script>')
        ],
        'raw_html': '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"> </script><script type="math/tex">x^2 + y^2 = z^2</script>',
        'expected': [
            ('<html><head><ccmath-inline type="latex" by="mathjax" html=\'&lt;script type="math/tex"&gt;x^2 + y^2 = z^2&lt;/script&gt;\'>x^2 + y^2 = z^2</ccmath-inline></head></html>', '<html><head><ccmath-inline type="latex" by="mathjax" html=\'&lt;script type="math/tex"&gt;x^2 + y^2 = z^2&lt;/script&gt;\'>x^2 + y^2 = z^2</ccmath-inline></head></html>')
        ]
    },
    {
        'input': [
            ('<script type="math/tex"></script>', '<script type="math/tex"></script>')
        ],
        'raw_html': '<script type="math/tex"></script>',
        'expected': []
    },
    {
        'input': [
            ('<p>保证生活，可能会影响自己的身心健康。当然，在 不打工的情况下考虑创业， 但是创业是有风险的，在自己没有经济$ $③收入的情况下，考虑打工也会让自己的压力倍增，所以是否选择打工，需要根据自己的实际情况决定!</p>', '<p>保证生活，可能会影响自己的身心健康。当然，在 不打工的情况下考虑创业， 但是创业是有风险的，在自己没有经济$ $③收入的情况下，考虑打工也会让自己的压力倍增，所以是否选择打工，需要根据自己的实际情况决定!</p>')
        ],
        'raw_html': '<p>保证生活，可能会影响自己的身心健康。当然，在 不打工的情况下考虑创业， 但是创业是有风险的，在自己没有经济$ $③收入的情况下，考虑打工也会让自己的压力倍增，所以是否选择打工，需要根据自己的实际情况决定!</p>',
        'expected': [('<p>保证生活，可能会影响自己的身心健康。当然，在 不打工的情况下考虑创业， 但是创业是有风险的，在自己没有经济$ $③收入的情况下，考虑打工也会让自己的压力倍增，所以是否选择打工，需要根据自己的实际情况决定!</p>', '<p>保证生活，可能会影响自己的身心健康。当然，在 不打工的情况下考虑创业， 但是创业是有风险的，在自己没有经济$ $③收入的情况下，考虑打工也会让自己的压力倍增，所以是否选择打工，需要根据自己的实际情况决定!</p>')]
    }

]

TEST_CASES_HTML = [
    # math-container, latex + mathjax
    {
        'input': ['assets/ccmath/stackexchange_1_span-math-container_latex_mathjax.html'],
        'base_url': 'https://worldbuilding.stackexchange.com/questions/162264/is-there-a-safe-but-weird-distance-from-black-hole-merger',
        'expected': 'assets/ccmath/stackexchange_1_span-math-container_latex_mathjax_1.html',
        'expected_inline': 'assets/ccmath/stackexchange_1_span-math-container_latex_mathjax_inline_1.html'
    },
    {
        'input': [
            'assets/ccmath/libretexts_1_p_latex_mathjax.html',
        ],
        'base_url': 'https://math.libretexts.org/Under_Construction/Purgatory/Remixer_University/Username%3A_pseeburger/MTH_098_Elementary_Algebra/1%3A_Foundations/1.5%3A_Multiply_and_Divide_Integers',
        'expected': 'assets/ccmath/libretexts_1_p_latex_mathjax_1.html',
        'expected_inline': 'assets/ccmath/libretexts_1_p_latex_mathjax_inline_1.html'
    },
    {
        'input': [
            'assets/ccmath/mathjax_tex_chtml.html',
        ],
        'base_url': 'https://math.libretexts.org/Under_Construction/Purgatory/Remixer_University/Username%3A_pseeburger/MTH_098_Elementary_Algebra/1%3A_Foundations/1.5%3A_Multiply_and_Divide_Integers',
        'expected': 'assets/ccmath/mathjax_tex_chtml_1.html',
        'expected_inline': 'assets/ccmath/mathjax_tex_chtml_inline_1.html'
    },
    {
        'input': [
            'assets/ccmath/wikipedia_1_math_annotation.html',
        ],
        'base_url': 'https://en.m.wikipedia.org/wiki/Variance',
        'expected': 'assets/ccmath/wikipedia_1_math_annotation_1.html',
        'expected_inline': 'assets/ccmath/wikipedia_1_math_annotation_inline_1.html'
    },
    {
        'input': [
            'assets/ccmath/mathjax-mml-chtml.html',
        ],
        'base_url': 'https://mathjax.github.io/MathJax-demos-web/tex-chtml.html',
        'expected': 'assets/ccmath/mathjax-mml-chtml_1.html',
        'expected_inline': 'assets/ccmath/mathjax-mml-chtml_inline_1.html'
    },
    # img latex.php
    {
        'input': ['assets/ccmath/geoenergymath_img.html'],
        'base_url': 'https://geoenergymath.com/2017/03/04/the-chandler-wobble-challenge/',
        'expected': 'assets/ccmath/geoenergymath_img_1.html',
        'expected_inline': 'assets/ccmath/geoenergymath_img_inline_1.html'
    },
    # # img codecogs.com
    {
        'input': ['assets/ccmath/img_codecogs_com.html'],
        'base_url': 'https://up-skill.me/math/find-interquartile-range.html',
        'expected': 'assets/ccmath/img_codecogs_com_1.html',
        'expected_inline': 'assets/ccmath/img_codecogs_com_inline_1.html'
    },
    # img mimetex.cgi
    {
        'input': ['assets/ccmath/img_mimetex_cgi.html'],
        'base_url': 'https://math.eretrandre.org/tetrationforum/showthread.php?tid=965',
        'expected': 'assets/ccmath/img_mimetex_cgi_1.html',
        'expected_inline': 'assets/ccmath/img_mimetex_cgi_inline_1.html'
    },
    {
        'input': ['assets/ccmath/katex_mathjax.html'],
        'base_url': 'https://www.intmath.com/cg5/katex-mathjax-comparison.php',
        'expected': 'assets/ccmath/katex_mathjax_1.html',  # 46个公式
        'expected_inline': 'assets/ccmath/katex_mathjax_inline_1.html'
    },
    {
        'input': [
            'assets/ccmath/mathjax-mml-chtml_prefix.html',
        ],
        'base_url': 'https://mathjax.github.io/MathJax-demos-web/tex-chtml.html',
        'expected': 'assets/ccmath/mathjax-mml-chtml_prefix_1.html',
        'expected_inline': 'assets/ccmath/mathjax-mml-chtml_prefix_inline_1.html'
    },
    {
        'input': [
            'assets/ccmath/math_physicsforums.html',
        ],
        'base_url': 'https://www.physicsforums.com/threads/probability-theoretic-inequality.246150/',
        'expected': 'assets/ccmath/math_physicsforums_1.html',
        'expected_inline': 'assets/ccmath/math_physicsforums_inline_1.html'
    },
    {
        'input': [
            'assets/ccmath/math_physicsforums_2.html',
        ],
        'base_url': 'https://physicshelpforum.com/t/latex-upgrade-physics-forum-powered-by-mathjax-v3.17489/',
        'expected': 'assets/ccmath/math_physicsforums_2_1.html',
        'expected_inline': 'assets/ccmath/math_physicsforums_2_inline_1.html'
    },
    {
        'input': [
            'assets/ccmath/math_class_math.html',
        ],
        'base_url': 'https://convertoctopus.com/4-7-years-to-minutes',
        'expected': 'assets/ccmath/math_class_math_1.html',
        'expected_inline': 'assets/ccmath/math_class_math_inline_1.html'
    }
]

TEST_EQUATION_TYPE = [
    {
        'input': '<span>$$a^2 + b^2 = c^2$$</span>',
        'expected': [('ccmath-interline', 'latex')]
    },
    {
        'input': '<span>$a^2 + b^2 = c^2$</span>',
        'expected': [('ccmath-inline', 'latex')]
    },
    {
        'input': '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>',
        'expected': [('ccmath-inline', 'mathml')]
    },
    {
        'input': '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>a</mi><mo>&#x2260;</mo><mn>0</mn></math>',
        'expected': [('ccmath-interline', 'mathml')]
    },
    {
        'input': '<span>x<sub>1</sub> + x<sup>2</sup></span>',
        'expected': [('ccmath-inline', 'htmlmath')]
    },
    {
        'input': '<p>`x=(-b +- sqrt(b^2 - 4ac))/(2a)`</p>',
        'expected': [('ccmath-interline', 'asciimath')]
    },
    {
        'input': '<p>Matrices: <code>[[a,b],[c,d]]</code> </p>',
        'expected': [(None, None)]
    },
    {
        'input': '<p>这是p的text</p>',
        'expected': [(None, None)]
    },
    {
        'input': r'<p>\begin{align} a^2+b=c\end{align}</p>',
        'expected': [('ccmath-interline', 'latex')]
    },
    {
        'input': r'<p>$$x=5$$,$x=6$</p>',
        'expected': [('ccmath-interline', 'latex'), ('ccmath-inline', 'latex')]
    },
    {
        'input': r'<p>[tex]\frac{1}{4} Log(x-1)=Log((x-1)^{1\over{4}})= Log(\sqrt[4]{x-1})[/tex]</p>',
        'expected': [('ccmath-interline', 'latex')]
    },
    {
        'input': r'<p>abc [itex]x^2[/itex] abc</p>',
        'expected': [('ccmath-inline', 'latex')]
    }
]

TEST_CONTENT_LIST_NODE = [
    {
        'input': (
            'https://www.baidu.com',
            '<html><body><p><ccmath-interline type="latex" by="mathjax" html="&lt;span class=&quot;math-container&quot;&gt;$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$&lt;/span&gt;">$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$</ccmath-interline></p></body></html>',
            '<span class="math-container">$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$</span>'
        ),
        'expected': {
            'type': 'equation-interline',
            'raw_content': '<span class="math-container">$$h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}$$</span>',
            'content': {
                'math_content': 'h \\approx {{GM} \\over c^2} \\times {1 \\over r} \\times {v^2 \\over c^2}',
                'math_type': 'latex',
                'by': 'mathjax'
            }
        }
    }
]

TEST_WRAP_MATH_MD = [
    {
        'input': r'$$a^2 + b^2 = c^2$$',
        'expected': r'a^2 + b^2 = c^2'
    },
    {
        'input': r'{\displaystyle \operatorname {Var} (X)=\operatorname {E} \left[(X-\mu)^{2}\right].}',
        'expected': r'{\displaystyle \operatorname {Var} (X)=\operatorname {E} \left[(X-\mu)^{2}\right].}'
    },
    {
        'input': r'$a^2 + b^2 = c^2$',
        'expected': r'a^2 + b^2 = c^2'
    },
    {
        'input': r'\(a^2 + b^2 = c^2\)',
        'expected': r'a^2 + b^2 = c^2'
    },
    {
        'input': r'\[a^2 + b^2 = c^2\]',
        'expected': r'a^2 + b^2 = c^2'
    },
    {
        'input': r'`E=mc^2`',
        'expected': r'E=mc^2'
    },
    {
        'input': '',
        'expected': ''
    },
    {
        'input': r'<br />\begin{align} a^2+b=c\end{align}\<br />',
        'url': 'mathhelpforum.com',
        'expected': r'\begin{align} a^2+b=c\end{align}'
    },
    {
        'input': r'<br />dz=\frac{1}{2}\frac{dx}{\cos ^2 x}<br />',
        'url': 'mathhelpforum.com',
        'expected': r'dz=\frac{1}{2}\frac{dx}{\cos ^2 x}'
    },
    {
        'input': r'<br />\begin{align} a^2+b=c\end{align}\<br />',
        'expected': r'<br />\begin{align} a^2+b=c\end{align}\<br />'
    }
]

TEST_FIX_MATHML_SUPERSCRIPT = [
    {
        'input': r'<math xmlns="http://www.w3.org/1998/Math/MathML"><mo stretchy="false">(</mo><mn>1</mn><mo>+</mo><mi>x</mi><msup><mo stretchy="false">)</mo><mn>2</mn></msup></math>',
        'expected': r'<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mo stretchy="false">(</mo><mn>1</mn><mo>+</mo><mi>x</mi><mo stretchy="false">)</mo></mrow><mn>2</mn></msup></math>'
    }
]

TEST_MML_TO_LATEX = [
    {
        'input': r'<math xmlns="http://www.w3.org/1998/Math/MathML"><msqrt><mn>3</mn><mi>x</mi><mo>&#x2212;<!-- − --></mo><mn>1</mn></msqrt><mo>+</mo><mo stretchy="false">(</mo><mn>1</mn><mo>+</mo><mi>x</mi><msup><mo stretchy="false">)</mo><mn>2</mn></msup></math>',
        'expected': r'$\sqrt{3x-1}+{\left(1+x\right)}^{2}$'
    },
    {
        'input': '''<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><msup><mrow><mo>(</mo><mrow><munderover><mo>&#x2211;<!-- ∑ --></mo><mrow class="MJX-TeXAtom-ORD"><mi>k</mi><mo>=</mo><mn>1</mn>
                </mrow><mi>n</mi></munderover><msub><mi>a</mi><mi>k</mi></msub><msub><mi>b</mi><mi>k</mi></msub></mrow><mo>)</mo></mrow><mrow class="MJX-TeXAtom-ORD"><mspace width="negativethinmathspace"></mspace><mspace width="negativethinmathspace"></mspace><mn>2</mn></mrow></msup></math>''',
        'expected': r'${\left(\sum _{k=1}^{n}{a}_{k}{b}_{k}\right)}^{2}$'
    }
]

TEST_CSDN_KATEX_MATHML = [
    {
        'input': r'''
        <span class="katex--inline"><span class="katex"><span class="katex-mathml">

           lim⁡
           x
           →
           1
             x
             2
            −
            1
            x
            −
            1

            \lim\limits_{x \to 1}\dfrac{x^2-1}{x-1}

        </span>
        ''',
        'expected_tag': 'ccmath-inline',
        'expected_formula': r'\lim\limits_{x \to 1}\dfrac{x^2-1}{x-1}'
    },
    {
        'input': r'''
        <span class="katex--display"><span class="katex-display"><span class="katex"><span class="katex-mathml">

            f
            (
            1
            )
            −
            f
            (
            1
            )
            1
            −
            1
          &#61;
           0
           0

            \frac{f(1)-f(1)}{1-1} &#61; \frac{0}{0}

         </span>
        ''',
        'expected_tag': 'ccmath-interline',
        'expected_formula': r'\frac{f(1)-f(1)}{1-1} = \frac{0}{0}'
    }
]

TEST_ZHIHU_ZTEXT_HTML = [
    {
        'input': r'<span class="ztext-math" data-eeimg="1" data-tex="s_1\overset{a_2}{\operatorname*{\longrightarrow}}s_2\overset{a_3}{\operatorname*{\longrightarrow}}s_5\overset{a_3}{\operatorname*{\longrightarrow}}s_8\overset{a_2}{\operatorname*{\longrightarrow}}s_9\overset{a_5}{\operatorname*{\longrightarrow}}s_9\overset{a_5}{\operatorname*{\longrightarrow}}s_9\ldots"><span>',
        'expected_tag': 'ccmath-inline',
        'expected_formula': r's_1\overset{a_2}{\operatorname*{\longrightarrow}}s_2\overset{a_3}{\operatorname*{\longrightarrow}}s_5\overset{a_3}{\operatorname*{\longrightarrow}}s_8\overset{a_2}{\operatorname*{\longrightarrow}}s_9\overset{a_5}{\operatorname*{\longrightarrow}}s_9\overset{a_5}{\operatorname*{\longrightarrow}}s_9\ldots'
    },
    {
        'input': r'<span class="ztext-math" data-eeimg="1" data-tex="\begin{aligned}  &amp; p(r|s,a) \\  &amp; \sum_{r\in\mathcal{R}(s,a)}p(r|s,a)=1\text{ for any }(s,a). \end{aligned}"><span>',
        'expected_tag': 'ccmath-interline',
        'expected_formula': r'\begin{aligned}  & p(r|s,a) \\  & \sum_{r\in\mathcal{R}(s,a)}p(r|s,a)=1\text{ for any }(s,a). \end{aligned}'
    }
]

TEST_IS_CC_TAG_NODE = [
    {
        'input': r'<div><p>行内公式1：$A+B=C$</p><p>行内公式2：$a+b=c$。</p><p>行间公式1：$$E+F=G$$。<\p><ccmath-interline type="latex" by="mathjax" html="$$t - \\dfrac{b}{3a}$$">t - \\dfrac{b}{3a}</ccmath-interline><p>行内公式3：$2A+2B=2C$。</p><p>行间公式2：$$2E+2F=2G$$。</p></div>',
        'cc_tag': '1',
        'not_cc_tag': '6',
    },
    {
        'input': r'<body><p><ccmath-interline type="latex" by="mathjax" html="$$x$$">x</ccmath-interline><p><ccmath-inline type="latex" by="mathjax" html="$x$">x</ccmath-inline></p><p>行内公式1：$A+B=C$</p><span class="math-container"><p>行间公式2$$D+E=F$$</p></span></body>',
        'cc_tag': '2',
        'not_cc_tag': '6',
    }
]
base_dir = Path(__file__).parent


class TestMathRecognizer(unittest.TestCase):
    def setUp(self):
        self.math_recognizer = MathRecognizer()
        self.maxDiff = None  # 显示完整的diff

    def test_math_recognizer(self):
        for test_case in TEST_CASES:
            with self.subTest(input=test_case['input'], raw_html=test_case['raw_html']):
                output_html = self.math_recognizer.recognize(
                    'https://www.baidu.com',
                    [(html_to_element(test_case['input'][0][0]), html_to_element(test_case['input'][0][1]))],
                    test_case['raw_html']
                )
                self.assertEqual(len(output_html), len(test_case['expected']))
                for i in range(len(output_html)):
                    expect = test_case['expected'][i][0]
                    self.assertEqual(element_to_html(output_html[i][0]), expect, msg=f'result is: {element_to_html(output_html[i][0])}, expected is: {expect}')

    def test_math_recognizer_html(self):
        for test_case in TEST_CASES_HTML:
            raw_html_path = base_dir.joinpath(test_case['input'][0])
            # print('raw_html_path::::::::', raw_html_path)
            base_url = test_case['base_url']
            raw_html = raw_html_path.read_text(encoding='utf-8')
            parts = self.math_recognizer.recognize(base_url, [(html_to_element(raw_html), html_to_element(raw_html))], raw_html)
            # print(parts)
            # 将parts列表中第一个元素拼接保存到文件，带随机数
            # import random
            # with open('parts'+str(random.randint(1, 100))+".html", 'w') as f:
            #     for part in parts:
            #         f.write(str(part[0]))
            # 创建预处理器并清理隐藏元素
            pre_extractor = HTMLFileFormatCleanTagsPreExtractor({})
            data_json = {'html': raw_html, 'url': base_url}
            data_json = pre_extractor._do_pre_extract(data_json)
            cleaned_html = data_json['html']

            # 使用清理后的HTML进行公式识别
            parts = self.math_recognizer.recognize(
                base_url,
                [(html_to_element(cleaned_html), html_to_element(cleaned_html))],
                cleaned_html
            )
            # 检查行间公式抽取正确性
            new_parts = []
            for part in parts:
                new_parts.append((element_to_html(part[0]), element_to_html(part[1])))
            parts = [part[0] for part in new_parts if CCTag.CC_MATH_INTERLINE in part[0]]
            expect_text = base_dir.joinpath(test_case['expected']).read_text(encoding='utf-8').strip()
            expect_formulas = [formula for formula in expect_text.split('\n') if formula]
            self.assertEqual(len(parts), len(expect_formulas))
            # answers = []
            for expect, part in zip(expect_formulas, parts):
                a_tree = html_to_element(part)
                a_result = a_tree.xpath(f'.//{CCTag.CC_MATH_INTERLINE}')[0]
                answer = a_result.text.replace('\n', '').strip()
                # print('part::::::::', part)
                # print('expect::::::::', expect)
                # print('answer::::::::', answer)
                # answers.append(answer)
                self.assertEqual(expect, answer)
            # print('answers::::::::', answers)
            # self.write_to_html(answers, test_case['input'][0])
            # 检查行内公式抽取正确性
            if test_case.get('expected_inline', None):
                # 从所有parts中提取所有行内公式
                all_inline_formulas = []
                for part in new_parts:
                    if CCTag.CC_MATH_INLINE in part[0]:
                        part_tree = html_to_element(part[0])
                        inline_elements = part_tree.xpath(f'.//{CCTag.CC_MATH_INLINE}')
                        for inline_elem in inline_elements:
                            formula = inline_elem.text.replace('\n', '').strip()
                            all_inline_formulas.append(formula)
                # print(f"Found {len(all_inline_formulas)} total inline formulas")
                # print(f"Total new_parts: {len(new_parts)}")
                expect_inline_text = base_dir.joinpath(test_case['expected_inline']).read_text(encoding='utf-8').strip()
                expect_inline_formulas = [formula for formula in expect_inline_text.split('\n') if formula]
                # print(f"Expected {len(expect_inline_formulas)} inline formulas")
                self.assertEqual(len(all_inline_formulas), len(expect_inline_formulas))
                for expect, formula in zip(expect_inline_formulas, all_inline_formulas):
                    # print('inline expect::::::::', expect)
                    # print('inline answer::::::::', formula)
                    self.assertEqual(expect, formula)

    def write_to_html(self, answers, file_name):
        file_name = file_name.split('.')[0]
        with open(base_dir.joinpath(f'{file_name}_1.html'), 'w', encoding='utf-8') as file:
            for formula in answers:
                file.write(formula)
                file.write('\n')

    def test_to_content_list_node(self):
        for test_case in TEST_CONTENT_LIST_NODE:
            with self.subTest(input=test_case['input']):
                output_node = self.math_recognizer.to_content_list_node(
                    test_case['input'][0],
                    html_to_element(test_case['input'][1]),
                    test_case['input'][2]
                )
                print('output_node::::::::', output_node)
                print(test_case['expected'])
                self.assertEqual(output_node, test_case['expected'])

        # 测试没有ccmath标签的情况
        invalid_content = (
            'https://www.baidu.com',
            '<div>Some math content</div>',
            '<div>Some math content</div>'
        )
        with self.assertRaises(HtmlMathRecognizerException) as exc_info:
            self.math_recognizer.to_content_list_node(
                invalid_content[0],
                html_to_element(invalid_content[1]),
                invalid_content[2]
            )
        self.assertIn('No ccmath element found in content', str(exc_info.exception))


class TestCCMATH(unittest.TestCase):
    def setUp(self):
        self.ccmath = CCMATH()

    def test_get_equation_type(self):
        for test_case in TEST_EQUATION_TYPE:
            with self.subTest(input=test_case['input']):
                tag_math_type_list = self.ccmath.get_equation_type(test_case['input'])
                print('input::::::::', test_case['input'])
                if tag_math_type_list:
                    for i in range(len(tag_math_type_list)):
                        expect0 = test_case['expected'][i][0]
                        expect1 = test_case['expected'][i][1]
                        self.assertEqual(tag_math_type_list[i][0], expect0, msg=f'result is: {tag_math_type_list[i][0]}, expected is: {expect0}')
                        self.assertEqual(tag_math_type_list[i][1], expect1, msg=f'result is: {tag_math_type_list[i][1]}, expected is: {expect1}')

    def test_wrap_math_md(self):
        for test_case in TEST_WRAP_MATH_MD:
            with self.subTest(input=test_case['input']):
                self.ccmath.url = test_case.get('url', '')
                output_math = self.ccmath.wrap_math_md(test_case['input'])
                self.assertEqual(output_math, test_case['expected'])

    def test_fix_mathml_superscript(self):
        for test_case in TEST_FIX_MATHML_SUPERSCRIPT:
            with self.subTest(input=test_case['input']):
                output_math = self.ccmath.fix_mathml_superscript(test_case['input'])
                output_math_clean = ''.join(output_math.split())
                expected_clean = ''.join(test_case['expected'].split())
                self.assertEqual(output_math_clean, expected_clean)

    def test_mml_to_latex(self):
        for test_case in TEST_MML_TO_LATEX:
            with self.subTest(input=test_case['input']):
                output_math = self.ccmath.mml_to_latex(test_case['input'])
                self.assertEqual(output_math, test_case['expected'])

    def test_csdn_katex_mathml(self):
        cm = CCMATH()
        for test_case in TEST_CSDN_KATEX_MATHML:
            with self.subTest(input=test_case['input']):
                element = html_to_element(test_case['input'])
                parent_class = CSDN.INLINE if test_case['expected_tag'] == CCMATH_INLINE else CSDN.DISPLAY
                katex_parent = element.xpath(f'//span[@class="{parent_class}"]')[0]
                expected_tag = test_case['expected_tag']
                process_katex_mathml(cm, 'katex', katex_parent)
                # 验证处理后的标签类型是否正确
                self.assertEqual(len(element.xpath(f'//{expected_tag}')), 1)
                # 验证公式内容是否正确
                formula = element.xpath(f'//{expected_tag}/text()')[0]
                self.assertIn(test_case['expected_formula'], formula)

    def test_zhihu_ztext_math(self):
        cm = CCMATH()
        for test_case in TEST_ZHIHU_ZTEXT_HTML:
            with self.subTest(input=test_case['input']):
                element = html_to_element(test_case['input'])
                ztext_math = element.xpath(f'//span[@class="{ZHIHU.MATH}"]')[0]
                expected_tag = test_case['expected_tag']
                process_zhihu_custom_tag(cm, 'MathJax', ztext_math)
                # 验证处理后的标签类型是否正确
                self.assertEqual(len(element.xpath(f'//{expected_tag}')), 1)
                # 验证公式内容是否正确
                formula = element.xpath(f'//{expected_tag}/text()')[0]
                self.assertIn(test_case['expected_formula'], formula)

    def test_is_cc_tag_node(self):
        from llm_web_kit.extractor.html.recognizer.recognizer import \
            BaseHTMLElementRecognizer
        for test_case in TEST_IS_CC_TAG_NODE:
            with self.subTest(input=test_case['input']):
                root = html_to_element(test_case['input'])
                cc_tag_count = 0
                not_cc_tag_count = 0

                def check_nodes(element):
                    nonlocal cc_tag_count, not_cc_tag_count
                    if element is None:
                        return
                    if BaseHTMLElementRecognizer.is_cc_tag_node(element):
                        cc_tag_count += 1
                        return
                    else:
                        not_cc_tag_count += 1
                    for child in element:
                        check_nodes(child)
                # mathjax方案是传入根节点递归调用，与其保持一致
                check_nodes(root)
                expected_cc_tag = int(test_case['cc_tag'])
                expected_not_cc_tag = int(test_case['not_cc_tag'])
                self.assertEqual(cc_tag_count, expected_cc_tag,
                                 f'Expected {expected_cc_tag} cc tags, but found {cc_tag_count}')
                self.assertEqual(not_cc_tag_count, expected_not_cc_tag,
                                 f'Expected {expected_not_cc_tag} non-cc tags, but found {not_cc_tag_count}')


if __name__ == '__main__':
    r = TestMathRecognizer()
    r.setUp()
    # r.test_math_recognizer()
    r.test_math_recognizer_html()
    # r.test_math_recognizer()
    # r.test_to_content_list_node()
    # html = r'<p class="lt-math-15120">\[\begin{array} {ll} {5 \cdot 3 = 15} &amp;{-5(3) = -15} \\ {5(-3) = -15} &amp;{(-5)(-3) = 15} \end{array}\]</p>'
    # tree = html_to_element(html)
    # print(tree.text)

    # raw_html_path = base_dir.joinpath('assets/ccmath/mathjax-mml-chtml.html')
    # raw_html = raw_html_path.read_text()
    # from llm_web_kit.libs.html_utils import build_html_tree
    # tree = build_html_tree(raw_html)
    # for node in tree.iter():
    #     print(node.tag)

    # c = TestCCMATH()
    # c.setUp()
    # c.test_mml_to_latex()
