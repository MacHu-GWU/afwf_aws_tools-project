# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.ec2_securitygroups import ec2_securitygroups_searcher as sr


class TestEc2SecurityGroupsSearcher(object):
    def test_list_res(self):
        res = sr.list_res()
        # print(res[0])
        item = sr.to_item(res[0])
        # print(item)

    def test_filter_res(self):
        res = sr.filter_res("dev")
        # print(res[0])

        res = sr.filter_res("dev sanhe")
        # print(res[0])


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
