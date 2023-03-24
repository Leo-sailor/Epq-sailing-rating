import unittest
from LocalDependencies.General import General
from LocalDependencies.Main_core import Csvcode
g = General()

class TestSum(unittest.TestCase):

    def test1(self):
        self.assertEqual(g.multiindex([0,1,1,5],1), [1,2], "Failed")
    def test2(self):
        self.assertEqual(g.multiindex([0, 1, 1, 5], 5), [3], "Failed")
    def test3(self):
        c = Csvcode("topper5.3", "LeoLeo99!")
        self.assertEqual(c.getsailorid(-1, "joseph rowe"), 'gb-4036-joero', "Failed")
    def test4(self):
        c = Csvcode("demo", "Leo")
        self.assertEqual(c.getsailorid(-1, "ed smith", 107), 'gb-6335-edwsm', "Failed")
    def test5(self):
        c = Csvcode("demo", "Leo")
        self.assertEqual(c.getsailorid(-1, "ed smith"), 'gb-7636-ed0sm', "Failed")




if __name__ == '__main__':
    unittest.main()
