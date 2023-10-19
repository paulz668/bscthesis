import unittest
import pandas as pd
from labelgen import *

a = pd.Series([1,2,3,4,5])
b = a.ewm(span=100).std()

print(pct_change(a, 3))

class TestLabelFunctions(unittest.TestCase):

    def testpct_change(self):
        self.assertEqual(pct_change(a, 4), 2.5)
        self.assertEqual(pct_change(a, 3), 2)

    def testslm(self):
        self.assertEqual(slm(0.1), 1)
        self.assertEqual(slm(1, 2), 2)
        self.assertEqual(slm(-0.003), 3)

    def teststbml(self):
        self.assertEqual(stbml(a, b.iloc[1]), 1)
        self.assertEqual(stbml(a, 10), 2)
        self.assertEqual(stbml(a.iloc[::-1], b.iloc[1]), 3)

    def testdtbml(self):
        self.assertEqual(dtbml(a, b.iloc[1:]), 1)
        self.assertEqual(dtbml(a, pd.Series([2,4,6,8])), 2)
        self.assertEqual(dtbml(a.iloc[::-1], b.iloc[1:]), 3)

if __name__ == '__main__':
    unittest.main()