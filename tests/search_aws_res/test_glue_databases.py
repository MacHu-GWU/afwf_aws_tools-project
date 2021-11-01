# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.glue_databases import GlueDatabasesSearcher


class TestGlueDatabasesSearcher(object):
    sr = GlueDatabasesSearcher()

    def test_list_all_databases(self):
        res = self.sr.get_databases_dict()
        # print(res)

    def test_list_res(self):
        res = self.sr.list_res()
        res = self.sr.filter_res("poc")
        # print(res)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
