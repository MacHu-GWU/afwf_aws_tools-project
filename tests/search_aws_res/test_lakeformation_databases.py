# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.lakeformation_databases import lakeformation_databases_searcher as sr


class TestLakeformationDatabasesSearcher(object):
    def test_list_res(self):
        res = sr.list_res()
        # print(res[0])

    def test_filter_res(self):
        res = sr.filter_res("poc")
        # print(res[0])


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
