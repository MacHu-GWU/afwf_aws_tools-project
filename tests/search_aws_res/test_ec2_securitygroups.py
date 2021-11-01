# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.ec2_securitygroups import Ec2SecurityGroupsSearcher


class TestEc2SecurityGroupsSearcher(object):
    sr = Ec2SecurityGroupsSearcher()

    def test(self):
        res = self.sr.list_res()
        # res = self.sr.filter_res("dev")
        # res = self.sr.filter_res("0e18")
        self.sr.to_item(res[0])


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
