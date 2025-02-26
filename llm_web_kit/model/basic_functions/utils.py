import functools
from typing import List

import jieba_fast


def div_zero(a, b):
    """
    避免除零错误
    Args:
        a: float 分子
        b: float 分母
    Returns:
        result: float 除法结果
    """
    if b == 0 and a == 0:
        result = float('nan')
    elif b == 0:
        result = float('inf')
    else:
        result = a / b
    return result


def dict_wrapper(key_list):
    """装饰器，将函数返回值转换为字典."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            as_dict = kwargs.get('as_dict', True)
            kwargs.pop('as_dict', None)
            results = func(*args, **kwargs)
            if as_dict:
                if not isinstance(results, tuple):
                    results = (results,)
                return {key: value for key, value in zip(key_list, results)}
            else:
                return results

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator


@functools.lru_cache(maxsize=128)
def jieba_lcut(*args, **kwargs):
    """
    input: text: str 输入文本
    output: words: list 分词后的词语列表
    description: 使用jieba分词对文本进行分词
    """
    words = jieba_fast.lcut(*args, **kwargs)
    return words


# 转换成词列表
# alpha表示去除数字、标点空格等
def content2words(content: str, alpha: bool = False) -> List[str]:
    seg_list = jieba_lcut(content)
    word_list = [w for w in seg_list if w.strip()]
    if alpha:
        return [w for w in word_list if w.isalpha()]
    else:
        return word_list
