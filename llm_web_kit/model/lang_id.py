import os
import re
from typing import Dict, Tuple

import fasttext

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.resource_utils.download_assets import (
    CACHE_DIR, download_auto_file)
from llm_web_kit.model.resource_utils.singleton_resource_manager import \
    singleton_resource_manager

language_dict = {
    'srp': 'sr', 'swe': 'sv', 'dan': 'da', 'ita': 'it', 'spa': 'es', 'pes': 'fa', 'slk': 'sk', 'hun': 'hu', 'bul': 'bg', 'cat': 'ca',
    'tur': 'tr', 'ell': 'el', 'eng': 'en', 'nob': 'no', 'fra': 'fr', 'rus': 'ru', 'hrv': 'hr', 'nld': 'nl', 'ind': 'id', 'hye': 'hy',
    'heb': 'he', 'ceb': 'ceb', 'ron': 'ro', 'pol': 'pl', 'kor': 'ko', 'vie': 'vi', 'deu': 'de', 'slv': 'sl', 'por': 'pt', 'ces': 'cs',
    'ukr': 'uk', 'fin': 'fi', 'arb': 'ar', 'tgl': 'tl', 'afr': 'af', 'est': 'et', 'war': 'war', 'zul': 'zu', 'lit': 'lt', 'ilo': 'ilo',
    'kat': 'ka', 'hin': 'hi', 'mkd': 'mk', 'swh': 'sw', 'epo': 'eo', 'sot': 'st', 'tsn': 'tn', 'xho': 'xh', 'lvs': 'lv', 'als': 'als',
    'tso': 'ts', 'kaz': 'kk', 'sna': 'sn', 'amh': 'am', 'zsm': 'ms', 'tha': 'th', 'tah': 'ty', 'nso': 'nso', 'ewe': 'ee', 'urd': 'ur',
    'isl': 'is', 'lin': 'ln', 'bis': 'bi', 'twi': 'tw', 'sin': 'si', 'ben': 'bn', 'mya': 'my', 'plt': 'mg', 'pan': 'pa', 'azj': 'az',
    'guj': 'gu', 'glg': 'gl', 'kir': 'ky', 'tel': 'te', 'tpi': 'tpi', 'ibo': 'ig', 'tam': 'ta', 'tat': 'tt', 'bem': 'bem', 'bel': 'be',
    'kin': 'rw', 'npi': 'ne', 'pap': 'pap', 'mar': 'mr', 'smo': 'sm', 'run': 'rn', 'che': 'ce', 'fij': 'fj', 'tir': 'ti', 'ast': 'ast',
    'kan': 'kn', 'mlt': 'mt', 'yor': 'yo', 'eus': 'eu', 'lua': 'lua', 'pag': 'pag', 'sag': 'sg', 'oss': 'os', 'khk': 'mn', 'tum': 'tum',
    'tgk': 'tg', 'lug': 'lg', 'mal': 'ml', 'umb': 'umb', 'hat': 'ht', 'kon': 'kg', 'azb': 'azb', 'hau': 'ha', 'mos': 'mos', 'kal': 'kl',
    'nno': 'nn', 'lus': 'lus', 'oci': 'oc', 'bos': 'bs', 'gaz': 'gaz', 'bak': 'ba', 'chv': 'cv', 'cym': 'cy', 'tuk': 'tk', 'luo': 'luo',
    'ayr': 'ay', 'ssw': 'ss', 'quy': 'qu', 'uzn': 'uz', 'kik': 'ki', 'kmb': 'kmb', 'jav': 'jv', 'ltz': 'lb', 'asm': 'as', 'ton': 'to',
    'nya': 'ny', 'kam': 'kam', 'ckb': 'ckb', 'min': 'min', 'bod': 'bo', 'lmo': 'lmo', 'gle': 'ga', 'sun': 'su', 'xmf': 'xmf', 'cjk': 'cjk',
    'nia': 'nia', 'kbp': 'kbp', 'ory': 'or', 'fon': 'fon', 'kmr': 'ku', 'khm': 'km', 'ydd': 'yi', 'abk': 'ab', 'san': 'sa', 'uig': 'ug',
    'lim': 'li', 'scn': 'scn', 'mai': 'mai', 'snd': 'sd', 'wes': 'wes', 'pcm': 'pcm', 'arn': 'arn', 'vec': 'vec', 'nav': 'nv', 'gom': 'gom',
    'gla': 'gd', 'yue': 'zh', 'dyu': 'dyu', 'kac': 'kac', 'roh': 'rm', 'udm': 'udm', 'lao': 'lo', 'diq': 'diq', 'som': 'so', 'kab': 'kab',
    'bjn': 'bjn', 'bxr': 'bxr', 'knc': 'knc', 'szl': 'szl', 'kea': 'kea', 'ban': 'ban', 'crh': 'crh', 'bug': 'bug', 'fur': 'fur', 'ace': 'ace',
    'fuv': 'fuv', 'prs': 'prs', 'mri': 'mi', 'dik': 'dik', 'taq': 'taq', 'kas': 'kas', 'pbt': 'pbt', 'tzm': 'tzm', 'bam': 'bm', 'mag': 'mag',
    'hne': 'hne', 'nus': 'nus', 'krc': 'krc', 'bho': 'bho', 'mni': 'mni', 'ltg': 'ltg', 'alt': 'alt', 'dzo': 'dz', 'lij': 'lij', 'wol': 'wo',
    'sat': 'sat', 'jpn': 'ja', 'shn': 'shn', 'grn': 'gn', 'fao': 'fo', 'zho': 'zh', 'awa': 'awa', 'aka': 'ak', 'ewo': 'ewo', 'srd': 'sc',
    'ady': 'ady'
}


class LanguageIdentification:
    """Language Identification model using fasttext."""

    def __init__(self, model_path: str = None):
        """Initialize LanguageIdentification model Will download the 218.bin
        model if model_path is not provided.

        Args:
            model_path (str, optional): Path to the model. Defaults to None.
        """

        if model_path is None:
            model_path = self.auto_download()
        self.model = fasttext.load_model(model_path)

    def auto_download(self):
        """Default download the 218.bin model."""
        resource_name = 'lang-id-218'
        resource_config = load_config()['resources']
        lang_id_218_config: dict = resource_config[resource_name]
        lang_id_218_url = lang_id_218_config['download_path']
        lang_id_218_sha256 = lang_id_218_config.get('sha256', '')
        target_path = os.path.join(CACHE_DIR, resource_name, 'model.bin')
        logger.info(f'try to make target_path: {target_path} exist')
        target_path = download_auto_file(lang_id_218_url, target_path, sha256_sum=lang_id_218_sha256)
        logger.info(f'target_path: {target_path} exist')
        return target_path

    @property
    def version(self) -> str:
        """
        Get the version of the model
        The version is determined by the number of labels in the model
        now have 176 version from : https://fasttext.cc/docs/en/language-identification.html
        and 218 version from : https://huggingface.co/facebook/fasttext-language-identification/tree/main

        Returns:
            str: The version of the model
        """
        if not hasattr(self, '_version'):
            labels_num = len(self.model.get_labels())
            if labels_num == 176:
                self._version = '176.bin'
            elif labels_num == 218:
                self._version = '218.bin'
            else:
                raise ValueError(f'Unsupported version: {labels_num} labels')
        return self._version

    def predict(self, text: str, k: int = 5) -> Tuple[Tuple[str], Tuple[float]]:
        """Predict language of the given text Return first k predictions, if k
        is greater than number of predictions, return all predictions default k
        is 5.

        Args:
            text (str): Text to predict language
            k (int, optional): Number of predictions to return. Defaults to 5.

        Returns:
            Tuple[Tuple[str], Tuple[float]]: Tuple of predictions and probabilities only return top 5 predictions
        """
        assert k > 0, 'k should be greater than 0'

        # remove new lines
        text = text.replace('\n', ' ')

        # returns top k predictions
        predictions, probabilities = self.model.predict(text, k=k)

        return predictions, probabilities


def get_singleton_lang_detect(model_path: str = None) -> LanguageIdentification:
    """Get the singleton language identification model.

    Args:
        model_path (str, optional): Path to the model. Defaults to None.

    Returns:
        LanguageIdentification: The language identification model
    """
    singleton_name = f'lang_detect_{model_path}' if model_path else 'lang_detect_default'

    if not singleton_resource_manager.has_name(singleton_name):
        singleton_resource_manager.set_resource(singleton_name, LanguageIdentification(model_path))
    return singleton_resource_manager.get_resource(singleton_name)


def decide_language_by_prob_v176(predictions: Tuple[str], probabilities: Tuple[float]) -> str:
    """Decide language based on probabilities The rules are tuned by Some
    sepciific data sources.Now the function supports the lid218 model and
    outputs the language code of lid176.

    Args:
        predictions (Tuple[str]): the predicted languages labels by 176.bin model (__label__zh, __label__en, etc)
        probabilities (Tuple[float]): the probabilities of the predicted languages

    Returns:
        str: the final language label
    """
    lang_prob_dict = {}
    # Regular expression to match both formats
    pattern_176 = re.compile(r'^__label__([a-z]+)$')  # Matches __label__en
    pattern_218 = re.compile(r'^__label__([a-z]+)_[A-Za-z]+$')  # Matches __label__eng__Latn
    for lang_key, lang_prob in zip(predictions, probabilities):
        if pattern_176.match(lang_key):
            lang = lang_key.replace('__label__', '')
        elif pattern_218.match(lang_key):
            label_without_prefix = lang_key.replace('__label__', '')
            lang_code = label_without_prefix.split('_')[0]
            lang = language_dict.get(lang_code, lang_code)
        else:
            raise ValueError(f'Unsupported prediction format: {lang_key}')
        if lang in lang_prob_dict:
            lang_prob_dict[lang] += lang_prob
        else:
            lang_prob_dict[lang] = lang_prob
    zh_prob = lang_prob_dict.get('zh', 0)
    en_prob = lang_prob_dict.get('en', 0)
    zh_en_prob = zh_prob + en_prob
    final_lang = None
    if zh_en_prob > 0.5:
        if zh_prob > 0.4 * zh_en_prob:
            final_lang = 'zh'
        else:
            final_lang = 'en'
    else:
        if max(lang_prob_dict.values()) > 0.6:
            final_lang = max(lang_prob_dict, key=lang_prob_dict.get)
            if final_lang == 'hr':
                final_lang = 'sr'
        elif max(lang_prob_dict.values()) > 0 and max(lang_prob_dict, key=lang_prob_dict.get) in ['sr', 'hr']:
            final_lang = 'sr'
        else:
            final_lang = 'mix'
    return final_lang


LANG_ID_SUPPORTED_VERSIONS = ['176.bin', '218.bin']


def detect_code_block(content_str: str) -> bool:
    """Detect if the content string contains code block."""
    code_hint_lines = sum([1 for line in content_str.split('\n') if line.strip().startswith('```')])
    return code_hint_lines > 1


def detect_inline_equation(content_str: str) -> bool:
    """Detect if the content string contains inline equation."""
    inline_eq_pattern = re.compile(r'\$\$.*\$\$|\$.*\$')
    return any([inline_eq_pattern.search(line) for line in content_str.split('\n')])


def detect_latex_env(content_str: str) -> bool:
    """Detect if the content string contains latex environment."""
    latex_env_pattern = re.compile(r'\\begin\{.*?\}.*\\end\{.*\}', re.DOTALL)
    return latex_env_pattern.search(content_str) is not None


def decide_language_func(content_str: str, lang_detect: LanguageIdentification) -> Dict[str, str]:
    """Decide language based on the content string. This function will truncate
    the content string if it is too long. This function will return "empty" if
    the content string is empty.

    Raises:
        ValueError: Unsupported version.
            The prediction str is different for different versions of fasttext model.
            So the version should be specified.
            Now only support version "176.bin" and "218.bin".

    Warning:
        The too long content string may be truncated.
        Some text with massive code block and equations may be misclassified.

    Args:
        content_str (str): The content string to decide language
        lang_detect (LanguageIdentification): The language identification model

    Returns:
        dict: Dictionary containing 'language' and 'language_details' keys
    """

    # truncate the content string if it is too long
    str_len = len(content_str)
    if str_len > 10000:
        logger.warning('Content string is too long, truncate to 10000 characters')
        start_idx = (str_len - 10000) // 2
        content_str = content_str[start_idx:start_idx + 10000]

    # check if the content string contains code block, inline equation, latex environment
    if detect_code_block(content_str):
        logger.warning('Content string contains code block, may be misclassified')
    if detect_inline_equation(content_str):
        logger.warning('Content string contains inline equation, may be misclassified')
    if detect_latex_env(content_str):
        logger.warning('Content string contains latex environment, may be misclassified')

    # return "empty" if the content string is empty
    if len(content_str.strip()) == 0:
        return {'language': 'empty', 'language_details': None}

    if lang_detect.version not in LANG_ID_SUPPORTED_VERSIONS:
        raise ValueError(f'Unsupported version: {lang_detect.version}. Supported versions: {LANG_ID_SUPPORTED_VERSIONS}')

    predictions, probabilities = lang_detect.predict(content_str)
    language = decide_language_by_prob_v176(predictions, probabilities)

    language_details = None
    if lang_detect.version == '218.bin':
        first_pred = predictions[0]
        match = re.match(r'^__label__([a-z]+)_[A-Za-z]+$', first_pred)
        if match:
            lang_code = match.group(1)
        else:
            lang_code = first_pred.replace('__label__', '').split('_')[0]
        language_details = lang_code

    return {
        'language': language,
        'language_details': language_details
    }


def update_language_by_str(content_str: str, model_path: str = None) -> Dict[str, str]:
    """Decide language based on the content string and return a dictionary with
    language and details."""
    lang_detect = get_singleton_lang_detect(model_path)
    return decide_language_func(content_str, lang_detect)


if __name__ == '__main__':
    li = LanguageIdentification()
    print(li.version)
    text = 'hello world, this is a test. the language is english'
    predictions, probabilities = li.predict(text)

    print(predictions, probabilities)

    print(update_language_by_str(text))

    text = '你好，这是一个测试。这个语言是中文'
    print(update_language_by_str(text))

    text = "```python\nprint('hello world')\n``` 这是一个中文的文档，包含了一些代码"
    print(update_language_by_str(text))

    text = '$$x^2 + y^2 = 1$$ これは数式を含むテストドキュメントです'
    print(update_language_by_str(text))

    text = '\\begin{equation}\n x^2 + y^2 = 1 \n\\end{equation} This is a test document, including some math equations'
    print(update_language_by_str(text))
