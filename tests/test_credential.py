# -*- coding: utf-8 -*-

import unittest
from aws_tools.credential import (
    read_all_aws_profile,
)


class Test(unittest.TestCase):
    def test_read_all_aws_profile(self):
        read_all_aws_profile()


if __name__ == '__main__':
    unittest.main()
