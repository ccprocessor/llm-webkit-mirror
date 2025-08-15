import inspect
from pathlib import Path

import commentjson as json


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
        self.dataset_name = ''
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


class HtmlMathMathjaxRenderRecognizerException(HtmlRecognizerException):
    """Exception raised during math render."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('HtmlRecognizer', 'HtmlMathMathjaxRenderRecognizerException')
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


class ModelBaseException(LlmWebKitBaseException):
    """Base exception class for Model module."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Model', 'ModelBaseException')
        super().__init__(custom_message, error_code)


class ModelResourceException(ModelBaseException):
    """Exception raised during model resource loading."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Model', 'ModelResourceException')
        super().__init__(custom_message, error_code)


class ModelInitException(ModelBaseException):
    """Exception raised during model initialization."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Model', 'ModelInitException')
        super().__init__(custom_message, error_code)


class ModelInputException(ModelBaseException):
    """Exception raised for model input data format."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Model', 'ModelInputException')
        super().__init__(custom_message, error_code)


class ModelRuntimeException(ModelBaseException):
    """Exception raised for model input data format."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Model', 'ModelRuntimeException')
        super().__init__(custom_message, error_code)


class ModelOutputException(ModelBaseException):
    """Exception raised for model output data format."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Model', 'ModelOutputException')
        super().__init__(custom_message, error_code)


class SafeModelException(ModelBaseException):
    """Exception raised for safe model related issues."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Model', 'SafeModelException')
        super().__init__(custom_message, error_code)


class CleanModelException(ModelBaseException):
    """Exception raised for clean model related issues."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Model', 'CleanModelException')
        super().__init__(custom_message, error_code)


##############################################################################
#
#  Model Exceptions
#
##############################################################################
class CleanModelUnsupportedLanguageException(CleanModelException):
    """Exception raised for clean model unsupported language."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Model', 'CleanModelUnsupportedLanguageException')
        super().__init__(custom_message, error_code)


##############################################################################
#
#  MainHtmlParser Exceptions
#
##############################################################################
class MainHtmlParserBaseException(LlmWebKitBaseException):
    """Base exception class for MainHtmlParser."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('MainHtmlParser', 'MainHtmlParserBaseException')
        super().__init__(custom_message, error_code)


##############################################################################
#
#  ProcessorChain Exceptions
#
##############################################################################
class ProcessorChainBaseException(LlmWebKitBaseException):
    """Base exception class for ProcessorChain."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('ProcessorChain', 'ProcessorChainBaseException')
        super().__init__(custom_message, error_code)


class ProcessorChainInitException(ProcessorChainBaseException):
    """Exception raised during ProcessorChain initialization."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('ProcessorChain', 'ProcessorChainInitException')
        super().__init__(custom_message, error_code)


class ProcessorChainConfigException(ProcessorChainBaseException):
    """Exception raised for ProcessorChain configuration related issues."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('ProcessorChain', 'ProcessorChainConfigException')
        super().__init__(custom_message, error_code)


class ProcessorChainInputException(ProcessorChainBaseException):
    """Exception raised for invalid ProcessorChain input data format."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('ProcessorChain', 'ProcessorChainInputException')
        super().__init__(custom_message, error_code)


class ProcessorNotFoundException(ProcessorChainBaseException):
    """Exception raised when specified Processor is not found."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('ProcessorChain', 'ProcessorNotFoundException')
        super().__init__(custom_message, error_code)


##############################################################################
#
#  Processor Exceptions
#
##############################################################################
class ProcessorBaseException(LlmWebKitBaseException):
    """Base exception class for all Processor related exceptions."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Processor', 'ProcessorBaseException')
        super().__init__(custom_message, error_code)


class HtmlPreProcessorException(ProcessorBaseException):
    """Exception raised during HTML pre-processing phase."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Processor', 'HtmlPreProcessorException')
        super().__init__(custom_message, error_code)


class HtmlProcessorException(ProcessorBaseException):
    """Base exception class for HTML processing."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Processor', 'HtmlProcessorException')
        super().__init__(custom_message, error_code)


class HtmlPostProcessorException(ProcessorBaseException):
    """Exception raised during HTML post-processing phase."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Processor', 'HtmlPostProcessorException')
        super().__init__(custom_message, error_code)


##############################################################################
#
#  Parser Exceptions
#
##############################################################################
class DomainClusteringParserException(HtmlProcessorException):
    """Exception raised during domain clustering processing."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Parser', 'DomainClusteringParserException')
        super().__init__(custom_message, error_code)


class LayoutClusteringParserException(HtmlProcessorException):
    """Exception raised during layout clustering processing."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Parser', 'LayoutClusteringParserException')
        super().__init__(custom_message, error_code)


class TypicalHtmlSelectorParserException(HtmlProcessorException):
    """Exception raised during typical HTML selector processing."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Parser', 'TypicalHtmlSelectorParserException')
        super().__init__(custom_message, error_code)


class TagSimplifiedParserException(HtmlProcessorException):
    """Exception raised during tag simplified processing."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Parser', 'TagSimplifiedParserException')
        super().__init__(custom_message, error_code)


class LimMainIdentifierParserException(HtmlProcessorException):
    """Exception raised during LIM main identifier processing."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Parser', 'LimMainIdentifierParserException')
        super().__init__(custom_message, error_code)


class TagMappingParserException(HtmlProcessorException):
    """Exception raised during tag mapping processing."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Parser', 'TagMappingParserException')
        super().__init__(custom_message, error_code)


class LayoutSubtreeParserException(HtmlProcessorException):
    """Exception raised during layout subtree parser processing."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Parser', 'LayoutSubtreeParserException')
        super().__init__(custom_message, error_code)


class LayoutBatchParserException(HtmlProcessorException):
    """Exception raised during layout batch processing."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Parser', 'LayoutBatchParserException')
        super().__init__(custom_message, error_code)


class DomContentFilterParserException(HtmlProcessorException):
    """Exception raised during DOM content filter processing."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('Parser', 'DomContentFilterParserException')
        super().__init__(custom_message, error_code)


##############################################################################
#
#  SimpleAPI Exceptions
#
##############################################################################
class SimpleAPIBaseException(LlmWebKitBaseException):
    """Base exception class for Simple API."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('SimpleAPI', 'SimpleAPIBaseException')
        super().__init__(custom_message, error_code)


class InvalidExtractorTypeException(SimpleAPIBaseException):
    """Exception raised for invalid extractor type."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('SimpleAPI', 'InvalidExtractorTypeException')
        super().__init__(custom_message, error_code)


class InvalidOutputFormatException(SimpleAPIBaseException):
    """Exception raised for invalid output format."""
    def __init__(self, custom_message: str | None = None, error_code: int | None = None):
        if error_code is None:
            error_code = ErrorMsg.get_error_code('SimpleAPI', 'InvalidOutputFormatException')
        super().__init__(custom_message, error_code)
