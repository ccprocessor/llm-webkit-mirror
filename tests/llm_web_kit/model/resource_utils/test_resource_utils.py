import os
from unittest.mock import patch

from llm_web_kit.model.resource_utils.utils import decide_cache_dir, try_remove


class Test_try_remove:

    @patch('os.remove')
    def test_remove(self, removeMock):
        try_remove('path')
        removeMock.assert_called_once_with('path')

    @patch('os.remove')
    def test_remove_exception(self, removeMock):
        removeMock.side_effect = Exception
        try_remove('path')
        removeMock.assert_called_once_with('path')


class TestDecideCacheDir:

    @patch('os.environ', {'WEB_KIT_CACHE_DIR': '/env/cache_dir'})
    @patch('llm_web_kit.model.resource_utils.utils.load_config')
    def test_only_env(self, get_config_mock):
        get_config_mock.side_effect = Exception
        cache_dir, cache_tmp_dir = decide_cache_dir()
        assert cache_dir == '/env/cache_dir'
        assert cache_tmp_dir == '/env/cache_dir/tmp'

    @patch('os.environ', {})
    @patch('llm_web_kit.model.resource_utils.utils.load_config')
    def test_only_config(self, get_config_mock):
        get_config_mock.return_value = {
            'resources': {'common': {'cache_path': '/config/cache_dir'}}
        }

        cache_dir, cache_tmp_dir = decide_cache_dir()
        assert cache_dir == '/config/cache_dir'
        assert cache_tmp_dir == '/config/cache_dir/tmp'

    @patch('os.environ', {})
    @patch('llm_web_kit.model.resource_utils.utils.load_config')
    def test_default(self, get_config_mock):
        get_config_mock.side_effect = Exception
        env_result = os.path.expanduser('~/.llm_web_kit_cache')
        cache_dir, cache_tmp_dir = decide_cache_dir()
        assert cache_dir == env_result
        assert cache_tmp_dir == f'{env_result}/tmp'

    @patch('os.environ', {'WEB_KIT_CACHE_DIR': '/env/cache_dir'})
    @patch('llm_web_kit.model.resource_utils.utils.load_config')
    def test_priority(self, get_config_mock):
        get_config_mock.return_value = {
            'resources': {'common': {'cache_path': '/config/cache_dir'}}
        }
        cache_dir, cache_tmp_dir = decide_cache_dir()
        assert cache_dir == '/config/cache_dir'
        assert cache_tmp_dir == '/config/cache_dir/tmp'
