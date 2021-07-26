# -*- coding: utf-8 -*-

import unittest
from workflow import Workflow3
from aws_tools.handlers.s3 import _list_bucket, create_boto_ses

boto_ses = create_boto_ses()

class Test(unittest.TestCase):
    def test_generate_password(self):
        _list_bucket(boto_ses)
        # for item in wf._items:
        #     assert len(item.arg) == 12
        #     assert item.title == item.arg



if __name__ == '__main__':
    unittest.main()
