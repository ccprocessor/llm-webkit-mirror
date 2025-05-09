import unittest

from cc_store.libs.domain import compute_domain_hash, extract_domain


class TestDomainFunctions(unittest.TestCase):
    """测试cc_store.libs.domain模块中的函数."""

    def test_compute_domain_hash(self):
        """测试计算域名哈希值的函数."""
        # 测试正常情况
        self.assertEqual(compute_domain_hash("example.com", 100), 85)
        self.assertEqual(compute_domain_hash("test.org", 1000), 561)

        # 测试特殊情况
        self.assertIsNone(compute_domain_hash(None, 100))

        # 测试哈希值范围
        hash_count = 100
        domain = "example.com"
        hash_value = compute_domain_hash(domain, hash_count)
        self.assertTrue(0 <= hash_value < hash_count)

    def test_extract_domain(self):
        """测试从URL中提取域名的函数."""
        # 测试正常URL
        self.assertEqual(extract_domain("https://www.example.com/path"), "www.example.com")
        self.assertEqual(extract_domain("http://test.org"), "test.org")
        self.assertEqual(extract_domain("https://sub.domain.co.uk/path?query=1"), "sub.domain.co.uk")

        # 测试不同协议
        self.assertEqual(extract_domain("ftp://files.example.com"), "files.example.com")

        # 测试大小写转换
        self.assertEqual(extract_domain("https://EXAMPLE.COM"), "example.com")

        # 测试特殊情况
        self.assertIsNone(extract_domain(None))
        self.assertIsNone(extract_domain("invalid-url"))
        self.assertIsNone(extract_domain("http://"))
