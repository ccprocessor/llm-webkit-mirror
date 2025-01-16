import unittest

from llm_web_kit.exception.exception import ErrorMsg, LlmWebKitBaseActException


class TestException(unittest.TestCase):
    """test Exception."""

    def process_positive_number(self, value):
        """
        test case for except
        Args:
            n:
        Returns:
        """
        if value < 0:
            raise LlmWebKitBaseActException('Value cannot be negative')
        return value * 2

    def test_llmwebkitbaseexp(self):
        """test llm webkitexp."""
        with self.assertRaises(LlmWebKitBaseActException) as cm:
            self.process_positive_number(-1)
        self.assertEqual(str(cm.exception.err_code), str(1000))

    def test_ErrorMsg(self):
        """test error msg."""
        res = ErrorMsg.get_error_message(str(1000))
        assert res == 'LlmWebKitBase error'
        res = ErrorMsg.get_error_message(str(2000))
        assert res == 'PipeLine input data_json error'
        res = ErrorMsg.get_error_message(str(3000))
        assert res == 'pipeline suit init error'
