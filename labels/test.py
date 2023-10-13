import unittest
import numpy as np
from labelgen import *

np.random.seed(123) 
data = np.zeros(1000) + np.random.randn(1000)

class TestLabelFunctions(unittest.TestCase):

    def testEW(self):
        self.assertIsNone(np.testing.assert_allclose(ew(data[0:3]), np.array([1.98019802, 1.96078816, 1.94176265])))

    def testWSD(self):
        self.assertAlmostEqual(wsd(data[:3], ew(data[:3])), 0.8666347566309145)
    
    def testEWMSD(self):
        self.assertIsNone(np.testing.assert_allclose(ewmsd(data[0:3], 1), np.array([0., 1.04147539, 0.86663476])))

    def testSTBL(self):
        self.assertEqual(stbl(data[0:3], wsd(data[0:3], ew(data[0:3]))), 1)
        self.assertEqual(stbl(data[0:3][::-1], wsd(data[0:3][::-1], ew(data[0:3]))), 3)
        self.assertEqual(stbl(data[0:3], 10), 2)

    def testDTBL(self):
        self.assertEqual(dtbl(data[0:3], np.array([0.86663476, 0.68429625])), 1)
        self.assertEqual(dtbl(data[0:3][::-1], np.array([0.86663476, 0.68429625])), 3)
        self.assertEqual(dtbl(data[0:3], np.array([10, 20])), 2)

if __name__ == '__main__':
    unittest.main()