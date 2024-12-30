from pathlib import Path

import commentjson as json

from llm_web_kit.exception.exception import PipelineInitExp
from llm_web_kit.input.datajson import DataJsonKey
from llm_web_kit.libs.logger import mylogger
from llm_web_kit.pipeline.pipeline import PipelineSimpleFactory


class PipelineSuit(object):
    """实现数据集处理pipeline的按需实例化，并调用方法的设计模式 从数据源到数据集的处理链 例如，从文件到contentList的处理链."""

    def __init__(self, config: str | dict):
        """从参数指定的配置文件中读取配置并初始化这个流水线链.

        Args:
            config (str|dict): 配置文件的路径,可以指向一个具体的jsonc文件，也可以是一个包含配置的字典对象，或者包含了很多个jsonc文件的目录
        """
        self.__pipelines = {}  # "dataset_name" => pipeline
        self.__config = {}  # "dataset_name" => config

        config_files = []
        if isinstance(config, str):
            pth = Path(config)
            if not pth.exists():
                raise PipelineInitExp(f'Config file {config} does not exist.')
            if pth.is_dir():
                config_files = [str(p) for p in Path(config).rglob('*.json')]
            else:
                config_files.append(config)

            for config_file in config_files:
                cfg = self.load_config_file(config_file_path=config_file)
                dataset_name = cfg.get(DataJsonKey.DATASET_NAME, None)
                if not dataset_name:
                    raise PipelineInitExp(f"JSON config object must be a dictionary containing '{DataJsonKey.DATASET_NAME}'.")
                else:
                    self.__config[dataset_name] = cfg
        elif isinstance(config, dict):
            dataset_name = config.get(DataJsonKey.DATASET_NAME, None)
            if not dataset_name:
                raise PipelineInitExp(f"JSON config object must be a dictionary containing '{DataJsonKey.DATASET_NAME}'.")
            else:
                self.__config[dataset_name] = config
        else:
            raise PipelineInitExp('Config must be a path to a jsonc file or a dictionary.')

    @staticmethod
    def load_config_file(config_file_path: str):
        """从配置文件中加载配置.

        Args:
            config_file_path (str): 配置文件的路径
        """
        with open(config_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def __getattr__(self, method_name):
        """ 动态转发方法到具体和dataset_name绑定的pipeline实例上
        例如：
        pipsuit = PipelineSuit("/path/to/datasource_config.jsonc")
        pipsuit.extract({"dataset_name": "zlib"}) # 此时会调用zlib的pipeline实例的extract方法

        Args:
            method_name (_type_): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            AttributeError: _description_

        Returns:
            _type_: _description_
        """

        # 这个方法会在访问的属性在PipelineSuit中不存在时被调用
        def method(*args, **kwargs):
            if not args:
                raise PipelineInitExp("First argument must be the JSON object containing 'dataset_name'.")

            json_obj = args[0]
            if not isinstance(json_obj, dict) or DataJsonKey.DATASET_NAME not in json_obj:
                raise PipelineInitExp("JSON object must be a dictionary containing 'dataset_name'.")

            dataset_name = json_obj[DataJsonKey.DATASET_NAME]
            pipeline = self._PipelineSuit__pipelines.get(dataset_name)

            if not pipeline:
                try:
                    pipeline_config = self._PipelineSuit__config[dataset_name]
                    pipeline = PipelineSimpleFactory.create(pipeline_config)
                    self._PipelineSuit__pipelines[dataset_name] = pipeline
                except KeyError:
                    raise PipelineInitExp(f'Dataset name {dataset_name} is not found in the configuration file.')
                except ValueError as e:
                    mylogger.exception(e)
                    raise PipelineInitExp(
                        f'Failed to initialize pipeline for dataset: {dataset_name}, check pipeline config file of this dataset.') from e
                except Exception as e:
                    mylogger.exception(e)
                    raise PipelineInitExp(f'Failed to initialize pipeline for dataset: {dataset_name}') from e

            # 检查Pipeline实例是否有这个方法
            if not hasattr(pipeline, method_name):
                raise PipelineInitExp(f'The method {method_name} is not defined in the pipeline for dataset: {dataset_name}')

            # 调用Pipeline实例的方法
            return getattr(pipeline, method_name)(*args, **kwargs)

        return method
