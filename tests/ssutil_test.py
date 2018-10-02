import unittest
from ssutil import *


class TestStringMethods(unittest.TestCase):
    def test_clean(self):
        s1 = "Hi, Guys!"
        e1 = "hi guys"
        self.assertEqual(e1, clean(s1))

        s2 = "hi guys"
        e2 = "hi guys"
        self.assertEqual(e2, clean(s2))

        s3 = "What do you mean, Candy?!"
        e3 = "what do you mean candy"
        self.assertEqual(e3, clean(s3))

        s4 = "money9"
        e4 = "money"
        self.assertEqual(e4, clean(s4))


if __name__ == '__main__':
    unittest.main()
