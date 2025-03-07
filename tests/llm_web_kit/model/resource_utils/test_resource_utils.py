from unittest.mock import patch

from llm_web_kit.model.resource_utils.utils import try_remove


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
