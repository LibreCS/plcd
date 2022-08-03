
import unittest
from src.plcd.ping import ping()
from src.plcd.ping import portSniff
from src.plcd.ping import configure()



class PingTest(unittest.TestCase):
 
    def test_ping(self):
    
        # test case goes here


class SniffTest(unittest.TestCase):
 
    def test_portSniff(self):
    
        # test case goes here

class ConfigTest(unittest.TestCase):

    def test_configure(self):

if __name__ == '__main__':
    unittest.main()
