# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.ec2_amis import Ec2AmiSearcher


class TestEc2AmiSearcher(object):
    sr = Ec2AmiSearcher()

    def test(self):
        res = self.sr.list_res()
        for i in res:
            # print(i)
            pass
        if len(res):
            item = self.sr.to_item(res[0])
        res = self.sr.filter_res("dev")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
