"""Test cases for domain_safety_detector.py."""

import unittest
from unittest.mock import MagicMock, patch

from llm_web_kit.model.domain_safety_detector import (
    DomainChecker, DomainFilter, auto_download, decide_domain_level,
    domain_type_val, get_domain_dict, get_domain_level_checker, get_domain_seq,
    get_url_domain, get_url_domain_seq, get_url_parts, is_ip_address,
    release_domain_level_detecter)


class TestDomainSafetyDetector(unittest.TestCase):
    """Test cases for domain safety detector functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = [
            b'{"domain": "example.com", "type": "whitelist"}',
            b'{"domain": "test.cn", "type": "blacklist"}',
            b'{"domain": "unknown.com", "type": "silverlist"}',
        ]

    def test_get_url_parts(self):
        """Test URL parsing functionality."""
        # Test with full URL
        url = 'https://example.com:8080/path?param=value#fragment'
        parts = get_url_parts(url)
        self.assertEqual(parts, ('https', 'example.com', '8080', '/path', '?param=value', '#fragment'))

        # Test with minimal URL
        url = 'http://example.com'
        parts = get_url_parts(url)
        self.assertEqual(parts, ('http', 'example.com', '', '', '', ''))

        # Test with empty URL
        self.assertIsNone(get_url_parts(''))
        self.assertIsNone(get_url_parts(None))

    def test_get_url_domain(self):
        """Test domain extraction from URL."""
        # Test with full URL
        self.assertEqual(get_url_domain('https://example.com:8080/path'), 'example.com')

        # Test with minimal URL
        self.assertEqual(get_url_domain('http://example.com'), 'example.com')

        # Test with invalid URL
        self.assertIsNone(get_url_domain(''))
        self.assertIsNone(get_url_domain(None))

    def test_is_ip_address(self):
        """Test IP address validation."""
        # Test valid IP addresses
        self.assertTrue(is_ip_address('192.168.1.1'))
        self.assertTrue(is_ip_address('10.0.0.0'))
        self.assertTrue(is_ip_address('256.256.256.256'))

        # Test invalid IP addresses
        self.assertFalse(is_ip_address('1.1.1'))
        self.assertFalse(is_ip_address(''))
        self.assertFalse(is_ip_address(None))

    def test_get_domain_seq(self):
        """Test domain sequence generation."""
        # Test with regular domain
        self.assertEqual(get_domain_seq('sub.example.com'), ['sub.example.com', 'example.com'])

        # Test with IP address
        self.assertEqual(get_domain_seq('192.168.1.1'), ['192.168.1.1'])

        # Test with secondary domain
        self.assertEqual(get_domain_seq('sub.example.co.uk'), ['sub.example.co.uk', 'example.co.uk'])

        # Test with empty domain
        self.assertEqual(get_domain_seq(''), [])
        self.assertEqual(get_domain_seq(None), [])

    def test_get_url_domain_seq(self):
        """Test URL domain sequence generation."""
        # Test with regular URL
        self.assertEqual(get_url_domain_seq('https://sub.example.com'), ['sub.example.com', 'example.com'])

        # Test with IP URL
        self.assertEqual(get_url_domain_seq('http://192.168.1.1'), ['192.168.1.1'])

        # Test with empty URL
        self.assertEqual(get_url_domain_seq(''), [])
        self.assertEqual(get_url_domain_seq(None), [])

    def test_domain_type_val(self):
        """Test domain type value mapping."""
        # Test valid types
        self.assertEqual(domain_type_val('whitelist'), 1)
        self.assertEqual(domain_type_val('blacklist'), 2)
        self.assertEqual(domain_type_val('silverlist'), 3)
        self.assertEqual(domain_type_val('graylist'), 4)

        # Test invalid type
        self.assertEqual(domain_type_val('unknown'), 100)

    @patch('llm_web_kit.model.domain_safety_detector.download_auto_file')
    @patch('llm_web_kit.model.domain_safety_detector.load_config')
    def test_auto_download(self, mock_load_config, mock_download):
        """Test auto_download function."""
        mock_load_config.return_value = {
            'resources': {
                'domain_blacklist': {
                    'download_path': 'http://example.com/test.json',
                    'md5': 'test_md5',
                },
            },
        }
        mock_download.return_value = 'test_path.json'

        result = auto_download()
        self.assertEqual(result, 'test_path.json')
        mock_download.assert_called_once()

    @patch('llm_web_kit.model.domain_safety_detector.auto_download')
    def test_get_domain_dict(self, mock_auto_download):
        """Test domain dictionary creation."""
        mock_auto_download.return_value = 'test.json'

        with patch('builtins.open', unittest.mock.mock_open(read_data=b'\n'.join(self.test_data))):
            result = get_domain_dict()

            self.assertIn('example.com', result)
            self.assertIn('test.cn', result)
            self.assertIn('unknown.com', result)

            self.assertEqual(result['example.com'], 'whitelist')
            self.assertEqual(result['test.cn'], 'blacklist')
            self.assertEqual(result['unknown.com'], 'silverlist')

    @patch('llm_web_kit.model.domain_safety_detector.singleton_resource_manager')
    def test_get_domain_level_checker(self, mock_manager):
        """Test domain level checker creation."""
        mock_manager.has_name.return_value = True
        mock_checker = MagicMock()
        mock_manager.get_resource.return_value = mock_checker

        checker = get_domain_level_checker()

        self.assertEqual(checker, mock_checker)
        mock_manager.get_resource.assert_called_once_with('domain_level_checker')

    @patch('llm_web_kit.model.domain_safety_detector.singleton_resource_manager')
    def test_release_domain_level_detecter(self, mock_manager):
        """Test domain level detector release."""
        release_domain_level_detecter()
        mock_manager.release_resource.assert_called_once_with('domain_level_checker')

    @patch('llm_web_kit.model.domain_safety_detector.get_domain_level_checker')
    @patch('llm_web_kit.model.domain_safety_detector.get_url_domain_seq')
    def test_decide_domain_level(self, mock_get_seq, mock_get_checker):
        """Test domain level decision."""
        mock_checker = MagicMock()
        mock_checker.get_domain_level.return_value = 'blacklist'
        mock_get_checker.return_value = mock_checker
        mock_get_seq.return_value = ['example.com']

        result = decide_domain_level('https://example.com')

        self.assertEqual(result, 'blacklist')
        mock_checker.get_domain_level.assert_called_once_with(['example.com'])


class TestDomainChecker(unittest.TestCase):
    """Test cases for DomainChecker class."""

    @patch('llm_web_kit.model.domain_safety_detector.get_domain_dict')
    def setUp(self, mock_get_domain_dict):
        """Set up test fixtures."""
        mock_get_domain_dict.return_value = {
            'example.com': 'whitelist',
            'test.cn': 'blacklist',
            'unknown.com': 'silverlist',
        }
        self.checker = DomainChecker()

    def test_get_domain_level(self):
        """Test domain level checking."""
        # Test with whitelist domain
        self.assertEqual(self.checker.get_domain_level(['example.com']), 'whitelist')

        # Test with blacklist domain
        self.assertEqual(self.checker.get_domain_level(['test.cn']), 'blacklist')

        # Test with unknown domain
        self.assertEqual(self.checker.get_domain_level(['unknown.com']), 'silverlist')

        # Test with empty domain sequence
        self.assertEqual(self.checker.get_domain_level([]), '')

        # Test with multiple domains (should return lowest level)
        self.assertEqual(self.checker.get_domain_level(['example.com', 'test.cn']), 'whitelist')


class TestDomainFilter(unittest.TestCase):
    """Test cases for DomainFilter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.filter = DomainFilter()

    @patch('llm_web_kit.model.domain_safety_detector.decide_domain_level')
    def test_filter(self, mock_decide_level):
        """Test filter method."""
        # Test with blacklist domain
        mock_decide_level.return_value = 'blacklist'
        result = self.filter.filter(
            content_str='Content from blacklist',
            language='en',
            url='https://test.cn',
            language_details='formal',
            content_style='article',
        )
        self.assertFalse(result[0])
        self.assertEqual(result[1], {'domain_level': 'blacklist'})

        # Test with non-blacklist domain
        mock_decide_level.return_value = 'whitelist'
        result = self.filter.filter(
            content_str='Content from whitelist',
            language='en',
            url='https://example.com',
            language_details='formal',
            content_style='article',
        )
        self.assertTrue(result[0])
        self.assertEqual(result[1], {'domain_level': 'whitelist'})


if __name__ == '__main__':
    unittest.main()
