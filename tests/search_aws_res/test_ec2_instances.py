# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.ec2_instances import Ec2InstancesSearcher


class TestEc2InstancesSearcher(object):
    sr = Ec2InstancesSearcher()

    def test_list_res(self):
        res = self.sr.list_res()
        # print(res[0])

    def test_filter_res(self):
        res = self.sr.filter_res("dev")
        # print(res[0])
        res = self.sr.filter_res("0e18")
        # print(res[0])
        res = self.sr.filter_res("dev sanhe")
        # for inst in res:
        #     print(inst.name)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
