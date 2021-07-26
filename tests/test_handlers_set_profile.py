# -*- coding: utf-8 -*-

import unittest
from workflow import Workflow3
from aws_tools.handlers.set_profile import set_profile


class Test(unittest.TestCase):
    def test_generate_password(self):
        wf = Workflow3()
        set_profile(wf, args=[])
        # for item in wf._items:
        #     assert len(item.arg) == 12
        #     assert item.title == item.arg



if __name__ == '__main__':
    unittest.main()
