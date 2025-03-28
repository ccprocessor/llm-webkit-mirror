import ctypes
import os
import pickle
import re
from typing import Any, Dict, Tuple

import pandas as pd

import llm_web_kit.model.basic_functions as bfuncs
from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.exception.exception import (
    CleanModelUnsupportedLanguageException, ModelInputException)
from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.basic_functions.features import (
    BULLET_POINT_SYMBOLS, content2lines, content2words, extract_formulas,
    formula_complexity_features, formula_count_features,
    formula_distribution_var, formula_type_ratios, get_content_len,
    get_content_len_without_space, stats_continue_space, stats_entropy,
    stats_html_entity, stats_ngram_mini, stats_punctuation_end_sentence,
    stats_stop_words, stats_unicode)
from llm_web_kit.model.basic_functions.utils import div_zero
from llm_web_kit.model.resource_utils import (CACHE_DIR, download_auto_file,
                                              get_unzip_dir, unzip_local_file)

_global_quality_model = {}
_model_resource_map = {
    'zh-article': 'zh_en_article',
    'en-article': 'zh_en_article',
    'zh-book': 'zh_en_long_article',
    'zh-paper': 'zh_en_long_article',
    'en-book': 'zh_en_long_article',
    'en-paper': 'zh_en_long_article',
}
threshold_map = {
    'zh_en_article': 0.59,
    'zh_en_long_article': 0.7,
}


class QualityModel:
    def __init__(
        self, language: str = None, content_style: str = None, model_path: str = None
    ) -> None:
        if not model_path:
            model_path = self.auto_download(language, content_style)
        self.quality_model = self._load_model(model_path)

    def auto_download(self, language: str = None, content_style: str = None):
        """Download checkpoint file according to language and content_style,
        default the zh_en_article.zip."""
        if language and content_style:
            resource_name = _model_resource_map[f'{language}-{content_style}']
        else:
            resource_name = 'zh_en_article'
        resource_config = load_config()['resources']
        zh_en_article_config: Dict = resource_config[resource_name]
        zh_en_article_s3 = zh_en_article_config['download_path']
        zh_en_article_md5 = zh_en_article_config.get('md5', '')
        # get the zip path calculated by the s3 path
        zip_path = os.path.join(CACHE_DIR, f'{resource_name}.zip')
        # the unzip path is calculated by the zip path
        unzip_path = get_unzip_dir(zip_path)
        logger.info(f'try to make unzip_path: {unzip_path}')
        # if the unzip path does not exist, download the zip file and unzip it
        if not os.path.exists(unzip_path):
            logger.info(f'unzip_path: {unzip_path} does not exist')
            logger.info(f'try to unzip from zip_path: {zip_path}')
            if not os.path.exists(zip_path):
                logger.info(f'zip_path: {zip_path} does not exist')
                logger.info(f'downloading {zh_en_article_s3}')
                zip_path = download_auto_file(
                    zh_en_article_s3, zip_path, zh_en_article_md5
                )
            logger.info(f'unzipping {zip_path}')
            unzip_path = unzip_local_file(zip_path, unzip_path)
        else:
            logger.info(f'unzip_path: {unzip_path} exist')

        if content_style == 'book' or content_style == 'paper':
            res_path = os.path.join(unzip_path, 'lgb_model_1028.pkl')
        else:
            res_path = os.path.join(unzip_path, 'lgb_model_0925.pkl')

        return res_path

    def _load_model(self, model_path):
        ctypes.cdll.LoadLibrary('libgomp.so.1')
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model

    def predict_with_features(self, features_dict: Dict[str, Any]) -> float:
        feature_df = pd.json_normalize(features_dict)
        pred = self.quality_model.predict(feature_df, num_threads=1)[0]

        return float(pred)

    def predict_with_content(self, content: str, content_style: str = None) -> float:
        # 停用词相关
        stop_word_dict = stats_stop_words(content)
        stop_word_num = stop_word_dict['stop_word_num']
        stop_word_frac = stop_word_dict['stop_word_frac']

        if stop_word_num < 1:
            return 0.0

        # 信息熵
        entropy = stats_entropy(content)['entropy']

        if entropy <= 1:
            return 0.0

        # 文本长度
        content_len = get_content_len(content)

        # 分词
        word_list = content2words(content)
        words_num = len(word_list)

        if word_list:
            longest_word_length = max([len(w) for w in word_list])
        else:
            longest_word_length = 0

        if longest_word_length > 56:
            return 0.0

        # 内容文本长度和占比
        content_word_list = [x for x in word_list if x.isalpha()]
        content_word_len = sum([len(x) for x in content_word_list])
        content_word_frac = div_zero(content_word_len, content_len)

        if content_word_len <= 30:
            return 0.0

        # 标点结尾句子
        punc_sentence_dict = stats_punctuation_end_sentence(content)
        punc_end_sentence_num = punc_sentence_dict['punc_end_sentence_num']
        punc_end_sentence_mean_len = punc_sentence_dict['punc_end_sentence_mean_len']
        longest_punc_sentence_len = punc_sentence_dict['longest_punc_sentence_len']

        if punc_end_sentence_mean_len <= 2:
            return 0.0

        if longest_punc_sentence_len > 480:
            return 0.0

        # 最大连续空格
        max_continue_space_num = stats_continue_space(content)['max_continue_space_num']

        if max_continue_space_num > 500:
            return 0.0

        # 分行
        content_lines = content2lines(content)
        lines_num = len(content_lines)

        # 分词压缩率
        content_len_without_space = get_content_len_without_space(content)
        word_compression = div_zero(content_len_without_space, words_num)

        # 特殊字符
        special_char_pattern = re.compile(r'[�□]')
        special_char_list = special_char_pattern.findall(content)
        special_char_len = sum([len(x) for x in special_char_list])
        special_char_frac = div_zero(special_char_len, content_len_without_space)

        if special_char_frac > 0.01:
            return 0.0

        # 数字长度和占比
        numbers = re.findall(r'\d+', content)
        num_len = sum([len(x) for x in numbers])
        num_frac = div_zero(num_len, content_len)

        # 空格长度和占比
        space_list = re.findall(r'\s+', content)
        space_len = sum([len(x) for x in space_list])
        space_frac = div_zero(space_len, content_len)

        # 标点长度和占比
        punc_list = bfuncs.character.get_common_punc_list()
        punc_pattern_str = re.escape(''.join(punc_list))
        punc_pattern = re.compile('[' + punc_pattern_str + ']')
        puncs = punc_pattern.findall(content)
        punc_len = sum([len(x) for x in puncs])
        punc_frac = div_zero(punc_len, content_len)

        # emoji的长度和占比
        emoji_pattern = bfuncs.char_norm.emoji_pattern
        emojis = emoji_pattern.findall(content)
        emoji_len = sum([len(x) for x in emojis])
        emoji_frac = div_zero(emoji_len, content_len)

        ellipsis_line_num = 0
        ellipsis_list = ['…', '...', '。。。']
        for line in content_lines:
            if any([line.endswith(ell) for ell in ellipsis_list]):
                ellipsis_line_num += 1
        ellipsis_line_frac = div_zero(ellipsis_line_num, lines_num)

        enter_num = len(re.findall(r'\n', content))
        enter_frac = div_zero(enter_num, content_len_without_space)

        # html 符号
        html_entity_dict = stats_html_entity(content)
        html_semi_entity_count = html_entity_dict['html_semi_entity_count']
        html_semi_entity_frac = html_entity_dict['html_semi_entity_frac']

        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        url_list = url_pattern.findall(content)
        url_len = sum([len(x) for x in url_list])
        url_char_frac = div_zero(url_len, content_len_without_space)

        # 退化度
        unique_words_frac = div_zero(len(set(word_list)), len(word_list))

        # search_text = 'javascript'
        # js_counts = sum([line.lower().count(search_text) > 0 for line in content_lines])
        # js_line_frac = div_zero(js_counts, lines_num)

        average_words_per_line = div_zero(words_num, lines_num)

        bulletpoint_lines = 0
        for line in content_lines:
            if line.lstrip().startswith(BULLET_POINT_SYMBOLS):
                bulletpoint_lines += 1
        bulletpoint_line_frac = div_zero(bulletpoint_lines, lines_num)

        gram_dict = stats_ngram_mini(content)
        dup_top_2gram = gram_dict['dup_top_2gram']
        # dup_top_3gram = gram_dict["dup_top_3gram"]
        dup_top_4gram = gram_dict['dup_top_4gram']
        # dup_5gram = gram_dict["dup_5gram"]
        # dup_6gram = gram_dict["dup_6gram"]
        # dup_7gram = gram_dict["dup_7gram"]
        # dup_8gram = gram_dict["dup_8gram"]
        # dup_9gram = gram_dict["dup_9gram"]
        dup_10gram = gram_dict['dup_10gram']

        unicode_dict = stats_unicode(content)
        std_dev_unicode_value = unicode_dict['std_dev_unicode_value']
        mean_diff_unicode_value = unicode_dict['mean_diff_unicode_value']

        features_dict = {}
        if content_style == 'book' or content_style == 'paper':
            # 公式相关特征
            inline_formulas, block_formulas = extract_formulas(content)

            formula_count_dict = formula_count_features(inline_formulas, block_formulas)
            inline_formula_count = formula_count_dict['inline_formula_count']
            block_formula_count = formula_count_dict['block_formula_count']
            total_formula_count = formula_count_dict['total_formula_count']

            formula_density = (
                total_formula_count / content_len if content_len > 0 else 0
            )

            formula_complexity_dict = formula_complexity_features(
                inline_formulas, block_formulas
            )
            average_formula_length = formula_complexity_dict['average_formula_length']
            average_operator_count = formula_complexity_dict['average_operator_count']

            formula_distribution_variance = formula_distribution_var(content_lines)

            formula_type_ratio_dict = formula_type_ratios(
                inline_formulas, block_formulas
            )
            integral_formula_ratio = formula_type_ratio_dict['integral_formula_ratio']
            derivative_formula_ratio = formula_type_ratio_dict[
                'derivative_formula_ratio'
            ]
            matrix_formula_ratio = formula_type_ratio_dict['matrix_formula_ratio']

            features_dict.update(
                {
                    'inline_formula_count': inline_formula_count,
                    'block_formula_count': block_formula_count,
                    'total_formula_count': total_formula_count,
                    'formula_density': formula_density,
                    'average_formula_length': average_formula_length,
                    'average_operator_count': average_operator_count,
                    'formula_distribution_variance': formula_distribution_variance,
                    'integral_formula_ratio': integral_formula_ratio,
                    'derivative_formula_ratio': derivative_formula_ratio,
                    'matrix_formula_ratio': matrix_formula_ratio,
                }
            )

        features_dict.update(
            {
                # "content_len": content_len,
                'lines_num': lines_num,
                'words_num': words_num,
                'word_compression': word_compression,
                'content_word_len': content_word_len,
                'content_word_frac': content_word_frac,
                'num_len': num_len,
                'num_frac': num_frac,
                'space_len': space_len,
                'space_frac': space_frac,
                'punc_len': punc_len,
                'punc_frac': punc_frac,
                'emoji_len': emoji_len,
                'emoji_frac': emoji_frac,
                'punc_end_sentence_num': punc_end_sentence_num,
                'punc_end_sentence_mean_len': punc_end_sentence_mean_len,
                'stop_word_num': stop_word_num,
                'stop_word_frac': stop_word_frac,
                # "ellipsis_line_num": ellipsis_line_num,
                'ellipsis_line_frac': ellipsis_line_frac,
                'enter_frac': enter_frac,
                'max_continue_space_num': max_continue_space_num,
                'html_semi_entity_count': html_semi_entity_count,
                'html_semi_entity_frac': html_semi_entity_frac,
                'url_char_frac': url_char_frac,
                'special_char_len': special_char_len,
                'special_char_frac': special_char_frac,
                'unique_words_frac': unique_words_frac,
                'entropy': entropy,
                # "js_line_frac": js_line_frac,
                'average_words_per_line': average_words_per_line,
                'bulletpoint_line_frac': bulletpoint_line_frac,
                'dup_top_2gram': dup_top_2gram,
                # "dup_top_3gram": dup_top_3gram,
                'dup_top_4gram': dup_top_4gram,
                # "dup_5gram": dup_5gram,
                # "dup_6gram": dup_6gram,
                # "dup_7gram": dup_7gram,
                # "dup_8gram": dup_8gram,
                # "dup_9gram": dup_9gram,
                'dup_10gram': dup_10gram,
                'std_dev_unicode_value': std_dev_unicode_value,
                'mean_diff_unicode_value': mean_diff_unicode_value,
            }
        )

        prob = self.predict_with_features(features_dict)
        return prob


def get_quality_model(language, content_style) -> Tuple[QualityModel, float]:
    model_name = _model_resource_map.get(f'{language}-{content_style}', None)
    if model_name is None:
        return None, None
    if model_name not in _global_quality_model:
        _global_quality_model[model_name] = QualityModel(language, content_style)
    threshold = threshold_map[model_name]

    return _global_quality_model[model_name], threshold


def quality_prober(data_dict: Dict[str, Any], language: str, content_style: str):
    model, _ = get_quality_model(language, content_style)
    if model is None:
        raise ModelInputException(
            f"Unsupport language '{language}' or content_style '{content_style}'"
        )
    content = DataJson(data_dict).get_content_list().to_txt()
    return {'quality_prob': model.predict_with_content(content, content_style)}


class QualityFilter:
    def __init__(self):
        pass

    def check_supported(self, language: str, content_style: str):
        return f'{language}-{content_style}' in _model_resource_map

    def filter(
        self, content_str: str, language: str, language_details: str, content_style: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """Predict the quality score of the content and filter out score below
        the threshold First, check if the language and content_style are
        supported Then get the quality model and threshold, and predict the
        quality score of the content Finally, return the result of whether the
        content should be filtered out.

        Args:
            content_str (str): the content string
            language (str): the language of the content
            language_details (str): the details of the language
            content_style (str): the content style of the content

        Raises:
            CleanModelUnsupportedLanguageException: raise  if the language and content_style are not supported

        Returns:
            bool: True if the content should remain, False if the content should be filtered out
        """
        if not self.check_supported(language, content_style):
            raise CleanModelUnsupportedLanguageException(
                f"Unsupport language '{language}' with content_style '{content_style}'"
            )
        else:
            model, threshold = get_quality_model(language, content_style)
            prob = model.predict_with_content(content_str, content_style)
            return prob > threshold, {'quality_prob': prob}
