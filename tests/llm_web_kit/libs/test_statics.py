import unittest

from llm_web_kit.libs.statics import Statics


class TestStatics(unittest.TestCase):
    def test_statics(self):
        statics = Statics({'table': 10, 'list': 5, 'list.text': 10})
        self.assertEqual(statics.__getitem__('table'), 10)
        self.assertEqual(statics.__getitem__('list'), 5)
        self.assertEqual(statics.__getitem__('list.text'), 10)
        statics.print()

    def test_merge_statics(self):
        statics = Statics({'table': 10, 'list': 5, 'list.text': 10})
        statics.merge_statics({'table': 10, 'list': 5, 'list.text': 10})
        self.assertEqual(statics.__getitem__('table'), 20)
        self.assertEqual(statics.__getitem__('list'), 10)
