# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

SNIFF_TEST_IP = "185.199.109.153"
SNIFF_TEST_PORT = 443

import unittest

from plcd.main import portSniff

class SniffTest(unittest.TestCase):

    def test_portIngest(self):
        self.assertEqual(portSniff(SNIFF_TEST_IP), SNIFF_TEST_PORT)


if __name__ == '__main__':
    unittest.main()
