import traceback
from typing import Any, Dict, List, Union

import commentjson as json

from llm_web_kit.exception.exception import (ExtractorChainBaseException,
                                             ExtractorChainConfigException,
                                             ExtractorChainInputException,
                                             ExtractorInitException,
                                             ExtractorNotFoundException,
                                             LlmWebKitBaseException)
from llm_web_kit.input.pre_data_json import PreDataJson
from llm_web_kit.libs.class_loader import load_python_class_by_name
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.main_html_parser.processor import (AbstractMainHtmlProcessor,
                                                    AbstractPostProcessor,
                                                    AbstractPreProcessor)


class MainHtmlProcessorChain:
    """HTML处理器链，串联多个处理器执行HTML处理流程."""

    def __init__(self, config: Dict[str, Any]):
        """初始化处理器链.

        Args:
            config (Dict[str, Any]): 配置字典，包含processor_pipe配置
        """
        self.__pre_processors: List[AbstractPreProcessor] = []
        self.__processors: List[AbstractMainHtmlProcessor] = []
        self.__post_processors: List[AbstractPostProcessor] = []
        self.__config = config

        # 获取处理器管道配置
        processor_config = config.get('processor_pipe', {})

        # 加载处理器
        self.__load_processors(processor_config)

    def process(self, pre_data: PreDataJson) -> PreDataJson:
        """执行整个处理链.

        Args:
            pre_data (PreDataJson): 包含初始数据的PreDataJson对象

        Returns:
            PreDataJson: 处理后的PreDataJson对象
        """
        try:
            # 执行预处理
            if self.__pre_processors:
                logger.info(f'开始执行预处理阶段，共有{len(self.__pre_processors)}个预处理器')
                for i, pre_processor in enumerate(self.__pre_processors):
                    pre_processor_name = pre_processor.get_name()
                    logger.info(f'开始执行第{i+1}个预处理器: {pre_processor_name}')
                    pre_data = pre_processor.pre_process(pre_data)
                    logger.info(f'第{i+1}个预处理器执行完成: {pre_processor_name}')

            # 执行主处理
            if self.__processors:
                logger.info(f'开始执行主处理阶段，共有{len(self.__processors)}个处理器')
                for i, processor in enumerate(self.__processors):
                    processor_name = processor.get_name()
                    logger.info(f'开始执行第{i+1}个处理器: {processor_name}')
                    pre_data = processor.execute(pre_data)
                    logger.info(f'第{i+1}个处理器执行完成: {processor_name}')

            # 执行后处理
            if self.__post_processors:
                logger.info(f'开始执行后处理阶段，共有{len(self.__post_processors)}个后处理器')
                for i, post_processor in enumerate(self.__post_processors):
                    post_processor_name = post_processor.get_name()
                    logger.info(f'开始执行第{i+1}个后处理器: {post_processor_name}')
                    pre_data = post_processor.post_process(pre_data)
                    logger.info(f'第{i+1}个后处理器执行完成: {post_processor_name}')

            logger.info('处理链执行完成')

        except KeyError as e:
            exc = ExtractorChainInputException(f'必要字段缺失: {str(e)}')
            exc.traceback_info = traceback.format_exc()
            raise exc
        except ExtractorChainBaseException as e:
            e.traceback_info = traceback.format_exc()
            raise
        except LlmWebKitBaseException as e:
            e.traceback_info = traceback.format_exc()
            raise
        except Exception as e:
            wrapped = ExtractorChainBaseException(f'处理过程中发生错误: {str(e)}')
            wrapped.traceback_info = traceback.format_exc()
            raise wrapped from e

        return pre_data

    def __load_processors(self, config: Dict[str, Any]):
        """从processor_pipe配置加载处理器.

        Args:
            config (Dict[str, Any]): 处理器配置
        """
        # 加载预处理器
        for pre_processor_config in config.get('pre_processor', []):
            if pre_processor_config.get('enable', False):
                pre_processor = self.__create_pre_processor(pre_processor_config)
                self.__pre_processors.append(pre_processor)

        # 加载主处理器
        for processor_config in config.get('processor', []):
            if processor_config.get('enable', False):
                processor = self.__create_processor(processor_config)
                self.__processors.append(processor)

        # 加载后处理器
        for post_processor_config in config.get('post_processor', []):
            if post_processor_config.get('enable', False):
                post_processor = self.__create_post_processor(post_processor_config)
                self.__post_processors.append(post_processor)

    def __create_processor(self, config: Dict[str, Any]) -> AbstractMainHtmlProcessor:
        """从配置创建处理器实例.

        Args:
            config (Dict[str, Any]): 处理器配置

        Returns:
            AbstractMainHtmlProcessor: 处理器实例
        """
        python_class = config.get('python_class')
        if not python_class:
            raise ExtractorChainConfigException('处理器配置缺少python_class字段')

        try:
            # 加载处理器类
            processor_cls = load_python_class_by_name(python_class)
            if not issubclass(processor_cls, AbstractMainHtmlProcessor):
                raise ExtractorChainConfigException(f'类 {python_class} 不是AbstractMainHtmlProcessor的子类')

            # 创建处理器实例
            kwargs = config.get('class_init_kwargs', {})
            processor = processor_cls(config=config, **kwargs)

            return processor

        except ImportError:
            raise ExtractorNotFoundException(f'处理器类未找到: {python_class}')
        except Exception as e:
            raise ExtractorInitException(f'初始化处理器 {python_class} 失败: {str(e)}')

    def __create_pre_processor(self, config: Dict[str, Any]) -> AbstractPreProcessor:
        """从配置创建预处理器实例.

        Args:
            config (Dict[str, Any]): 预处理器配置

        Returns:
            AbstractPreProcessor: 预处理器实例
        """
        python_class = config.get('python_class')
        if not python_class:
            raise ExtractorChainConfigException('预处理器配置缺少python_class字段')

        try:
            # 加载处理器类
            processor_cls = load_python_class_by_name(python_class)
            if not issubclass(processor_cls, AbstractPreProcessor):
                raise ExtractorChainConfigException(f'类 {python_class} 不是AbstractPreProcessor的子类')

            # 创建处理器实例
            kwargs = config.get('class_init_kwargs', {})
            processor = processor_cls(config=config, **kwargs)

            return processor

        except ImportError:
            raise ExtractorNotFoundException(f'预处理器类未找到: {python_class}')
        except Exception as e:
            raise ExtractorInitException(f'初始化预处理器 {python_class} 失败: {str(e)}')

    def __create_post_processor(self, config: Dict[str, Any]) -> AbstractPostProcessor:
        """从配置创建后处理器实例.

        Args:
            config (Dict[str, Any]): 后处理器配置

        Returns:
            AbstractPostProcessor: 后处理器实例
        """
        python_class = config.get('python_class')
        if not python_class:
            raise ExtractorChainConfigException('后处理器配置缺少python_class字段')

        try:
            # 加载处理器类
            processor_cls = load_python_class_by_name(python_class)
            if not issubclass(processor_cls, AbstractPostProcessor):
                raise ExtractorChainConfigException(f'类 {python_class} 不是AbstractPostProcessor的子类')

            # 创建处理器实例
            kwargs = config.get('class_init_kwargs', {})
            processor = processor_cls(config=config, **kwargs)

            return processor

        except ImportError:
            raise ExtractorNotFoundException(f'后处理器类未找到: {python_class}')
        except Exception as e:
            raise ExtractorInitException(f'初始化后处理器 {python_class} 失败: {str(e)}')

    @classmethod
    def from_config_file(cls, config_file_path: str) -> 'MainHtmlProcessorChain':
        """从配置文件创建处理器链.

        Args:
            config_file_path (str): 配置文件路径，JSON格式

        Returns:
            MainHtmlProcessorChain: 处理器链实例
        """
        try:
            with open(config_file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            return cls(config)
        except Exception as e:
            raise ExtractorChainConfigException(f'加载配置文件 {config_file_path} 失败: {str(e)}')


class HtmlProcessorSimpleFactory:
    """创建MainHtmlProcessorChain实例的工厂类."""

    @staticmethod
    def create(config: Union[str, Dict[str, Any]]) -> MainHtmlProcessorChain:
        """从配置创建MainHtmlProcessorChain.

        Args:
            config: 配置字典或配置文件路径

        Returns:
            MainHtmlProcessorChain实例
        """
        # 如果提供的是文件路径，加载配置
        if isinstance(config, str):
            try:
                with open(config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except Exception as e:
                raise ExtractorChainConfigException(f'加载配置文件失败: {str(e)}')

        # 创建并返回处理器链
        return MainHtmlProcessorChain(config)
