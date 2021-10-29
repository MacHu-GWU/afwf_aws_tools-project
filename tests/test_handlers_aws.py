# -*- coding: utf-8 -*-

import unittest
from workflow import Workflow3
from aws_tools.handlers.aws import aws


class Test(unittest.TestCase):
    def test_generate_password(self):
        wf = Workflow3()
        aws(wf, args=[""])
        for item in wf._items:
            print(item)
        #     assert len(item.arg) == 12
        #     assert item.title == item.arg



if __name__ == '__main__':
    unittest.main()
