import unittest

from llm_web_kit.exception.exception import ErrorMsg, LlmWebKitBaseActException


class TestException(unittest.TestCase):
    """test Exception."""

    def process_positive_number(self, value):
        """
        test case for except
        Args:
            value:
        Returns:
        """
        if value < 0:
            raise LlmWebKitBaseActException('Value cannot be negative')
        return value * 2

    def test_llm_web_kit_base_exp(self):
        """test LlmWebKitBaseExp."""
        with self.assertRaises(LlmWebKitBaseActException) as cm:
            self.process_positive_number(-1)
        self.assertEqual(str(cm.exception.err_code), str(1000))

    def test_ErrorMsg(self):
        """test error msg."""
        res = ErrorMsg.get_error_message(1000)
        assert res == 'LlmWebKitBase error'
        res = ErrorMsg.get_error_message(2000)
        assert res == 'ExtractorChain base error'
        res = ErrorMsg.get_error_message(2100)
        assert res == 'Failed to initialize extractor'
        res = ErrorMsg.get_error_message(2200)
        assert res == 'Invalid input data format for ExtractorChain'
        res = ErrorMsg.get_error_message(2300)
        assert res == 'ExtractorChain configuration error'
        res = ErrorMsg.get_error_message(2400)
        assert res == 'Specified extractor not found'
        res = ErrorMsg.get_error_message(7000)
        assert res == 'Clean base error'
        res = ErrorMsg.get_error_message(7010)
        assert res == 'Clean lang type error'
