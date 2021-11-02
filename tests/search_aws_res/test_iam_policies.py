# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.iam_policies import IamPolicysSearcher


class TestIamPolicysSearcher(object):
    sr = IamPolicysSearcher()

    def test_list_all_policies(self):
        res = self.sr.list_policys_dict()
        len(res)

    def test_list_res(self):
        res = self.sr.list_res()
        res = self.sr.filter_res("dev")
        # print(res)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])