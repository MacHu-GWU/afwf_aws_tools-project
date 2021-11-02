# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.lakeformation_tables import lakeformation_tables_searcher as sr


class TestLakeformationTablesSearcher(object):
    def test_list_res(self):
        res = sr.list_res()
        # print(res)

    def test_filter_res(self):
        res = sr.filter_res("poc")
        # print(res)

        res = sr.filter_res("glue_etl_job_poc.")
        # for tb in res:
        #     print(tb.full_name)

        res = sr.filter_res("glue_etl_job_poc.all_column")
        # for tb in res:
        #     print(tb.full_name)

        res = sr.filter_res("glue_etl_job_poc.column all")
        # for tb in res:
        #     print(tb.full_name)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
