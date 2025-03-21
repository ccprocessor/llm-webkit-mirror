from typing import Dict
import os

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.model.resource_utils import (CACHE_DIR, download_auto_file,
                                              singleton_resource_manager)


CONTENT_STYLE_MAP = {
    "问答": "qna",
    "文章": "article",
    "论坛": "forum",
    "百科": "pedia",
    "书籍": "book",
    "论文": "paper",
}


SAFE_LEVEL_MAP = {
    "safe_source": "safe_source",
    "domestic_source": "domestic_source",
    "other": "other",
}

def auto_download():
    resource_config = load_config()['resources']
    resource_name = "data_source_safe_type"
    domain_list_config: Dict = resource_config[resource_name]
    download_path = domain_list_config['download_path']
    md5 = domain_list_config['md5']
    local_path = os.path.join(CACHE_DIR, f"{resource_name}.csv")
    domain_list_file_path = download_auto_file(download_path, local_path, md5)
    return domain_list_file_path


def build_data_source_map():

    def map_content_style(in_content_style):
        return CONTENT_STYLE_MAP.get(in_content_style, None)

    def map_safe_type(in_safe_type):
        return SAFE_LEVEL_MAP.get(in_safe_type, None)

    data_file = auto_download()
    data_source_map = {}
    with open(data_file, "r") as f:
        lines = f.readlines()

        for i in range(len(lines)):
            if i == 0:
                continue
            line = lines[i]
            line = line.strip()

            line = line.split(",")
            data_source = line[0]
            if len(data_source) == 0:
                continue
            content_style = line[1]
            safe_type = line[2]
            if data_source not in data_source_map:
                # empty content_style string is considered as None
                # empty safe_type string is considered as None
                info_dict = {
                    "content_style": map_content_style(content_style) if len(content_style) > 0 else None,
                    "safe_type": map_safe_type(safe_type) if len(safe_type) > 0 else None,
                }
                data_source_map[data_source] = info_dict
            else:
                raise Exception("data_source: %s already exists" % data_source)
    return data_source_map


def get_data_source_map():
    resource_name = "data_source_safety_map"
    if not singleton_resource_manager.has_name(resource_name):
        singleton_resource_manager.set_resource(resource_name, build_data_source_map())
    return singleton_resource_manager.get_resource(resource_name)

def lookup_safe_type_by_data_source(data_source: str) -> str:
    data_source_map = get_data_source_map()
    if data_source in data_source_map:
        return data_source_map[data_source]["safe_type"]
    return None

def decide_domestic_source_by_data_source(data_source: str) -> bool:
    return lookup_safe_type_by_data_source(data_source) == "domestic_source"

def decide_safe_source_by_data_source(data_source: str) -> bool:
    return lookup_safe_type_by_data_source(data_source) == "safe_source"

class SourceFilter:
    def __init__(self):
        pass

    def filter(
        self,
        content_str: str,
        language: str,
        data_source: str,
        language_details: str,
        content_style: str,
    ) -> dict:
        from_safe_source = decide_safe_source_by_data_source(data_source)
        from_domestic_source = decide_domestic_source_by_data_source(data_source)
        return {'from_safe_source': from_safe_source, 'from_domestic_source': from_domestic_source}
