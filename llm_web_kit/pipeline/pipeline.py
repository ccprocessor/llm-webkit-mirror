from abc import ABC, abstractmethod
from typing import List

from overrides import override

from llm_web_kit.input.datajson import DataJson
from llm_web_kit.libs.class_loader import load_python_class_by_name
from llm_web_kit.pipeline.extractor.extractor import AbstractExtractor
from llm_web_kit.pipeline.extractor.post_extractor import AbstractPostExtractor
from llm_web_kit.pipeline.extractor.pre_extractor import AbstractPreExtractor
from llm_web_kit.pipeline.formatter.base import AbstractFormatter


class AbstractPipeline(ABC):
    """抽象的pipeline类，定义了pipeline的接口规范.

    Args:
        ABC (_type_): _description_

    Raises:
        NotImplementedError: _description_
        NotImplementedError: _description_
    """

    @abstractmethod
    def format(self, data_json: DataJson) -> DataJson:
        raise NotImplementedError

    @abstractmethod
    def extract(self, data_json: DataJson) -> DataJson:
        raise NotImplementedError


# ##########################################################
# formatter chain
# ##########################################################
class FormatterChain:
    """_summary_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, config: dict):
        """_summary_

        Args:
            config (Dict): 配置文件里的整个配置字典
        """
        self.__formatter_lst: List[AbstractFormatter] = []

        dataset_name = config.get('dataset_name', None)
        is_formatter_enable = config.get('formatter_pipe', {}).get('enable', False)

        if is_formatter_enable:
            formatter_config_lst = config.get('formatter_pipe', {}).get('formatter', [])
            for formatter_config in formatter_config_lst:
                is_enable = formatter_config.get('enable', False)
                if is_enable:
                    formatter_class = formatter_config.get('python_class', None)
                    class_init_kwargs = formatter_config.get('class_init_kwargs', {})
                    # 根据formatter_class指向的类名，动态加载类，然后实例化一个formatter
                    if formatter_class is None:
                        raise ValueError(f'formatter_class is None, dataset name : {dataset_name}')
                    formatter = load_python_class_by_name(formatter_class, config, class_init_kwargs)
                    self.__formatter_lst.append(formatter)

    def format(self, data: DataJson) -> DataJson:
        """_summary_

        Args:
            data (DataJson): _description_

        Returns:
            DataJson: _description_
        """
        for fmt in self.__formatter_lst:
            data = fmt.format(data)

        return data


# ##########################################################
# extractor chain
# ##########################################################
class ExtractorChain:
    """_summary_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, config: dict):
        """_summary_

        Args:
            config (Dict): 配置文件里的整个配置字典
        """
        self.__pre_extractor_lst: List[AbstractPreExtractor] = []
        self.__extractor_lst: List[AbstractExtractor] = []
        self.__post_extractor_lst: List[AbstractPostExtractor] = []

        dataset_name = config.get('dataset_name', None)
        is_extractor_enable = config.get('extractor_pipe', {}).get('enable', False)
        if not is_extractor_enable:
            return

        # #########################################################
        # 初始化pre_extractor
        # #########################################################
        pre_extractor_config_lst = config.get('extractor_pipe', {}).get('pre_extractor', [])
        for pre_extractor_config in pre_extractor_config_lst:
            pre_extractor_class = pre_extractor_config.get('python_class', None)
            class_init_kwargs = pre_extractor_config.get('class_init_kwargs', {})
            is_extractor_enable = pre_extractor_config.get('enable', False)
            if is_extractor_enable:
                if pre_extractor_class is None:
                    raise ValueError(f'pre_extractor_class is None, dataset name : {dataset_name}')
                pre_extractor = load_python_class_by_name(pre_extractor_class, config, class_init_kwargs)
                self.__pre_extractor_lst.append(pre_extractor)

        # #########################################################
        # 初始化extractor
        # #########################################################
        extractor_config_lst = config.get('extractor_pipe', {}).get('extractor', [])
        for extractor_config in extractor_config_lst:
            extractor_class = extractor_config.get('python_class', None)
            class_init_kwargs = extractor_config.get('class_init_kwargs', {})
            is_extractor_enable = extractor_config.get('enable', False)
            if is_extractor_enable:
                if extractor_class is None:
                    raise ValueError(f'extractor_class is None, dataset name : {dataset_name}')
                extractor = load_python_class_by_name(extractor_class, config, class_init_kwargs)
                self.__extractor_lst.append(extractor)

        # #########################################################
        # 初始化post_extractor
        # #########################################################
        post_extractor_config_lst = config.get('extractor_pipe', {}).get('post_extractor', [])
        for post_extractor_config in post_extractor_config_lst:
            post_extractor_class = post_extractor_config.get('python_class', None)
            class_init_kwargs = post_extractor_config.get('class_init_kwargs', {})
            is_post_extractor_enable = post_extractor_config.get('enable', False)
            if is_post_extractor_enable:
                if post_extractor_class is None:
                    raise ValueError(f'post_extractor_class is None, dataset name : {dataset_name}')
                post_extractor = load_python_class_by_name(post_extractor_class, config, class_init_kwargs)
                self.__post_extractor_lst.append(post_extractor)

    def extract(self, data: DataJson) -> DataJson:
        """_summary_

        Args:
            data (DataJson): _description_

        Returns:
            DataJson: _description_
        """
        for ext in self.__pre_extractor_lst:
            data = ext.pre_extract(data)

        for ext in self.__extractor_lst:
            data = ext.extract(data)

        for ext in self.__post_extractor_lst:
            data = ext.post_extract(data)

        return data


class Pipeline(AbstractPipeline):
    """实现每个数据集一个pipeline的设计模式 所有的pipeline构成一个优先级处理链 format() ---> extract()

    ---> other...
    """

    def __init__(self, config: dict, formatter_chain: FormatterChain, extractor_chain: ExtractorChain):
        """从formatter和extractor初始化一个pipeline.

        Args:
            formatter_lst (List[AbstractFormatter]): _description_
            extractor_chain (ExtractorChain: _description_

        Returns:
            _type_: _description_
        """
        self.__config = config
        self.__formatter_chain: FormatterChain = formatter_chain
        self.__extractor_chain: ExtractorChain = extractor_chain

    @override
    def format(self, data_json: DataJson) -> DataJson:
        """_summary_

        Args:
            data_json (DataJson): _description_

        Returns:
            DataJson: _description_
        """
        self.__validate_format_input(data_json)
        data = self.__formatter_chain.format(data_json)
        return data

    @override
    def extract(self, data_json: DataJson) -> DataJson:
        """_summary_

        Args:
            data_json (DataJson): _description_
        Returns:
            DataJson: DataJson对象
        """
        self.__validate_extract_input(data_json)
        data = self.__extractor_chain.extract(data_json)
        return data

    def __validate_format_input(self, data_json: DataJson):
        """校验一下配置里必须满足的条件，否则抛出异常.

        Args:
            config (dict): _description_
        """
        self.__validate_input_data_format(data_json)

    def __validate_extract_input(self, data_json: DataJson):
        """校验一下配置里必须满足的条件，否则抛出异常.

        Args:
            config (dict): _description_
        """
        self.__validate_input_data_format(data_json)

    def __validate_input_data_format(self, data_json):
        """校验一下输入的data_json对象是否是DataJson对象，否则抛出异常.

        Args:
            data_json (DataJson): _description_
        """
        if not isinstance(data_json, DataJson):
            raise ValueError(f'input data is not DataJson object, data type is {type(data_json)}')  # TODO: 这里应该抛出一个自定义的异常


############################################################
#
# Pipeline工厂方法，用于根据配置生成各种不同的pipeline
#
############################################################


class PipelineSimpleFactory:
    """_summary_"""

    @staticmethod
    def create(config: dict) -> AbstractPipeline:
        """_summary_

        Args:
            config (dict): 完整的配置文件的json字典

        Returns:
            AbstractPipeline: _description_

        Raises:
            ValueError: _description_
        """

        # 检查一下pipeline是否启用，如果没有启用，直接返回None，这样上层在派发数据的时候找不到对应的pipeline实例，就会抛出异常，标记这条数据为异常。
        is_pipeline_enable = config.get('enable', False)
        # 如果没有启用，直接返回None，为什么不可以返回一个空的pipeline呢？因为如果这个步骤被禁止就应该拒绝所有关于这个dataset的数据处理请求，让他们失败，否则不经处理通过管线是不合理的。
        if not is_pipeline_enable:
            return None
        # #########################################################
        # 初始化formatter
        # #########################################################
        formatter_chain = FormatterChain(config)

        # #########################################################
        # 初始化extractor链
        # #########################################################
        # 根据配置生成不同的formatter和extractor，然后实例化一个pipeline
        extractor_chain = ExtractorChain(config)

        # #########################################################
        # 初始化pipeline
        # #########################################################
        pipe = Pipeline(config, formatter_chain, extractor_chain)
        return pipe
