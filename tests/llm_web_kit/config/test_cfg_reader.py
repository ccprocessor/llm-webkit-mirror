
import os
import unittest

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.exception.exception import ModelResourceException


class TestCfgReader(unittest.TestCase):
    """Test cases for the config reader module."""
    def test_get_config_path(self):
        """Test the get_config_path function with different scenarios."""
        # Test when environment variable is set
        # Test with non-existent file path in environment variable
        os.environ['LLM_WEB_KIT_CFG_PATH'] = '/path/to/nonexistent/config.jsonc'
        with self.assertRaises(ModelResourceException):
            load_config()

        # Test with suppress_error=True
        config = load_config(suppress_error=True)
        assert config == {}

        # Clean up environment variable
        del os.environ['LLM_WEB_KIT_CFG_PATH']
