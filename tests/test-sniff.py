
import unittest
from src.plcd.ping import portSniff
from src.plcd.ping import portIngest
from src.plcd.ping import PLC_PORT_DEFINITIONS

SNIFF_TEST_IP = "185.199.109.153"
SNIFF_TEST_PORT = 443

portName = [str("")]*PLC_PORT_DEFINITIONS
portNum = [int(0)]*PLC_PORT_DEFINITIONS

class SniffTest(unittest.TestCase):

    portIngest()

    def test_portIngest(self):
        self.assertEqual(portSniff(SNIFF_TEST_IP), SNIFF_TEST_PORT)


if __name__ == '__main__':
    unittest.main()
