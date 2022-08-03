
import unittest
from src.plcd.ping import hostValid

HOST = ["10.0.0.1", "256.1.1.1", "1.1.1", "1.1.1.1.1"]
HOST_STATUS = [True, False, False, False]

class HostTest(unittest.TestCase):
 
    def test_hostValid(self):
    
        for i in HOST:
            self.assertEqual(hostValid(HOST[i]), HOST_STATUS[i])


if __name__ == '__main__':
    unittest.main()
