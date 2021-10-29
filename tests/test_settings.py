# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
from aws_tools.settings import settings, SettingKeys


class Test(unittest.TestCase):
    def test_read_all_aws_profile(self):
        settings[SettingKeys._debug] = "debug info"


if __name__ == '__main__':
    unittest.main()
