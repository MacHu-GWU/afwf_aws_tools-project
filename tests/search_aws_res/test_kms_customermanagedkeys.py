# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.kms_customermanagedkeys import kms_customermanagedkeys_searcher as sr


class TestKMSCustomerManagedKeysSearcher(object):
    def test_list_res(self):
        res = sr.list_res()
        # for key in res:
        #     print(key)

    def test_filter_res(self):
        res = sr.filter_res("test")
        # for key in res:
        #     print(key)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
