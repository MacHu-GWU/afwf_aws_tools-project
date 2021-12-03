# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.ec2_amis import ec2_amis_searcher as sr


class TestEc2AmiSearcher(object):
    def test_list_res(self):
        res = sr.list_res()
        for i in res:
            # print(i)
            pass

    def test_filter_res(self):
        res = sr.filter_res("dev")
        # print(res[0])
        item = sr.to_item(res[0])
        # print(item)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
