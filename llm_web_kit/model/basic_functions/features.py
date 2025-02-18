import math
import re
from collections import Counter, defaultdict
from itertools import islice
from typing import List, Union

import numpy as np

import llm_web_kit.model.basic_functions as bfuncs
from llm_web_kit.model.basic_functions.utils import (dict_wrapper, div_zero,
                                                     jieba_lcut)

"""
文本长度
"""


# 文本总字符数
def get_content_len(content: str) -> int:
    return len(content)


# 文本非空格字符数（因为正则化之后的文本，只考虑去除空格）
def get_content_len_without_space(content: str) -> int:
    return len(re.sub(r'\s', '', content))


"""
文本行数
"""


# 文本正则之后只考虑\n
def content2lines(content: str) -> List[str]:
    return [line.strip() for line in content.split('\n') if len(line.strip()) > 0]


def get_lines_num(content: str) -> int:
    return len(content2lines(content))


"""
文本分词数
"""


# 转换成词列表
# alpha表示去除数字、标点空格等
def content2words(content: str, alpha: bool = False) -> List[str]:
    seg_list = jieba_lcut(content)
    word_list = [w for w in seg_list if w.strip()]
    if alpha:
        return [w for w in word_list if w.isalpha()]
    else:
        return word_list


"""
最长连续空格数
"""


@dict_wrapper(['max_continue_space_num'])
def stats_continue_space(content: str) -> int:
    """
    统计文本中连续空格的数量
    Args:
        content_str: str 输入文本
    Returns:
        continue_space_num: int 连续空格的数量
    """
    pattern = re.compile(r'\s+')
    matches = pattern.findall(content)
    max_continue_space_num = 0
    for match in matches:
        length = len(match)
        max_continue_space_num = max(max_continue_space_num, length)
    return max_continue_space_num


"""
信息熵
"""


@dict_wrapper(['entropy'])
def stats_entropy(content: str) -> float:
    """计算文本的熵值（信息熵）"""

    # 计算每个字符的频数
    freq = Counter(content)
    total_chars = len(content)

    # 计算熵
    entropy = 0.0
    for count in freq.values():
        p_x = div_zero(count, total_chars)
        entropy -= p_x * math.log2(p_x)

    return entropy


"""
标点结尾的行数和占比
"""


@dict_wrapper(
    ['punc_end_sentence_num', 'punc_end_sentence_mean_len', 'longest_punc_sentence_len']
)
def stats_punctuation_end_sentence(content: str):
    """
    统计以终止标点符号结尾的句子数量、比例、长度比例、总行数、总字符数
    定义: 'punc_end_sentence_ratio'为平均每行以终止标点符号结尾的句子数量.
    """
    lines = content2lines(content)
    punc_sentences = []

    for line in lines:
        while len(line) > 0:
            # find the first punctuation in punctuation_set
            for i in range(len(line)):
                if line[i] in bfuncs.character.get_common_punc_end_list():
                    break
            punc_sentences.append(line[: i + 1])
            line = line[i + 1 :]

    # 去除空字符串
    punc_sentences = [sentence for sentence in punc_sentences if sentence != '']
    # print(punc_sentences)

    punc_end_sentence_num = 0
    punc_end_sentence_length = 0
    longest_punc_sentence_len = 0

    for sentence in punc_sentences:
        sentence = sentence.strip()
        longest_punc_sentence_len = max(
            len(sentence.encode('utf-8')), longest_punc_sentence_len
        )
        if sentence[-1] in bfuncs.character.get_common_punc_end_list():
            punc_end_sentence_num += 1
            punc_end_sentence_length += len(re.sub(r'\s', '', sentence))

    punc_end_sentence_mean_len = div_zero(
        punc_end_sentence_length, punc_end_sentence_num
    )

    return punc_end_sentence_num, punc_end_sentence_mean_len, longest_punc_sentence_len


"""
停用词数和停用词占比
"""


@dict_wrapper(['stop_word_num', 'stop_word_frac'])
def stats_stop_words(
    content: str, stop_word_list: set = bfuncs.word.get_stop_word_en_zh_set()
):
    """给定文本中停用词的数量及其在文本中的比例，停用词长度占比，总单词数量，停用词总长度，总字符数。"""
    # 注释：这里的总长度只包含内容文本（即不包含数字、标点等等）
    word_list = content2words(content, alpha=True)
    word_list = [word.lower() for word in word_list]
    words_in_stop_word_list = [word for word in word_list if word in stop_word_list]
    # print(words_in_stop_word_list)

    stop_word_num = len(words_in_stop_word_list)
    word_num = len(word_list)

    # stop_word_length = sum([len(word) for word in words_in_stop_word_list])
    # total_word_length = sum([len(word) for word in word_list])

    stop_word_frac = div_zero(stop_word_num, word_num)
    # stop_word_length_ratio = div_zero(stop_word_length, total_word_length)

    return stop_word_num, stop_word_frac


"""
项目符号开头行占比
"""


BULLET_POINT_SYMBOLS = (
    '\u2022',  # bullet point
    '\u2023',  # triangular bullet point
    '\u25b6',  # black right pointing triangle
    '\u25c0',  # black left pointing triangle
    '\u25e6',  # white bullet point
    '\u25a0',  # black square
    '\u25a1',  # white square
    '\u25aa',  # black small square
    '\u25ab',  # white small square
    '\u2013',  # en dash
)


"""
html entity
"""


HTML_ENTITY_LIST = [
    'nbsp',
    'lt',
    'gt',
    'amp',
    'quot',
    'apos',
    'hellip',
    'ndash',
    'mdash',
    'lsquo',
    'rsquo',
    'ldquo',
    'rdquo',
]


@dict_wrapper(['html_semi_entity_count', 'html_semi_entity_frac'])
def stats_html_entity(content: str):
    """
    统计文本中的html entity数量
    Args:
        input_text: str 输入文本
    Returns:
        html_entity_count: int 完整匹配html entity数量
        html_semi_entity_count: int 部分匹配html entity数量（不包含分号或不包含前后字符）
        html_bare_entity_count: int 纯html entity数量（不包含前后字符）
    """
    content_len = get_content_len_without_space(content)

    html_semi_entity_count = 0
    html_semi_entity_len = 0

    # pattern = re.compile(r"([&＆])(" + "|".join(HTML_ENTITY_LIST + HTML_NORMAL_ENTITY_LIST) + r")(;|；)")
    # html_entity_count = len(pattern.findall(clean_text))

    pattern = re.compile(r'([&＆])(' + '|'.join(HTML_ENTITY_LIST) + r')(?![a-zA-Z0-9])')
    match_list = pattern.findall(content)
    html_semi_entity_count += len(match_list)
    html_semi_entity_len += sum([len(x) for x in match_list])

    pattern = re.compile(r'(?<![a-zA-Z0-9])(' + '|'.join(HTML_ENTITY_LIST) + r')(;|；)')
    match_list = pattern.findall(content)
    html_semi_entity_count += len(match_list)
    html_semi_entity_len += sum([len(x) for x in match_list])

    # pattern = re.compile(r"(?<![a-zA-Z0-9])(" + "|".join(HTML_ENTITY_LIST) + r")(?![a-zA-Z0-9])")
    # html_bare_entity_count = len(pattern.findall(clean_text))

    html_semi_entity_frac = div_zero(html_semi_entity_len, content_len)

    return html_semi_entity_count, html_semi_entity_frac


def split_zh_en_mixed_text(text: str) -> List[str]:
    # "abc1我的ni 1,bd2 一个短语在这里"
    # -> ['abc1', '我的', 'ni', '1', 'bd2', '一个', '短语', '在', '这里']
    # 先把用单词的边界匹配把中英文数字的连续片段分开
    words_and_numbers = re.findall(r'\b\w+\b', text)
    splited_words = []
    for word in words_and_numbers:
        # 使用jieba分词
        if not bfuncs.character.has_chinese_char(word):
            splited_words.append(word)
            continue
        splited_words.extend(jieba_lcut(word))
    return splited_words


"""
unicode 码值相关
"""


@dict_wrapper(['std_dev_unicode_value', 'mean_diff_unicode_value'])
def stats_unicode(content):
    # 转换每个字符为其 UTF-8 编码值
    unicode_values = [ord(c) for c in content]

    # 计算标准差
    std_dev_unicode_value = np.std(unicode_values)

    # 计算相邻两个字符的 UTF-8 编码值之差
    diff_values = [
        unicode_values[i + 1] - unicode_values[i]
        for i in range(len(unicode_values) - 1)
    ]

    # 计算差值的平均值
    mean_diff_unicode_value = div_zero(sum(diff_values), len(diff_values))

    return std_dev_unicode_value, mean_diff_unicode_value


"""
ngram 重复度
"""


def window(seq, n=2):
    """Returns a sliding window (of width n) over data from the iterable."""
    '   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   '
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def max_ngram_dup_fraction(n: int):
    def calc(tokens: Union[str, list]) -> float:
        d = defaultdict(list)

        for i, ngram in enumerate(window(tokens, n)):
            d[ngram].append(range(i, i + n))

        max_dup_len = 0
        for ngram, pos_list in d.items():
            if len(pos_list) <= 1:
                continue
            dup_idx = set()
            for ngram_pos in pos_list:
                for i in ngram_pos:
                    dup_idx.add(i)

            dup_lens = map(lambda i: len(tokens[i]), dup_idx)
            max_dup_len = max(max_dup_len, sum(dup_lens))

        total_len = sum(map(lambda t: len(t), tokens))
        if total_len <= 0:
            return 0
        return div_zero(max_dup_len, total_len)

    return calc


def sum_ngram_dup_fraction(n: int):
    def calc(tokens: Union[str, list]) -> float:
        d = defaultdict(list)

        for i, ngram in enumerate(window(tokens, n)):
            d[ngram].append(range(i, i + n))

        dup_idx = set()
        for ngram, pos_list in d.items():
            if len(pos_list) <= 1:
                continue
            for ngram_pos in pos_list:
                for i in ngram_pos:
                    dup_idx.add(i)

        dup_lens = map(lambda i: len(tokens[i]), dup_idx)
        total_dup_len = sum(dup_lens)
        total_len = sum(map(lambda t: len(t), tokens))
        if total_len <= 0:
            return 0
        return div_zero(total_dup_len, total_len)

    return calc


@dict_wrapper(['dup_top_2gram', 'dup_top_4gram', 'dup_10gram'])
def stats_ngram_mini(content: str):
    tokens = bfuncs.word.filter_stop_word(split_zh_en_mixed_text(content))
    res_list = []

    for i in [2, 4]:
        value = max_ngram_dup_fraction(i)(tokens)
        res_list.append(value)

    for i in [10]:
        value = sum_ngram_dup_fraction(i)(tokens)
        res_list.append(value)

    return tuple(res_list)


"""
公式相关
"""


def extract_formulas(text):
    # 提取行内公式（用$...$包围）
    inline_formulas = re.findall(r'\$(.*?)\$', text)
    # 提取块级公式（用$$...$$包围）
    block_formulas = re.findall(r'\$\$(.*?)\$\$', text)
    res_inline = [formula for formula in inline_formulas if formula.strip()]
    res_block = [formula for formula in block_formulas if formula.strip()]
    return res_inline, res_block


def formula_count_features(inline_formulas, block_formulas):
    # inline_formulas, block_formulas = extract_formulas(text)

    inline_count = len(inline_formulas)
    block_count = len(block_formulas)
    total_formulas = inline_count + block_count

    return {
        'inline_formula_count': inline_count,
        'block_formula_count': block_count,
        'total_formula_count': total_formulas
    }


def formula_complexity_features(inline_formulas, block_formulas):
    # inline_formulas, block_formulas = extract_formulas(text)
    all_formulas = inline_formulas + block_formulas

    # 计算公式的长度
    formula_lengths = [len(formula) for formula in all_formulas]
    average_formula_length = sum(formula_lengths) / len(formula_lengths) if formula_lengths else 0

    # 统计操作符数量
    operator_pattern = r'[+\-*/=]|\\(sum|int|frac|sqrt|sin|cos|log|times|gamma|alpha)'
    operator_counts = [len(re.findall(operator_pattern, formula)) for formula in all_formulas]
    average_operator_count = sum(operator_counts) / len(operator_counts) if operator_counts else 0

    return {
        'average_formula_length': average_formula_length,
        'average_operator_count': average_operator_count
    }


def formula_distribution_var(content_lines):
    # 查找所有公式的位置（行号）
    # lines = text.splitlines()
    formula_lines = []
    for i, line in enumerate(content_lines):
        if re.search(r'\$.*\$', line):
            formula_lines.append(i)

    if not formula_lines:
        return 0

    variance = np.var(formula_lines)
    return variance


def formula_type_ratios(inline_formulas, block_formulas):
    # inline_formulas, block_formulas = extract_formulas(text)
    all_formulas = inline_formulas + block_formulas

    integral_count = sum(1 for formula in all_formulas if r'\int' in formula)
    derivative_count = sum(1 for formula in all_formulas if r'\frac{\partial' in formula or r'\dot{' in formula)
    matrix_count = sum(1 for formula in all_formulas if r'\mathbf{' in formula or r'\det' in formula)

    total_formulas = len(all_formulas)

    return {
        'integral_formula_ratio': integral_count / total_formulas if total_formulas else 0,
        'derivative_formula_ratio': derivative_count / total_formulas if total_formulas else 0,
        'matrix_formula_ratio': matrix_count / total_formulas if total_formulas else 0
    }
