

xyz_language_lst = ["ar", "cs", "hu", "sr", "ru", "ko", "vi", "th"]


######## todo：跑通后删掉本句   原decide_unsafe_words.py #############

from typing import Any, Dict

# from app.common.unsafe_words import get_ac, get_unsafe_words

from ..core.content import get_text_content
# from ..core.definitions import xyz_language_lst

_global_unsafe_words_detect = []


class UnsafeWordChecker:
    def __init__(self, language="zh-en") -> None:
        self.ac = get_ac(language)

    def check_unsafe_words(self, content_str: str, data_source: str) -> list:
        unsafe_words_list = get_unsafe_words(self.ac, content=content_str, data_source=data_source)
        return unsafe_words_list


def get_unsafe_words_checker(language="zh-en") -> UnsafeWordChecker:
    if len(_global_unsafe_words_detect) == 0:
        _global_unsafe_words_detect.append(UnsafeWordChecker(language))
    return _global_unsafe_words_detect[0]


def release_unsafe_checker():
    while len(_global_unsafe_words_detect) > 0:
        del _global_unsafe_words_detect[0]


def decide_unsafe_word_by_data_checker(data_dict: dict, unsafeWordChecker: UnsafeWordChecker) -> str:
    content_str = get_text_content(data_dict.get("content_list"))
    data_source = data_dict.get("data_source")
    unsafe_words_list = unsafeWordChecker.check_unsafe_words(content_str=content_str, data_source=data_source)
    unsafe_word_levels = []

    for w in unsafe_words_list:
        word, level, count = w["word"], w["level"], w["count"]
        # "涉政|观测|L4|带头人"
        unsafe_word_levels.append(level)

    unsafe_word_levels = list(set(unsafe_word_levels))
    unsafe_word_min_level = min(unsafe_word_levels + ["NF"])

    return unsafe_word_min_level


def decide_unsafe_word_data_dict(data_dict: dict) -> str:
    language = data_dict.get("language", "zh-en")
    if language in xyz_language_lst:
        language = "xyz"

    unsafeWordChecker = get_unsafe_words_checker(language)
    unsafe_word_min_level = decide_unsafe_word_by_data_checker(data_dict=data_dict, unsafeWordChecker=unsafeWordChecker)

    return unsafe_word_min_level


def update_unsafe_word_by_data_dict(data_dict: dict) -> Dict[str, Any]:
    unsafe_word_min_level = decide_unsafe_word_data_dict(data_dict=data_dict)
    return {"unsafe_word_min_level": unsafe_word_min_level}


def get_zh_en_unsafe_fields(data_dict: dict):
    labels_dict = data_dict.get("labels", {})
    unsafe_word_min_level = labels_dict.get("unsafe_word_min_level", "")
    from_safe_source = labels_dict.get("from_safe_source", False)
    from_domestic_source = labels_dict.get("from_domestic_source", False)

    return unsafe_word_min_level, from_safe_source, from_domestic_source


def get_xyz_unsafe_fields(data_dict: dict):
    labels_dict = data_dict.get("labels", {})
    unsafe_word_min_level = labels_dict.get("unsafe_word_min_level", "")

    return unsafe_word_min_level, False, True


def check_unsafe_word(data_dict: Dict[str, Any]) -> bool:
    """
    input: data_dict: Dict[str, Any]
    output: bool (True: unsafe, False: safe)
    description: check if the content is safe。
    """
    language = data_dict.get("language", "")
    if language in xyz_language_lst:
        unsafe_word_min_level, from_safe_source, from_domestic_source = get_xyz_unsafe_fields(data_dict)
    else:
        unsafe_word_min_level, from_safe_source, from_domestic_source = get_zh_en_unsafe_fields(data_dict)

    if from_safe_source:
        return False
    if from_domestic_source:
        unsafe_range = ("L1",)
    else:
        unsafe_range = ("L1", "L2")
    return unsafe_word_min_level in unsafe_range


######## todo：跑通后删掉本句   原unsafe_words.py #############


from typing import Optional

from app.common.asset_util import get_asset
from app.common.json_util import *


def is_en_letter(c: str):
    return ("a" <= c <= "z") or ("A" <= c <= "Z")


def is_space(c: str):
    return c in [" ", "\t"]


def is_pure_en_word(s: str):
    for c in s:
        if is_en_letter(c) or is_space(c):
            continue
        return False
    return True


def get_ac(language="zh-en"):
    import ahocorasick

    if language == "xyz":
        with open(get_asset("assets/xyz_internal_unsafe_words.jsonl"), "r") as f:
            lines = f.readlines()
    else:
        with open(get_asset("assets/unsafe_words.jsonl"), "r") as f:
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
        if is_pure_en_word(sub_word):
            prev_pos = end_pos - len(sub_word)
            if prev_pos >= 0 and is_en_letter(content[prev_pos]):
                return False
            post_pos = end_pos + 1
            if post_pos < len(content) and is_en_letter(content[post_pos]):
                return False
        return True

    all_sub_words = set()
    all_w_info_lst = []
    for pos, w_info_lst in ac.iter(content):
        for w_info in w_info_lst:
            sub_word = w_info["sub_word"]
            if is_word_standalone(sub_word, pos):
                all_sub_words.add(sub_word)
                all_w_info_lst.append(w_info)

    unsafe_words = {}
    for w_info in all_w_info_lst:
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


def add_partition_unsafe_words(iter):
    from pyspark.sql import Row

    ac = get_ac()
    for row in iter:
        d = json_loads(row.value)
        d["unsafe_words"] = get_unsafe_words(ac, d["content"], d.get("data_source"))
        yield Row(value=json_dumps(d))


level_score_map = {
    "L1": 100,
    "L2": 10,
    "L3": 1,
    "L4": 0.1,
}


def get_unsafe_words_metric(unsafe_words: list, token_len: int):
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


def add_unsafe_words_metric(row):
    from pyspark.sql import Row

    d = json_loads(row.value)
    m = get_unsafe_words_metric(d["unsafe_words"], len(d["content"]))

    d.update(m)
    return Row(value=json_dumps(d))


if __name__ == "__main__":
    from pprint import pprint

    content = "习近平讲话"
    unsafe_words = get_unsafe_words(get_ac(), content, "cn-weixin")
    pprint(unsafe_words)
    metrics = get_unsafe_words_metric(unsafe_words, len(content))
    pprint(metrics)
