import inspect
from pathlib import Path

import commentjson as json

from llm_web_kit.input.datajson import DataJsonKey


class ErrorMsg:
    """Error message manager class."""
    _errors = {}

    @classmethod
    def _load_errors(cls):
        """Load error codes and messages from JSON file."""
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
            return f'unknown error code {error_code}'
        return cls._errors[str(error_code)]['message']

    @classmethod
    def get_error_code(cls, module: str, error_name: str) -> int:
        """根据模块名和错误名获取错误代码."""
        for code, info in cls._errors.items():
            if info['module'] == module and info['error_name'] == error_name:
                return int(code)
        raise ValueError(f'error code not found: module={module}, error_name={error_name}')


ErrorMsg._load_errors()


class LlmWebKitBaseException(Exception):
    """Base exception class for LlmWebKit."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('LlmWebKitBase', 'LlmWebKitBaseException')

        self.error_code = error_code
        self.message = ErrorMsg.get_error_message(self.error_code)
        self.custom_message = custom_message
        self.dataset_name = DataJsonKey.DATASET_NAME
        super().__init__(self.message)
        frame = inspect.currentframe().f_back
        self.__py_filename = frame.f_code.co_filename
        self.__py_file_line_number = frame.f_lineno

    def __str__(self):
        return (
            f'{self.__py_filename}: {self.__py_file_line_number}#{self.error_code}#{self.message}#{self.custom_message}'
        )


##############################################################################
#
#  ExtractorChain Exceptions
#
##############################################################################

class ExtractorChainBaseException(LlmWebKitBaseException):
    """Base exception class for ExtractorChain."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('ExtractorChain', 'ExtractorChainBaseException')
        super().__init__(custom_message, error_code)


class ExtractorInitException(ExtractorChainBaseException):
    """Exception raised during Extractor initialization."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('ExtractorChain', 'ExtractorChainInitException')
        super().__init__(custom_message, error_code)


class ExtractorChainInputException(ExtractorChainBaseException):
    """Exception raised for invalid input data format."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('ExtractorChain', 'ExtractorChainInputException')
        super().__init__(custom_message, error_code)


class ExtractorChainConfigException(ExtractorChainBaseException):
    """Exception raised for configuration related issues."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('ExtractorChain', 'ExtractorChainConfigException')
        super().__init__(custom_message, error_code)


class ExtractorNotFoundException(ExtractorChainBaseException):
    """Exception raised when specified Extractor is not found."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('ExtractorChain', 'ExtractorNotFoundException')
        super().__init__(custom_message, error_code)


##############################################################################
#
#  Extractor Base Exception
#
##############################################################################

class ExtractorBaseException(LlmWebKitBaseException):
    """Base exception class for all Extractor related exceptions."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Extractor', 'ExtractorBaseException')
        super().__init__(custom_message, error_code)


##############################################################################
#
#  File Extractor Exceptions
#
##############################################################################

class HtmlFileExtractorException(ExtractorBaseException):
    """Base exception class for HTML file processing."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Extractor', 'HtmlFileExtractorException')
        super().__init__(custom_message, error_code)


class PdfFileExtractorException(ExtractorBaseException):
    """Exception raised during PDF file processing."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Extractor', 'PdfFileExtractorException')
        super().__init__(custom_message, error_code)


class EbookFileExtractorException(ExtractorBaseException):
    """Exception raised during Ebook file processing."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Extractor', 'EbookFileExtractorException')
        super().__init__(custom_message, error_code)


class OtherFileExtractorException(ExtractorBaseException):
    """Exception raised during processing of other file types."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Extractor', 'OtherFileExtractorException')
        super().__init__(custom_message, error_code)


##############################################################################
#
#  HTML Processing Exceptions
#
##############################################################################

class MagicHtmlExtractorException(HtmlFileExtractorException):
    """Exception raised during magic-html processing."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Extractor', 'MagicHtmlExtractorException')
        super().__init__(custom_message, error_code)


class HtmlPreExtractorException(HtmlFileExtractorException):
    """Exception raised during HTML pre-extraction phase."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Extractor', 'HtmlPreExtractorException')
        super().__init__(custom_message, error_code)


class HtmlExtractorException(HtmlFileExtractorException):
    """Base exception class for HTML extraction."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Extractor', 'HtmlExtractorException')
        super().__init__(custom_message, error_code)


class HtmlPostExtractorException(HtmlFileExtractorException):
    """Exception raised during HTML post-extraction phase."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Extractor', 'HtmlPostExtractorException')
        super().__init__(custom_message, error_code)


##############################################################################
#
#  HTML Recognizer Exceptions
#
##############################################################################

class HtmlRecognizerException(HtmlExtractorException):
    """Base exception class for HTML recognizer."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('HtmlRecognizer', 'HtmlRecognizerException')
        super().__init__(custom_message, error_code)


class HtmlMathRecognizerException(HtmlRecognizerException):
    """Exception raised during math content recognition."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('HtmlRecognizer', 'HtmlMathRecognizerException')
        super().__init__(custom_message, error_code)


class HtmlCodeRecognizerException(HtmlRecognizerException):
    """Exception raised during code content recognition."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('HtmlRecognizer', 'HtmlCodeRecognizerException')
        super().__init__(custom_message, error_code)


class HtmlTableRecognizerException(HtmlRecognizerException):
    """Exception raised during table content recognition."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('HtmlRecognizer', 'HtmlTableRecognizerException')
        super().__init__(custom_message, error_code)


class HtmlImageRecognizerException(HtmlRecognizerException):
    """Exception raised during image content recognition."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('HtmlRecognizer', 'HtmlImageRecognizerException')
        super().__init__(custom_message, error_code)


class HtmlListRecognizerException(HtmlRecognizerException):
    """Exception raised during list content recognition."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('HtmlRecognizer', 'HtmlListRecognizerException')
        super().__init__(custom_message, error_code)


class HtmlAudioRecognizerException(HtmlRecognizerException):
    """Exception raised during audio content recognition."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('HtmlRecognizer', 'HtmlAudioRecognizerException')
        super().__init__(custom_message, error_code)


class HtmlVideoRecognizerException(HtmlRecognizerException):
    """Exception raised during video content recognition."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('HtmlRecognizer', 'HtmlVideoRecognizerException')
        super().__init__(custom_message, error_code)


class HtmlTitleRecognizerException(HtmlRecognizerException):
    """Exception raised during title content recognition."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('HtmlRecognizer', 'HtmlTitleRecognizerException')
        super().__init__(custom_message, error_code)


class HtmlTextRecognizerException(HtmlRecognizerException):
    """Exception raised during text content recognition."""

    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('HtmlRecognizer', 'HtmlTextRecognizerException')
        super().__init__(custom_message, error_code)


##############################################################################
#
#  Clean Module Exceptions
#
##############################################################################

class CleanExp(LlmWebKitBaseException):
    """清洗模块异常基类."""

    def __init__(self, custom_message: str = None, err_code: int = 7000):
        """清洗模块初始化异常.

        Args:
            custom_message (str, optional): _description_. Defaults to None.
        """
        super().__init__(custom_message, err_code)


class CleanLangTypeExp(CleanExp):
    """清洗模块语言类型异常."""

    def __init__(self, custom_message: str = None):
        super().__init__(custom_message, 7010)
