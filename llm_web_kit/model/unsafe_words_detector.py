import os
from typing import Optional
from typing import Any, Dict

# from networkx import load_centrality
# from app.common.asset_util import get_asset
# from app.common.json_util import *
from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.standard_utils import json_loads, json_dumps
from llm_web_kit.model.resource_utils.download_assets import (
    CACHE_DIR,
    download_auto_file,
)
from llm_web_kit.model.basic_functions.format_check import *

xyz_language_lst = ["ar", "cs", "hu", "sr", "ru", "ko", "vi", "th"]
level_score_map = {
    "L1": 100,
    "L2": 10,
    "L3": 1,
    "L4": 0.1,
}

_global_unsafe_words_detect = {}


def auto_download(language="zh-en"):
    resource_config = load_config()["resources"]
    if language == "zh-en":
        resource_name = "unsafe_words.jsonl"
    elif language == "xyz":
        resource_name = "xyz_internal_unsafe_words.jsonl"
    else:
        raise ValueError(
            f"Unsupported language: {language}"
        )  # todo : 换成llm_web_kit/exception/exception.py里面的异常
    language_unsafe_words_config: Dict = resource_config[resource_name]
    download_path = language_unsafe_words_config["download_path"]
    md5 = language_unsafe_words_config["md5"]
    local_path = os.path.join(CACHE_DIR, resource_name)
    unsafe_words_file_path = download_auto_file(download_path, local_path, md5)
    return unsafe_words_file_path


def get_ac(language="zh-en"):
    import ahocorasick

    unsafe_words_file_path = auto_download(language)
    with open(unsafe_words_file_path, "r") as f:
        lines = f.readlines()

    # sub_word: [{
    #   "word": "席源评",
    #   "sub_words": ["席源评"],
    #   "type": "涉政",
    #   "level": "L3",
    #   "language": "zh",
    # }, {
    #   ...
    # }]
    words = {}
    for line in lines:
        w = json_loads(line)
        word = str(w.get("word") or "").lower()
        if not word:
            continue
        if is_pure_en_word(word) and len(word) <= 4:
            continue

        sub_words = word.split("&&&")

        w_info = {
            "word": word,
            "sub_words": set(sub_words),
            "type": w.get("type"),
            "level": w.get("level"),
            "language": w.get("language"),
            "applicable": w.get("applicable"),
            "unapplicable": w.get("unapplicable"),
        }

        for sub_word in sub_words:
            lst = words.get(sub_word, [])
            lst.append({"sub_word": sub_word, **w_info})
            words[sub_word] = lst

    ac = ahocorasick.Automaton()
    for word, w_info_lst in words.items():
        ac.add_word(word, w_info_lst)
    ac.make_automaton()
    return ac


def get_unsafe_words(ac, content: str, data_source: Optional[str]) -> list:
    content = content.lower()

    def is_word_standalone(sub_word, end_pos):
        # 检查子词是否为独立英文单词（前后无其他英文字符）
        if is_pure_en_word(sub_word):
            prev_pos = end_pos - len(sub_word)
            # 检查前一个字符是否为英文字母
            if prev_pos >= 0 and is_en_letter(content[prev_pos]):
                return False
            # 检查后一个字符是否为英文字母
            post_pos = end_pos + 1
            if post_pos < len(content) and is_en_letter(content[post_pos]):
                return False
        return True  # 子词是独立的

    all_sub_words = set()   # 记录所有独立出现的子词
    all_w_info_lst = []     # 记录所有子词的详细信息
    # 遍历所有匹配的子词及其结束位置pos
    for pos, w_info_lst in ac.iter(content):
        for w_info in w_info_lst:
            sub_word = w_info["sub_word"]
            if is_word_standalone(sub_word, pos):
                all_sub_words.add(sub_word)
                all_w_info_lst.append(w_info)

    unsafe_words = {}
    for w_info in all_w_info_lst:
        # 检查该词的所有子词是否均被匹配到  
        if all_sub_words.issuperset(w_info["sub_words"]):
            if data_source is not None:
                if w_info["applicable"] and data_source not in w_info["applicable"]:
                    continue
                if w_info["unapplicable"] and data_source in w_info["unapplicable"]:
                    continue
            if w_info["word"] not in unsafe_words:
                unsafe_words[w_info["word"]] = {
                    "word": w_info["word"],
                    "type": w_info["type"],
                    "level": w_info["level"],
                    "language": w_info["language"],
                    "count": 0.0,
                }
            unsafe_words[w_info["word"]]["count"] += 1.0 / len(w_info["sub_words"])
    return list(unsafe_words.values())


def get_unsafe_words_metric(
    unsafe_words: list, token_len: int
):  # todo：是否还要保留该功能
    """
    根据一段文本命中的敏感词及文本长度，计算敏感词的指标
    :param unsafe_words: 命中的敏感词列表
    :param token_len: 文本长度
    :return: 敏感词指标
    """
    d = {}
    unsafe_word_words = []
    unsafe_word_levels = []
    unsafe_word_l1_words = []
    unsafe_word_l2_words = []
    unsafe_word_l3_words = []
    unsafe_word_l4_words = []

    score = 0
    word_count_dict = {}
    for w in unsafe_words:
        word, level, count = w["word"], w["level"], w["count"]

        # "涉政|观测|L4|带头人"
        w_detail = f'{w["type"]}|{level}|{word}'
        unsafe_word_words.append(w_detail)
        unsafe_word_levels.append(level)

        if level == "L1":
            unsafe_word_l1_words.append(w_detail)
        elif level == "L2":
            unsafe_word_l2_words.append(w_detail)
        elif level == "L3":
            unsafe_word_l3_words.append(w_detail)
        elif level == "L4":
            unsafe_word_l4_words.append(w_detail)

        score += level_score_map[level] * count
        word_count_dict[word] = word_count_dict.get(word, 0) + count

    unsafe_word_levels = list(set(unsafe_word_levels))

    d["unsafe_word_words"] = unsafe_word_words
    d["unsafe_word_levels"] = unsafe_word_levels
    d["unsafe_word_l1_words"] = unsafe_word_l1_words
    d["unsafe_word_l2_words"] = unsafe_word_l2_words
    d["unsafe_word_l3_words"] = unsafe_word_l3_words
    d["unsafe_word_l4_words"] = unsafe_word_l4_words
    d["unsafe_word_min_level"] = min(unsafe_word_levels + ["NF"])
    d["unsafe_word_score"] = score
    d["unsafe_word_density"] = (score / token_len) if token_len > 0 else 0.0
    d["unsafe_word_count"] = word_count_dict

    return d


class UnsafeWordChecker:
    def __init__(self, language="zh-en") -> None:
        self.ac = get_ac(language)

    def check_unsafe_words(self, content_str: str, data_source: str) -> list:
        unsafe_words_list = get_unsafe_words(
            self.ac, content=content_str, data_source=data_source
        )
        return unsafe_words_list


def get_unsafe_words_checker(language="zh-en") -> UnsafeWordChecker:
    if language not in _global_unsafe_words_detect:
        _global_unsafe_words_detect[language] = UnsafeWordChecker(language)
    return _global_unsafe_words_detect[language]


def release_unsafe_checker():
    _global_unsafe_words_detect.clear()


def decide_unsafe_word_by_data_checker(
    data_dict: dict, unsafeWordChecker: UnsafeWordChecker
) -> str:

    data_obj = DataJson(data_dict)
    content_str = data_obj.get_content_list().to_txt()
    # todo：这里强制把data_source设为None，即假设没有data_source，看看有无问题
    data_source = None
    unsafe_words_list = unsafeWordChecker.check_unsafe_words(
        content_str=content_str, data_source=data_source
    )
    unsafe_word_levels = []

    for w in unsafe_words_list:
        word, level, count = w["word"], w["level"], w["count"]
        # "涉政|观测|L4|带头人"
        unsafe_word_levels.append(level)

    unsafe_word_levels = list(set(unsafe_word_levels))
    unsafe_word_min_level = min(unsafe_word_levels + ["NF"])

    return unsafe_word_min_level


def get_zh_en_unsafe_fields(
    data_dict: dict,
):  # todo：如何获得from_safe_source和from_domestic_source待定
    labels_dict = data_dict.get("labels", {})
    unsafe_word_min_level = labels_dict.get("unsafe_word_min_level", "")
    from_safe_source = labels_dict.get("from_safe_source", False)
    from_domestic_source = labels_dict.get("from_domestic_source", False)

    return unsafe_word_min_level, from_safe_source, from_domestic_source


def get_xyz_unsafe_fields(
    data_dict: dict,
):  # todo：如何获得from_safe_source和from_domestic_source待定
    labels_dict = data_dict.get("labels", {})
    unsafe_word_min_level = labels_dict.get("unsafe_word_min_level", "")

    return unsafe_word_min_level, False, True


######## 入口 #############


def unsafe_words_filter(
    data_dict: Dict[str, Any], language: str, content_style: str
) -> str:
    if language in xyz_language_lst:
        language = "xyz"
    elif language in ["zh", "en"]:
        language = "zh-en"
    else:
        return "NF"  # todo: 待讨论  非支持语言直接返回NF，表示未命中敏感词

    unsafeWordChecker = get_unsafe_words_checker(language)
    unsafe_word_min_level = decide_unsafe_word_by_data_checker(
        data_dict=data_dict, unsafeWordChecker=unsafeWordChecker
    )

    return unsafe_word_min_level


def unsafe_words_filter_overall(
    data_dict: Dict[str, Any], language: str, content_style: str
):  # todo ：如何获得from_safe_source和from_domestic_source还没迁，是否要迁
    unsafe_word_min_level = unsafe_words_filter(data_dict=data_dict)

    if language in xyz_language_lst:
        unsafe_word_min_level, from_safe_source, from_domestic_source = (
            get_xyz_unsafe_fields(data_dict)
        )
    else:
        unsafe_word_min_level, from_safe_source, from_domestic_source = (
            get_zh_en_unsafe_fields(data_dict)
        )
    if from_safe_source:
        return False
    if from_domestic_source:
        unsafe_range = ("L1",)
    else:
        unsafe_range = ("L1", "L2")
    hit = unsafe_word_min_level in unsafe_range
    return {"hit_unsafe_words": hit}


# 以下为测试代码 todo：跑通后删掉


if __name__ == "__main__":
    from pprint import pprint

    content = "习近平讲话"
    unsafe_words = get_unsafe_words(get_ac(), content, "cn-weixin")
    pprint(unsafe_words)
    metrics = get_unsafe_words_metric(unsafe_words, len(content))
    pprint(metrics)
