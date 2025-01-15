import unittest

from llm_web_kit.exception.exception import (ErrorMsg, LlmWebKitBaseException,
                                             PipelineInputExp)


class TestException(unittest.TestCase):
    """test Exception."""
    def test_llmwebkitbaseexp(self):
        """test llm webkitexp."""
        try:
            raise LlmWebKitBaseException(1000, 'check pipeline config file of this dataset')
        except LlmWebKitBaseException as e:
            print(e)

    def test_pipelineinputexp(self):
        """test pipeline input exp."""
        try:
            raise PipelineInputExp(custom_message='pipelint init exp')
        except LlmWebKitBaseException as e:
            print(e)

    def test_ErrorMsg(self):
        """test error msg."""
        res = ErrorMsg.get_error_message(str(1000))
        assert res == 'LlmWebKitBase error'
        res = ErrorMsg.get_error_message(str(2000))
        assert res == 'PipeLine input data_json error'
        res = ErrorMsg.get_error_message(str(3000))
        assert res == 'pipeline suit init error'
