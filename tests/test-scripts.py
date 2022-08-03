
import unittest
from src.plcd.ping import hostValid
from src.plcd.ping import portValid
from src.plcd.ping import calculate_time

HOST = ["10.0.0.1", "256.1.1.1", "1.1.1", "1.1.1.1.1"]
HOST_STATUS = [True, False, False, False]

PORT = [0, 50001, 443]
PORT_STATUS = [False, False, True]


class PortTest(unittest.TestCase):
 
    def test_portValid(self):

        # test case goes here
    
        for i in PORT:
            self.assertEqual(portValid(PORT[i]), PORT_STATUS[i])


class HostTest(unittest.TestCase):
 
    def test_hostValid(self):
    
        # test case goes here

        for i in HOST:
            self.assertEqual(hostValid(HOST[i]), HOST_STATUS[i])

class TimeTest(unittest.TestCase):

    def test_calculate_time(self):

        # test case goes here

if __name__ == '__main__':
    unittest.main()
