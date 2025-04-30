import traceback
from typing import Any, Dict, List, Union

import commentjson as json

from llm_web_kit.exception.exception import (LlmWebKitBaseException,
                                             ProcessorChainBaseException,
                                             ProcessorChainConfigException,
                                             ProcessorChainInitException,
                                             ProcessorChainInputException,
                                             ProcessorNotFoundException)
from llm_web_kit.input.pre_data_json import PreDataJson
from llm_web_kit.libs.class_loader import load_python_class_by_name
from llm_web_kit.main_html_parser.processor import AbstractProcessor


class ProcessorChain:
    """HTML处理器链，串联多个处理器执行HTML处理流程."""

    def __init__(self, config: Dict[str, Any]):
        """初始化处理器链.

        Args:
            config (Dict[str, Any]): 配置字典，包含processor_pipe配置
        """
        self.__processors: List[AbstractProcessor] = []
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
            # 执行主处理
            for processor in self.__processors:
                pre_data = processor.execute(pre_data)
        except KeyError as e:
            exc = ProcessorChainInputException(f'必要字段缺失: {str(e)}')
            exc.traceback_info = traceback.format_exc()
            raise exc
        except ProcessorChainBaseException as e:
            e.traceback_info = traceback.format_exc()
            raise
        except LlmWebKitBaseException as e:
            e.traceback_info = traceback.format_exc()
            raise
        except Exception as e:
            wrapped = ProcessorChainBaseException(f'处理过程中发生错误: {str(e)}')
            wrapped.traceback_info = traceback.format_exc()
            raise wrapped from e

        return pre_data

    def __load_processors(self, config: Dict[str, Any]):
        """从processor_pipe配置加载处理器.

        Args:
            config (Dict[str, Any]): 处理器配置
        """
        for processor_config in config.get('processor', []):
            if processor_config.get('enable', False):
                processor = self.__create_processor(processor_config)
                self.__processors.append(processor)

    def __create_processor(self, config: Dict[str, Any]) -> AbstractProcessor:
        """从配置创建处理器实例.

        Args:
            config (Dict[str, Any]): 处理器配置

        Returns:
            AbstractMainHtmlProcessor: 处理器实例
        """
        python_class = config.get('python_class')
        if not python_class:
            raise ProcessorChainConfigException('处理器配置缺少python_class字段')

        try:
            # 加载处理器类
            processor_cls = load_python_class_by_name(python_class)
            if not issubclass(processor_cls, AbstractProcessor):
                raise ProcessorChainConfigException(f'类 {python_class} 不是AbstractProcessor的子类')

            # 创建处理器实例
            kwargs = config.get('class_init_kwargs', {})
            processor = processor_cls(config=config, **kwargs)

            return processor

        except ImportError:
            raise ProcessorNotFoundException(f'处理器类未找到: {python_class}')
        except Exception as e:
            raise ProcessorChainInitException(f'初始化处理器 {python_class} 失败: {str(e)}')

    @classmethod
    def from_config_file(cls, config_file_path: str) -> 'ProcessorChain':
        """从配置文件创建处理器链.

        Args:
            config_file_path (str): 配置文件路径，JSON格式

        Returns:
            ProcessorChain: 处理器链实例
        """
        try:
            with open(config_file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            return cls(config)
        except Exception as e:
            raise ProcessorChainConfigException(f'加载配置文件 {config_file_path} 失败: {str(e)}')


class ProcessorSimpleFactory:
    """创建ProcessorChain实例的工厂类."""

    @staticmethod
    def create(config: Union[str, Dict[str, Any]]) -> ProcessorChain:
        """从配置创建ProcessorChain.

        Args:
            config: 配置字典或配置文件路径

        Returns:
            ProcessorChain实例
        """
        # 如果提供的是文件路径，加载配置
        if isinstance(config, str):
            try:
                with open(config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except Exception as e:
                raise ProcessorChainConfigException(f'加载配置文件失败: {str(e)}')

        # 创建并返回处理器链
        return ProcessorChain(config)
