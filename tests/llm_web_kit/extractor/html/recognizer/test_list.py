import os
import unittest

from llm_web_kit.extractor.html.recognizer.list import ListRecognizer


class TestSimpleListRecognize(unittest.TestCase):
    def setUp(self):
        self.__list_recognize = ListRecognizer()
        self.__simple_list_content = None
        self.__complex_list_content = None

        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/simple_list.html', 'r') as file:
            self.__simple_list_content = file.read()

        with open(f'{os.path.dirname(os.path.abspath(__file__))}/assets/recognizer/complex_list.html', 'r') as file:
            self.__complex_list_content = file.read()

    def test_simple_list(self):
        html_part = self.__list_recognize.recognize('http://url.com', [(self.__simple_list_content, self.__complex_list_content)], self.__simple_list_content)
        assert len(html_part) == 6

    def test_complex_list(self):
        # TODO: Fix this test
        html_part = self.__list_recognize.recognize('http://url.com', [(self.__simple_list_content, self.__complex_list_content)], self.__complex_list_content)
        assert len(html_part) == 6
