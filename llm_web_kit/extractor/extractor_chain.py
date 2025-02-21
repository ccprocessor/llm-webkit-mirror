import json
from typing import List, Union

from llm_web_kit.exception.exception import (ExtractorChainConfigException,
                                             ExtractorChainInputException,
                                             ExtractorInitException,
                                             ExtractorNotFoundException)
from llm_web_kit.extractor.extractor import AbstractExtractor
from llm_web_kit.extractor.post_extractor import AbstractPostExtractor
from llm_web_kit.extractor.pre_extractor import AbstractPreExtractor
from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.class_loader import load_python_class_by_name
from llm_web_kit.libs.logger import mylogger


# ##########################################################
# extractor chain
# ##########################################################
class ExtractorChain:
    """Handles extraction by chaining pre_extractors, extractors and
    post_extractors."""

    def __init__(self, config: dict):
        """Initialize extractor chain from config.

        Args:
            config (dict): Config dict containing extractor_pipe configuration
        """
        self.__pre_extractors: List[AbstractPreExtractor] = []
        self.__extractors: List[AbstractExtractor] = []
        self.__post_extractors: List[AbstractPostExtractor] = []

        # Get extractor pipe config
        extractor_config = config.get('extractor_pipe', {})

        # Load extractors
        self.__load_extractors(extractor_config)

    def extract(self, data: DataJson) -> DataJson:
        """Run the extraction extractor."""
        # Validate input
        self.__validate_extract_input(data)

        try:
            # Pre extractors
            for pre_ext in self.__pre_extractors:
                data = pre_ext.pre_extract(data)

            # Main extractors
            for ext in self.__extractors:
                data = ext.extract(data)

            # Post extractors
            for post_ext in self.__post_extractors:
                data = post_ext.post_extract(data)

        except KeyError as e:
            mylogger.error(f'Required field missing in input data: {str(e)}')
            raise ExtractorChainInputException(f'Required field missing in input data: {str(e)}')
        except Exception as e:
            mylogger.error(f'Error during extraction: {str(e)}')
            raise

        return data

    def __load_extractors(self, config: dict):
        """Load extractors from extractor_pipe config."""
        # Load pre extractors
        for pre_config in config.get('pre_extractor', []):
            if pre_config.get('enable'):
                pre_extractor = self.__create_extractor(pre_config)
                self.__pre_extractors.append(pre_extractor)

        # Load main extractors
        for ext_config in config.get('extractor', []):
            if ext_config.get('enable'):
                extractor = self.__create_extractor(ext_config)
                self.__extractors.append(extractor)

        # Load post extractors
        for post_config in config.get('post_extractor', []):
            if post_config.get('enable'):
                post_extractor = self.__create_extractor(post_config)
                self.__post_extractors.append(post_extractor)

    def __create_extractor(self, config: dict) -> Union[AbstractPreExtractor, AbstractExtractor, AbstractPostExtractor]:
        """Create extractor instance from config."""
        python_class = config.get('python_class')
        if not python_class:
            raise ExtractorChainConfigException(
                'python_class not specified in extractor config'
            )

        try:
            kwargs = config.get('class_init_kwargs', {})
            return load_python_class_by_name(python_class, config, kwargs)
        except ImportError:
            raise ExtractorNotFoundException(
                f'Extractor class not found: {python_class}'
            )
        except Exception as e:
            raise ExtractorInitException(
                f'Failed to initialize extractor {python_class}: {str(e)}'
            )

    def __validate_extract_input(self, data_json: DataJson):
        """校验一下配置里必须满足的条件，否则抛出异常.

        Args:
            data_json (DataJson): _description_
        """
        self.__validate_input_data_format(data_json)

    def __validate_input_data_format(self, data_json):
        """校验一下输入的data_json对象是否是DataJson对象，否则抛出异常."""
        if not isinstance(data_json, DataJson):
            raise ExtractorChainInputException(
                f'input data is not DataJson object, data type is {type(data_json)}'
            )


class ExtractSimpleFactory:
    """Factory to create ExtractorChain instances."""

    @staticmethod
    def create(config: Union[str, dict]) -> ExtractorChain:
        """Create ExtractorChain from config.

        Args:
            config: Config dict or path to config file

        Returns:
            ExtractorChain instance
        """
        # Load config if file path provided
        if isinstance(config, str):
            with open(config) as f:
                config = json.load(f)

        # Create and return chain
        return ExtractorChain(config)
