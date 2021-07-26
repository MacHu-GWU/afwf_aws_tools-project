# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
from aws_tools.handlers.s3 import _list_bucket, create_boto_ses

boto_ses = create_boto_ses()


class Test(unittest.TestCase):
    def test_list_bucket(self):
        result = _list_bucket(boto_ses)
        bucket_list = [tp[0] for tp in result]
        self.assertIn("aws-data-lab-sanhe-for-everything", bucket_list)


if __name__ == '__main__':
    unittest.main()
