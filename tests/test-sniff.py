
import unittest
from plcd.main import portSniff

SNIFF_TEST_IP = "185.199.109.153"
SNIFF_TEST_PORT = 443

class SniffTest(unittest.TestCase):
 
    def test_portSniff(self):
        self.assertEqual(portSniff(SNIFF_TEST_IP), SNIFF_TEST_PORT)
 
 
if __name__ == '__main__':
    unittest.main()
