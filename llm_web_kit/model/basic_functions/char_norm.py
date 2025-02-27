import re

# tab is not handled
line_breaks_re = r'[\n\v\f\r\x85\u2028\u2029]'
visible_spaces_re = r'[\x20\xa0\u2000-\u200a\u202f\u205f\u3000]'
invisible_spaces_re = r'[\u200b-\u200d\u2060\ufeff]'
invisible_chars_re = r'[\xad\ufffc\u2061-\u2063]'
other_controls_re = r'[\x00-\x08\x0e-\x1f\x7f-\x84\x86-\x9f]'
direction_controls_re = r'[\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]'
head_view_invisible_spaces_re = r'^[\x20\xa0\u2000-\u200a\u202f\u205f\u3000 ]'

ar_invisible_spaces_re = r'[\u2060\ufeff]'
ar_direction_controls_re = r'[\u061c\u202c\u2066-\u2069]'

private_use_area_pattern = (
    r'[\uE000-\uF8FF]'  # BMP 私有使用区
    r'|[\U000F0000-\U000FFFFD]'  # 辅助平面 A 私有使用区
    r'|[\U00100000-\U0010FFFD]'  # 辅助平面 B 私有使用区
)

# 汉字区块（一部分）
chinese_pattern = (
    r'[\u4E00-\u9FFF\u3400-\u4DBF\u2F00-\u2FDF\u2E80-\u2EFF\uF900-\uFAFF\u31c0-\u31ef]'
)

# 部分补充汉字区块
supp_chinese_pattern = re.compile(
    r'['
    '\U00020000-\U0002a6df'
    '\U0002a700-\U0002b73f'
    '\U0002b740-\U0002b81f'
    '\U0002b820-\U0002ceaf'
    '\U0002ceb0-\U0002ebef'
    '\U00030000-\U0003134f'
    '\U0002f800-\U0002fa1f'
    ']',
    flags=re.UNICODE,
)

# 汉字基本区块
chinese_base_pattern = r'[\u4E00-\u9FFF]'

# 全角符号
full_width_punc_pattern = r'[\uFF01-\uFF0F\u3000\uFF1A-\uFF1F\uFF3B-\uFF3D\uFF5B-\uFF5D\u3002\u3001【】《》“”‘’]'

# 英文常见符号
en_common_punc_pattern = r"[\s\\\、.,-:#\*()\'/!?\"&;|$>–%\[\]+—@…<_=~`{}·£€^″′−]"

# 其他西欧语言元音字符
other_vowel_letter_pattern = (
    r'[äöüßéèêëáàâæçœìíîïùúûüýÿñéáüíöóèäñâçàúêôÂÉãåïßëšæāčÃÖβÜə]'
)

# 斯拉夫语言
slavic_pattern = r'[\u0400-\u04FF]'

# 日韩字符
jap_ko_pattern = r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7AF\u1100-\u11FF]'

# 希腊字符
greek_pattern = r'[\u0370-\u03FF]'

# emoji
emoji_pattern = re.compile(
    r'['
    '\U0001f600-\U0001f64f'  # emoticons
    '\U0001f300-\U0001f5ff'  # symbols & pictographs
    '\U0001f680-\U0001f6ff'  # transport & map symbols
    '\U0001f700-\U0001f77f'
    '\U0001f780-\U0001f7ff'
    '\U0001f800-\U0001f8ff'
    '\U0001f900-\U0001f9ff'
    '\U0001fa00-\U0001fa6f'
    '\U0001fa70-\U0001faff'
    '\U0001f1e0-\U0001f1ff'  # flags (iOS)
    '\U00002702-\U000027b0'
    # u"\U000024C2-\U0001F251"
    '\U00002300-\U000023ff' ']',
    flags=re.UNICODE,
)

# character_normalize #


ESCAPED_CHARS = r'\`*_{}[]()>#.!+-'

_ZH_END_MARKS = ('。', '？', '！', '”', '：', '；')
_ZH_FINISH_END_MARKS = ('。', '？', '！', '”')

_EN_END_MARKS = ('.', '?', '!', '"', ',', ':')
_EN_FINISH_END_MARKS = ('.', '?', '!', '"')

ALL_END_MARKS = _ZH_END_MARKS + _EN_END_MARKS
ALL_FINISH_END_MARKS = _ZH_FINISH_END_MARKS + _EN_FINISH_END_MARKS

ALL_MD_END_MARKS = tuple([f'\\{c}' if c in ESCAPED_CHARS else c for c in ALL_END_MARKS])
ALL_MD_FINISH_END_MARKS = tuple(
    [f'\\{c}' if c in ESCAPED_CHARS else c for c in ALL_FINISH_END_MARKS]
)


# def character_normalize(s: str):
#     s = re.sub(r"\r\n", "\n", s)
#     s = re.sub(line_breaks_re, "\n", s)
#     s = re.sub(visible_spaces_re, " ", s)
#     s = re.sub(invisible_spaces_re, "", s)
#     s = re.sub(other_controls_re, "", s)
#     return s


def character_normalize(s: str) -> str:
    """对字符串进行字符级标准化."""
    s = re.sub(r'\r\n', '\n', s)
    s = re.sub(line_breaks_re, '\n', s)
    s = re.sub(visible_spaces_re, ' ', s)
    s = re.sub(head_view_invisible_spaces_re, '', s)
    s = re.sub(invisible_spaces_re, '', s)
    s = re.sub(invisible_chars_re, '', s)
    s = re.sub(other_controls_re, '', s)
    s = re.sub(private_use_area_pattern, '', s)

    return s


def ar_character_normalize(s: str) -> str:
    """对阿拉伯语字符串进行字符级标准化."""
    s = re.sub(r'\r\n', '\n', s)
    s = re.sub(line_breaks_re, '\n', s)
    s = re.sub(visible_spaces_re, ' ', s)
    s = re.sub(head_view_invisible_spaces_re, '', s)
    s = re.sub(ar_invisible_spaces_re, '', s)
    s = re.sub(other_controls_re, '', s)
    s = re.sub(private_use_area_pattern, '', s)

    return s
