# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.vpc_vpcs import vpc_vpcs_searcher as sr


class TestVpcVpcsSearcher(object):
    def test_list_res(self):
        res = sr.list_res()
        # print(res[0])

    def test_filter_res(self):
        res = sr.filter_res("dev")
        # print(res[0])
        res = sr.filter_res("0fe6")
        # print(res[0])
        res = sr.filter_res("dev sanhe")
        # for inst in res:
        #     print(inst.name)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
