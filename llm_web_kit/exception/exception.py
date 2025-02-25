import inspect
from pathlib import Path

import commentjson as json

from llm_web_kit.input.datajson import DataJsonKey


class ErrorMsg:
    # 类属性，用于存储错误代码和消息
    _errors = {}

    @classmethod
    def _load_errors(cls):
        # 从JSON文件中加载错误代码和消息
        exception_defs_file_path = Path(__file__).parent / 'exception.jsonc'
        with open(exception_defs_file_path, 'r', encoding='utf-8') as file:
            jso = json.load(file)
            for module, module_defs in jso.items():
                for err_name, err_info in module_defs.items():
                    err_code = err_info['code']
                    cls._errors[str(err_code)] = {
                        'message': err_info['message'],
                        'module': module,
                        'error_name': err_name,
                    }

    @classmethod
    def get_error_message(cls, error_code: int):
        # 根据错误代码获取错误消息
        if str(error_code) not in cls._errors:
            return f'未知错误代码{error_code}'
        return cls._errors[str(error_code)]['message']


ErrorMsg._load_errors()


class WebKitBaseException(Exception):
    """基础的Pipeline异常类，系统中任何地方抛出的异常都必须是这个异常的子类.

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, err_code: int, custom_message: str):
        self.err_code = err_code
        self.message = ErrorMsg.get_error_message(self.err_code)
        self.custom_message = custom_message
        self.dataset_name = DataJsonKey.DATASET_NAME
        super().__init__(self.message)
        frame = inspect.currentframe().f_back
        self.__py_filename = frame.f_code.co_filename
        self.__py_file_line_number = frame.f_lineno

    def __str__(self):
        return (
            f'{self.__py_filename}: {self.__py_file_line_number}#{self.err_code}#{self.message}#{self.custom_message}'
        )


##############################################################################
#
#  extractor_chain相关的异常
#
###############################################################################


class LlmWebKitBaseException(WebKitBaseException):
    """llm web kit base exp."""

    def __init__(self, error_code, custom_message: str = None):
        """init llm web kit异常."""
        super().__init__(error_code, custom_message)


class LlmWebKitBaseActException(LlmWebKitBaseException):
    """llm web kit base exp."""

    def __init__(self, custom_message: str = None):
        super().__init__(1000, custom_message)


class ExtractorChainBaseException(LlmWebKitBaseException):
    """ExtractorChain基础异常类."""

    def __init__(self, error_code, custom_message: str = None):
        super().__init__(error_code, custom_message)


class ExtractorInitException(ExtractorChainBaseException):
    """Extractor初始化异常."""

    def __init__(self, custom_message: str = None):
        super().__init__(2100, custom_message)


class ExtractorChainInputException(ExtractorChainBaseException):
    """输入数据格式异常."""

    def __init__(self, custom_message: str = None):
        super().__init__(2200, custom_message)


class ExtractorChainConfigException(ExtractorChainBaseException):
    """配置相关异常."""

    def __init__(self, custom_message: str = None):
        super().__init__(2300, custom_message)


class ExtractorNotFoundException(ExtractorChainBaseException):
    """找不到指定的Extractor."""

    def __init__(self, custom_message: str = None):
        super().__init__(2400, custom_message)


##############################################################################
#
#  HTML相关异常
#
###############################################################################


class HtmlBaseExp(ExtractorChainBaseException):
    """HTML基础异常类."""

    def __init__(self, error_code: int, custom_message: str = None):
        super().__init__(error_code, custom_message)


class HTMLExp(HtmlBaseExp):
    """HTML处理异常."""

    def __init__(self, error_code: int, custom_message: str = None):
        super().__init__(5000, custom_message)


# 其他HTML相关异常继承HTMLExp
class HtmlFormatExp(HTMLExp):
    """html format 异常."""

    def __init__(self, custom_message: str = None):
        super().__init__(5001, custom_message)


class HtmlPreExtractorExp(HTMLExp):
    """html pre extractor 异常."""

    def __init__(self, custom_message: str = None):
        super().__init__(5002, custom_message)


class HtmlRecognizerExp(HTMLExp):
    """Html recognizer."""

    def __init__(self, error_code, custom_message: str = None):
        """html recognizer init."""
        super().__init__(4130, custom_message)


class HtmlMagicHtmlExtractorExp(HtmlRecognizerExp):
    """magic-html异常."""

    def __init__(self, custom_message: str = None):
        """magic-html error."""
        super().__init__(4140, custom_message)


class HtmlMathRecognizerExp(HtmlRecognizerExp):
    """math recognizer异常."""

    def __init__(self, custom_message: str = None):
        """math recognizer error."""
        super().__init__(4131, custom_message)


class HtmlCodeRecognizerExp(HtmlRecognizerExp):
    """code recognizer 异常."""

    def __init__(self, custom_message: str = None):
        """code recognizer error."""
        super().__init__(4132, custom_message)


class HtmlTableRecognizerExp(HtmlRecognizerExp):
    """html table recognizer 异常."""

    def __init__(self, custom_message: str = None):
        """html table recognizer init."""
        super().__init__(4133, custom_message)


class HtmlImageRecognizerExp(HtmlRecognizerExp):
    """html image recognizer 异常."""

    def __init__(self, custom_message: str = None):
        """html image recognizer init."""
        super().__init__(4134, custom_message)


class HtmlListRecognizerExp(HtmlRecognizerExp):
    """html list recognizer 异常."""

    def __init__(self, custom_message: str = None):
        """html list recognizer init."""
        super().__init__(4135, custom_message)


class HtmlAudioRecognizerExp(HtmlRecognizerExp):
    """Html audio recognizer异常."""

    def __init__(self, custom_message: str = None):
        """html audio recognizer init."""
        super().__init__(4136, custom_message)


class HtmlVideoRecognizerExp(HtmlRecognizerExp):
    """Html video recognizer 异常."""

    def __init__(self, custom_message: str = None):
        """html video recognizer init."""
        super().__init__(4137, custom_message)


class HtmlTitleRecognizerExp(HtmlRecognizerExp):
    """html title recognizer 异常."""

    def __init__(self, custom_message: str = None):
        """html title recognizer init."""
        super().__init__(4138, custom_message)


class HtmlTextRecognizerExp(HtmlRecognizerExp):
    """html text recognizer 异常."""

    def __init__(self, custom_message: str = None):
        """html text recognizer init."""
        super().__init__(4139, custom_message)


class HtmlPostExtractorExp(HTMLExp):
    """html post extractor 异常."""

    def __init__(self, custom_message: str = None):
        """html post extractor init."""
        super().__init__(4150, custom_message)


class CleanExp(LlmWebKitBaseException):
    """清洗模块异常基类."""

    def __init__(self, err_code: int = 7000, custom_message: str = None):
        """清洗模块初始化异常.

        Args:
            custom_message (str, optional): _description_. Defaults to None.
        """
        super().__init__(err_code, custom_message)


class CleanLangTypeExp(CleanExp):
    """清洗模块语言类型异常."""
    def __init__(self, custom_message: str = None):
        super().__init__(7010, custom_message)
