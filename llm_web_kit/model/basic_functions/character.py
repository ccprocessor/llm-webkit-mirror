import json
import os
import re

RES_MAP = {}


def build_all_punc_list():
    """
    从文件中获取所有的标点符号
    Returns:
        punc_list: list 所有的标点符号信息
    """
    # {"category": "Po", "punc": "。", "name": "IDEOGRAPHIC FULL STOP", "hex": "0x3002", "common_en": false, "common_zh": true, "can_be_begin": false, "can_be_end": true}

    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets/punc_list.jsonl'), 'r') as f:
        lines = f.readlines()
    punc_list = []
    for line in lines:
        punc_list.append(json.loads(line.strip()))
    return punc_list


def get_all_punc_list():
    if 'ALL_PUNC_LIST' not in RES_MAP:
        RES_MAP['ALL_PUNC_LIST'] = build_all_punc_list()
    return RES_MAP['ALL_PUNC_LIST']


def get_punc_set(include_keys: list = None, exclude_keys: list = None) -> set:
    """
    从ALL_PUNC_LIST中获取特定类型的标点符号
    include_keys and exclude_keys 表示需要具有的属性和不需要具有的属性（取与逻辑）
    属性仅为 en_cc_top_30, zh_cc_top_30, en_cc_end_top_30, zh_cc_end_top_30
    Args:
        include_keys: list 需要具有的属性
        exclude_keys: list 不需要具有的属性
    Returns:
        result_set: list 符合条件的标点符号列表
    """
    valid_keys = [
        'en_cc_top_30',
        'zh_cc_top_30',
        'en_cc_end_top_30',
        'zh_cc_end_top_30',
    ]
    if include_keys is None:
        include_keys = []
    if exclude_keys is None:
        exclude_keys = []
    assert all([key in valid_keys for key in include_keys])
    assert all([key in valid_keys for key in exclude_keys])
    result_set = set()
    for punc in get_all_punc_list():
        include_flag = all([punc[key] for key in include_keys])
        exclude_flag = not any([punc[key] for key in exclude_keys])
        if include_flag and exclude_flag:
            result_set.add(punc['punc'])
    return result_set


def get_common_punc_list():
    if 'COMMON_PUNCTUATION_LIST' not in RES_MAP:
        RES_MAP['COMMON_PUNCTUATION_LIST'] = list(
            get_punc_set(include_keys=['en_cc_top_30']).union(
                get_punc_set(include_keys=['zh_cc_top_30'])
            )
        )
    return RES_MAP['COMMON_PUNCTUATION_LIST']


def get_common_punc_end_list():
    if 'COMMON_PUNCTUATION_END_LIST' not in RES_MAP:
        RES_MAP['COMMON_PUNCTUATION_END_LIST'] = list(
            get_punc_set(include_keys=['en_cc_end_top_30']).union(get_punc_set(include_keys=['zh_cc_end_top_30']))
        )
    return RES_MAP['COMMON_PUNCTUATION_END_LIST']


def has_chinese_char_closure():
    pattern = re.compile(r'[\u4e00-\u9fa5]')

    def has_chinese_char(text: str) -> bool:
        return pattern.search(text) is not None

    return has_chinese_char


has_chinese_char = has_chinese_char_closure()
