import unittest

from src.proxy_checker import check_proxy_account


class TestProxyChecker(unittest.TestCase):
    def test_proxy_account(self):
        proxy = "proxy1:port1"
        account = "account1:password1"
        result = check_proxy_account(proxy, account)
        self.assertTrue(result)
