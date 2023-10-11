import unittest
from labelgen import *

data = np.zeros(1000) + np.random.randn(1000)

class TestLabelFunctions(unittest.TestCase):

    def TestEW(self):
        self.assertEqual(EW(data, 1, 1), 1 + np.exp(np.linspace(0, 1000, endpoint=True) * -1))

    def TestWSD(self):
        None
    
    def TestEWMSD(self):
        None

    def TestSTBL(self):
        None

    def TestDTBL(self):
        None

if __name__ == '__main__':
    unittest.main()