import os
from typing import List, Union

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.html_classify.model import Markuplm
from llm_web_kit.model.resource_utils import (CACHE_DIR, download_auto_file,
                                              get_unzip_dir, unzip_local_file)


class HTMLLayoutClassifier:
    def __init__(self, model_path: str = None, device: str = 'cuda'):
        if not model_path:
            model_path = self.auto_download()
        self.model = Markuplm(model_path, device)

    def auto_download(self) -> str:
        """Default download the html_cls_25m4.zip model."""
        resource_name = 'html_cls-25m4'
        resource_config = load_config()['resources']
        print(resource_config)
        model_config: dict = resource_config[resource_name]
        model_config_s3 = model_config['download_path']
        model_config_md5 = model_config.get('md5', '')
        # get the zip path calculated by the s3 path
        zip_path = os.path.join(CACHE_DIR, f'{resource_name}.zip')
        # the unzip path is calculated by the zip path
        unzip_path = get_unzip_dir(zip_path)
        logger.info(f'try to make unzip_path: {unzip_path} exist')
        # if the unzip path does not exist, download the zip file and unzip it
        if not os.path.exists(unzip_path):
            logger.info(f'unzip_path: {unzip_path} does not exist')
            logger.info(f'try to unzip from zip_path: {zip_path}')
            if not os.path.exists(zip_path):
                logger.info(f'zip_path: {zip_path} does not exist')
                logger.info(f'downloading {model_config_s3}')
                zip_path = download_auto_file(
                    model_config_s3, zip_path, model_config_md5
                )
            logger.info(f'unzipping {zip_path}')
            unzip_path = unzip_local_file(zip_path, unzip_path)
        return unzip_path

    def predict(self, html_str_input: Union[str, List[str]]) -> Union[str, List[str]]:
        """predict the layout type of the html string.

        Example:
            html_str_input = ["<html>layout1</html>", "<html>layout2</html>"]
            layout_type = model.predict(html_str_input)
            print(layout_type)
            # [{'pred_prob': 0.98, 'pred_label': "article"}, {'pred_prob': 0.99, 'pred_label': "forum"}]
        Args:
            html_str_input (Union[str, List[str]]): The html string or a list of html strings

        Returns:
            Union[str, List[str]]: The layout type of the html string or a list of layout types
        """
        one_input = isinstance(html_str_input, str)

        if one_input:
            html_str_input = [html_str_input]

        # predict the layout type of the html string
        results = self.model.inference_batch(html_str_input)

        if one_input:
            results = results[0]

        return results


if __name__ == '__main__':
    model = HTMLLayoutClassifier()
    html_str_input = ['<html>layout1</html>', '<html>layout2</html>']
    layout_type = model.predict(html_str_input)
    print(layout_type)
