import re


def __normalize_ctl_char(char: str, before: str) -> str:
    """处理空白字符，将各种空白字符规范化处理.

    Args:
        char: 当前字符
        before: 前一个字符

    Returns:
        str: 处理后的字符

    处理规则:
    1. \r\n 组合转换为空字符， 这是windows换行符
    2. \n 和 \r 单独出现时转换为 \n， 这是unix风格换行符
    3. \t 保持不变
    4. 控制字符(\u0000-\u001f)转换为空字符， 这些字符是不可见的
    5. 特殊控制字符(\u007f-\u009f)转换为空字符， 这些字符是不可见的
    6. 零宽字符和其他特殊空白(\u200b,\u2408,\ufeff)转换为空字符， 这些字符是不可见的
    7. 各种宽度空格(\u2002-\u200a)转换为普通空格
    8. 其他特殊空格字符转换为普通空格
    9. Unicode私有区域中的特殊空格转换为普通空格
    10. 其他字符保持不变
    """
    # 处理 \r\n 组合
    if char == '\n' and before == '\r':
        return ''

    # 处理换行符
    if char in ['\n', '\r']:
        return '\n'

    # 保持制表符不变
    if char == '\t':
        return '\t'

    # 处理控制字符
    if '\u0000' <= char < '\u0020':
        return ''

    # 处理特殊控制字符
    if '\u007f' <= char <= '\u009f':
        return ''

    # 处理零宽字符和其他特殊空白
    if char in ['\u200b', '\u2408', '\ufeff']:
        return ''

    # 处理各种宽度空格
    if '\u2002' <= char <= '\u200a':
        return ' '

    # 处理其他特殊空格字符
    if char in ['\u00a0', '\u202f', '\u205f', '\u2420', '\u3000', '\u303f']:
        return ' '

    # 处理Unicode私有区域中的特殊空格
    if char in ['\U0001da7f', '\U0001da80', '\U000e0020']:
        return ' '

    # 其他字符保持不变
    return char


def __normalize_space_sequence(text:str) -> str:
    """处理空白字符，将连续的空白字符转换为1个空白字符.

    \u00a0 代表html的&nbsp;
    Args:
        text: 文本

    Returns:
        str: 处理后的字符
    """
    new_s = re.sub(r'[ \t\u00a0]+', ' ', text)
    return new_s


def normalize_text_segment(text:str) -> str:
    """对文本进行处理，将连续的空格字符转换为1个空格字符.

    Args:
        text: 文本

    Returns:
        str: 处理后的文本
    """
    ret = ''
    for i in range(len(text)):
        if i == 0:
            ret += __normalize_ctl_char(text[i], '')
        else:
            ret += __normalize_ctl_char(text[i], text[i - 1])

    ret = __normalize_space_sequence(ret)
    return ret


def collapse_dup_newlines(text:str) -> str:
    return re.sub(r'\n{2,}', '\n', text)
