import re


def __normalize_ctl_char(char: str, before: str) -> str:
    """处理空白字符，将各种空白字符规范化处理.

    Args:
        char: 当前字符
        before: 前一个字符

    Returns:
        str: 处理后的字符

    处理规则:
    1. \r\n 组合转换为\n， 这是windows换行符
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
    if char in ['\u200b', '\u2408', '\ufeff', '\u2000', '\u2001', '�', '□']:
        return ''

    # 其他一些乱码字符替换为空
    if char in ['�', '□']:
        return ''

    # 处理各种宽度空格
    if '\u2002' <= char <= '\u200f':
        return ' '

    if '\u2060' <= char <= '\u206f':
        return ''

    # 处理其他特殊空格字符
    if char in ['\u00a0', '\u202f', '\u205f', '\u2420', '\u3000', '\u303f', '\xa0']:
        return ' '

    # 处理Unicode私有区域中的特殊空格
    if char in ['\U0001da7f', '\U0001da80', '\U000e0020']:
        return ' '

    # 其他字符保持不变
    return char


def __ctl_char_to_space(text:str) -> str:
    """将控制字符转换为空格."""
    return re.sub(r'[\r\t\f\v]', ' ', text)


def __blank_sequence_to_space(text:str) -> str:
    """将连续的空格字符转换为1个空格字符."""
    return re.sub(r'[ ]+', ' ', text)


def collapse_dup_newlines(text:str) -> str:
    return re.sub(r'\n{2,}', '\n\n', text)


def normalize_ctl_text(text: str) -> str:
    """处理空白字符，将各种空白字符规范化处理.

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
    return ret


def normalize_math_delimiters(text: str) -> str:
    """将[tex][/tex]和[itex][/itex]格式的数学公式转换为$$..$$和$..$ 格式.

    这是兜底处理，针对公式被br标签分割后没有识别为公式的情况.
    处理两种情况:
    1. 行间公式: [tex]...[/tex] -> $$...$$
    2. 行内公式: [itex]...[/itex] -> $...$
    该方法保留公式内容的原始格式，包括换行符和空格。
    Args:
        text (str): 包含数学公式的文本
    Returns:
        str: 替换数学公式标记后的文本
    """
    import re

    # 替换行间公式 [tex]...[/tex] -> $$...$$
    # 使用非贪婪匹配和DOTALL标志以匹配跨行公式
    display_pattern = re.compile(r'\[tex\](.*?)\[/tex\]', re.DOTALL)
    text = display_pattern.sub(lambda m: f'$${m.group(1).strip()}$$', text)

    # 替换行内公式 [itex]...[/itex] -> $...$
    inline_pattern = re.compile(r'\[itex\](.*?)\[/itex\]', re.DOTALL)
    text = inline_pattern.sub(lambda m: f'${m.group(1).strip()}$', text)

    return text


def normalize_text_segment(text:str) -> str:
    """对文本进行处理，将连续的空格字符转换为1个空格字符.
    2. \t, \r, \f, \v 换成空格
    3. 连续的多个空格换成1个
    4. 连续的多个\n换成2个

    Args:
        text: 文本

    Returns:
        str: 处理后的文本
    """
    ret = normalize_ctl_text(text)  # 处理空白字符，将各种空白字符规范化处理
    ret = __ctl_char_to_space(ret)  # 将控制字符转换为空格
    ret = __blank_sequence_to_space(ret)  # 将连续的空格字符转换为1个空格字符
    ret = collapse_dup_newlines(ret)  # 将连续的\n转换为2个
    return ret
