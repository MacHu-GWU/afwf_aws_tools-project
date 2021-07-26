# -*- coding: utf-8 -*-

import unittest
from aws_tools.helpers import (
    tokenize,
)


class Test(unittest.TestCase):
    def test_tokenize(self):
        self.assertListEqual(tokenize("a-b_c-d"), ["a", "b", "c", "d"])
        self.assertListEqual(tokenize("a-b-c-d"), ["a", "b", "c", "d"])
        self.assertListEqual(tokenize("a_b-c_d"), ["a", "b", "c", "d"])


if __name__ == '__main__':
    unittest.main()
