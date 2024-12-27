import re

from py_asciimath.translator.translator import ASCIIMath2Tex

asciimath2tex = ASCIIMath2Tex(log=False)
color_regex = re.compile(r'\\textcolor\[.*?\]\{.*?\}')


def extract_asciimath(s: str) -> str:
    parsed = asciimath2tex.translate(s)
    return parsed


def text_strip(text):
    return text.strip() if text else text


def wrap_math(s, display=False):
    s = re.sub(r'\s+', ' ', s)
    s = color_regex.sub('', s)
    s = s.replace('$', '')
    s = s.replace('\n', ' ').replace('\\n', '')
    s = s.strip()
    if len(s) == 0:
        return s
    # Don't wrap if it's already in \align
    if 'align' in s:
        return s
    if display:
        return '$$' + s + '$$'
    return '$' + s + '$'
