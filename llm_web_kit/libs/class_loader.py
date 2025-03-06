import importlib


def load_python_class_by_name(class_name: str, config: dict, init_kwargs: dict):
    """根据类名动态加载类，并实例化一个对象.

    Args:
        class_name (str): 类名，格式为"模块名.pkg....类名", 例如"llm_web_kit.extractor.html.extractor.HTMLFileFormatExtractor"
        config (dict): 从文件里读取的配置
        init_kwargs (dict): 初始化参数

    Returns:
        object: 类的实例
    """
    module_name, class_name = class_name.rsplit('.', 1)  # 分割模块名和类名
    module = importlib.import_module(module_name)  # 动态导入模块
    _class = getattr(module, class_name)  # 从模块中获取类
    class_instance = _class(config=config, **init_kwargs)  # 实例化类
    return class_instance
