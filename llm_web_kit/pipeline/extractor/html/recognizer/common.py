from py_asciimath.translator.translator import ASCIIMath2Tex

asciimath2tex = ASCIIMath2Tex(log=False)


def extract_asciimath(s: str) -> str:
    parsed = asciimath2tex.translate(s)
    return parsed


def text_strip(text):
    return text.strip() if text else text
