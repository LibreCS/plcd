
import unittest
from src.plcd.ping import portValid

PORT = [0, 50001, 443]
PORT_STATUS = [False, False, True]
PORT_SCAN_MAX = 50000

class PortTest(unittest.TestCase):
 
    def test_portValid(self):
    
        for i in PORT:
            self.assertEqual(portValid(PORT[i]), PORT_STATUS[i])


if __name__ == '__main__':
    unittest.main()
  
