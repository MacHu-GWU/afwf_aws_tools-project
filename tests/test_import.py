# -*- coding: utf-8 -*-

import unittest

class TestImport(unittest.TestCase):
    def test(self):
        from aws_tools.handlers import handler


if __name__ == '__main__':
    unittest.main()
