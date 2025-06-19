import os
import time
from typing import Any, Dict, Tuple

import ahocorasick

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.exception.exception import SafeModelException
from llm_web_kit.libs.standard_utils import json_loads
from llm_web_kit.model.basic_functions.format_check import (is_en_letter,
                                                            is_pure_en_word)
from llm_web_kit.model.resource_utils import (CACHE_DIR, download_auto_file,
                                              singleton_resource_manager)

xyz_language_lst = [
    'ar',
    'cs',
    'hu',
    'sr',
    'ru',
    'ko',
    'vi',
    'th',
    'arb',
    'arb_Arab',
    'arb_Latn',
    'ces',
    'ces_Latn',
    'hun',
    'hun_Latn',
    'srp',
    'srp_Cyrl',
    'rus',
    'rus_Cyrl',
    'kor',
    'kor_Hang',
    'vie',
    'vie_Latn',
    'tha',
    'tha_Thai',
]
level_score_map = {
    'L1': 100,
    'L2': 10,
    'L3': 1,
    'L4': 0.1,
}


def auto_download(language='zh-en'):
    resource_config = load_config()['resources']
    if language == 'zh-en':
        resource_name = 'unsafe_words'
    elif language == 'xyz':
        resource_name = 'xyz_internal_unsafe_words'
    else:
        raise SafeModelException(f'Unsupported language: {language}')
    language_unsafe_words_config: Dict = resource_config[resource_name]
    download_path = language_unsafe_words_config['download_path']
    md5 = language_unsafe_words_config['md5']
    local_path = os.path.join(CACHE_DIR, resource_name)
    unsafe_words_file_path = download_auto_file(download_path, local_path, md5)
    return unsafe_words_file_path


def get_ac(language='zh-en'):
    t1 = time.time()
    unsafe_words_file_path = auto_download(language)
    t2 = time.time()
    print(
        f'-----------------auto_download cost time: {t2 - t1} , language: {language}------------------'
    )
    with open(unsafe_words_file_path, 'r') as f:
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
        if w.get('tag') == 'delete':
            continue
        word = str(w.get('word') or '').lower()
        if not word:
            continue
        if is_pure_en_word(word) and len(word) <= 4:
            continue

        sub_words = word.split('&&&')

        w_info = {
            'word': word,
            'sub_words': set(sub_words),
            'type': w.get('type'),
            'level': w.get('level'),
            'language': w.get('language'),
            'applicable': w.get('applicable'),
            'unapplicable': w.get('unapplicable'),
        }

        for sub_word in sub_words:
            lst = words.get(sub_word, [])
            lst.append({'sub_word': sub_word, **w_info})
            words[sub_word] = lst

    ac = ahocorasick.Automaton()
    for word, w_info_lst in words.items():
        ac.add_word(word, w_info_lst)
    ac.make_automaton()
    return ac


def get_unsafe_words(ac, content: str) -> list:
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

    all_sub_words = set()  # 记录所有独立出现的子词
    all_w_info_lst = []  # 记录所有子词的详细信息
    # 遍历所有匹配的子词及其结束位置pos
    for pos, w_info_lst in ac.iter(content):
        for w_info in w_info_lst:
            sub_word = w_info['sub_word']
            if is_word_standalone(sub_word, pos):
                all_sub_words.add(sub_word)
                all_w_info_lst.append(w_info)

    unsafe_words = {}
    for w_info in all_w_info_lst:
        # 检查该词的所有子词是否均被匹配到
        if all_sub_words.issuperset(w_info['sub_words']):
            if w_info['word'] not in unsafe_words:
                unsafe_words[w_info['word']] = {
                    'word': w_info['word'],
                    'type': w_info['type'],
                    'level': w_info['level'],
                    'language': w_info['language'],
                    'count': 0.0,
                }
            unsafe_words[w_info['word']]['count'] += 1.0 / len(w_info['sub_words'])
    return list(unsafe_words.values())


class UnsafeWordChecker:
    def __init__(self, language='zh-en') -> None:
        t1 = time.time()
        self.ac = get_ac(language)
        t2 = time.time()
        print(
            f'---------------UnsafeWordChecker init time: {t2 - t1} , language: {language}-----------------'
        )

    def check_unsafe_words(self, content_str: str) -> list:
        unsafe_words_list = get_unsafe_words(self.ac, content=content_str)
        return unsafe_words_list


def get_unsafe_words_checker(language='zh-en') -> UnsafeWordChecker:
    if not singleton_resource_manager.has_name(language):
        singleton_resource_manager.set_resource(language, UnsafeWordChecker(language))
    return singleton_resource_manager.get_resource(language)


def decide_content_unsafe_word_by_data_checker(
    content_str: str, unsafeWordChecker: UnsafeWordChecker
) -> str:
    unsafe_words_list = unsafeWordChecker.check_unsafe_words(content_str=content_str)
    unsafe_word_levels = []
    for w in unsafe_words_list:
        _, level, _ = w['word'], w['level'], w['count']
        # "涉政|观测|L4|带头人"
        unsafe_word_levels.append(level)

    unsafe_word_levels = list(set(unsafe_word_levels))
    unsafe_word_min_level = min(unsafe_word_levels + ['NF'])

    return unsafe_word_min_level


class UnsafeWordsFilter:
    def __init__(self,raise_not_support_language_exception: bool = False):
        self.raise_not_support_language_exception = raise_not_support_language_exception

    def filter(
        self,
        content_str: str,
        language: str,
        language_details: str,
        content_style: str,
        from_safe_source: bool,
        from_domestic_source: bool,
    ) -> Tuple[bool, Dict[str, Any]]:
        if language in xyz_language_lst:
            language = 'xyz'
        elif language in [
            'zh',
            'en',
            'yue',
            'zho',
            'eng',
            'zho_Hans',
            'zho_Hant',
            'yue_Hant',
            'eng_Latn',
        ]:
            language = 'zh-en'
        else:
            if self.raise_not_support_language_exception:
                raise SafeModelException(f'Unsupported language: {language}')
            else:
                return True, {'hit_unsafe_words': False}

        if from_safe_source:
            return True, {'hit_unsafe_words': False}
        if from_domestic_source:
            unsafe_range = ('L1',)
        else:
            unsafe_range = ('L1', 'L2')
        unsafe_word_min_level = decide_content_unsafe_word_by_data_checker(
            content_str, get_unsafe_words_checker(language)
        )
        hit = unsafe_word_min_level in unsafe_range
        return not hit, {'hit_unsafe_words': hit}
