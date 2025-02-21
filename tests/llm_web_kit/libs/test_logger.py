import os
import unittest
from datetime import datetime as dt

from llm_web_kit.libs.logger import init_logger


class TestLogger(unittest.TestCase):

    def setUp(self):
        self.config = {
            'logger': [{
                'to': 'sys.stdout',
                'log-level': 'DEBUG',
                'log-format': '{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}',
            }, {
                'to': '/tmp/logs/test-{time:YYYY-MM-DD}.log',
                'rotation': '1 day',
                'retention': '10 days',
                'log-level': 'INFO'
            }, {
                'to': '/tmp/logs/error-{time:YYYY-MM-DD}.log',
                'rotation': '1 day',
                'retention': '10 days',
                'log-level': 'ERROR'
            }]
        }
        self.info_log_file = '/tmp/logs/test-{time}.log'.format(time=dt.now().strftime('%Y-%m-%d'))
        self.error_log_file = '/tmp/logs/error-{time}.log'.format(time=dt.now().strftime('%Y-%m-%d'))

    def tearDown(self):
        # 删除生成的日志文件
        try:
            if os.path.exists(self.info_log_file):
                os.remove(self.info_log_file)
            if os.path.exists(self.error_log_file):
                os.remove(self.error_log_file)
        except Exception:
            pass

    def test_init_logger_with_config(self):
        log = init_logger(self.config)
        self.assertIsNotNone(log)
        self.assertEqual(len(log._core.handlers), 3)

    def test_log_file_content(self):
        log = init_logger(self.config)
        log.debug('This is a debug message')
        log.info('This is an info message')
        log.warning('This is a warning message')
        log.error('This is an error message')
        log.complete()

        # 检查info日志文件是否存在
        self.assertTrue(os.path.exists(self.info_log_file))

        # 检查info日志文件内容
        with open(self.info_log_file, 'r') as f:
            lines = f.readlines()
            self.assertGreaterEqual(len(lines), 3)
            self.assertIn('INFO', lines[0])
            self.assertIn('This is an info message', lines[0])
            self.assertIn('WARNING', lines[1])
            self.assertIn('This is a warning message', lines[1])
            self.assertIn('ERROR', lines[2])
            self.assertIn('This is an error message', lines[2])

        # 检查error日志文件是否存在
        self.assertTrue(os.path.exists(self.error_log_file))

        # 检查error日志文件内容
        with open(self.error_log_file, 'r') as f:
            lines = f.readlines()
            self.assertGreaterEqual(len(lines), 1)
            self.assertIn('ERROR', lines[0])
            self.assertIn('This is an error message', lines[0])
