import unittest
import numpy as np
from labelgen import *

np.random.seed(123) 
data = np.zeros(1000) + np.random.randn(1000)

class TestLabelFunctions(unittest.TestCase):

    def testEW(self):
        self.assertIsNone(np.testing.assert_allclose(EW(data[0:3]), np.array([0.9862327 , 0.97265495, 0.95926412])))

    def testWSD(self):
        self.assertTrue(True)
    
    def testEWMSD(self):
        self.assertTrue(True)

    def testSTBL(self):
        self.assertTrue(True)

    def testDTBL(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()