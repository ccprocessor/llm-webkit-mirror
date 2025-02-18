RES_MAP = {}


def build_stop_word_set(include_zh: bool = True, include_en: bool = True) -> set:
    stop_word_list = []
    if include_zh:
        with open("../assets/stop_word.txt", "r") as f:
            for line in f:
                stop_word_list.append(line.strip())
    if include_en:
        from nltk.corpus import stopwords

        stop_word_list += stopwords.words("english")
    stop_word_set = set(stop_word_list)
    return stop_word_set


def get_stop_word_en_zh_set():
    if "STOP_WORD_EN_ZH_SET" not in RES_MAP:
        RES_MAP["STOP_WORD_EN_ZH_SET"] = build_stop_word_set(
            include_zh=True, include_en=True
        )
    return RES_MAP["STOP_WORD_EN_ZH_SET"]


def filter_stop_word(token_str_list: list, stop_word_set: set = None):
    if stop_word_set is None:
        stop_word_set = get_stop_word_en_zh_set()
    return [word for word in token_str_list if word not in stop_word_set]
