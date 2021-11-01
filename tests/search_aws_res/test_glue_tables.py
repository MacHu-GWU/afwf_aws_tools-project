# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.glue_tables import GlueTablesSearcher


class TestGlueTablesSearcher(object):
    sr = GlueTablesSearcher()

    def test_get_table_dict(self):
        res = self.sr.get_tables_dict("default", "dev")
        # print(res)

    def test_list_res(self):
        res = self.sr.list_res()
        # print(res)

    def test_filter_res(self):
        # res = self.sr.filter_res("poc")
        # print(res)

        res = self.sr.filter_res("glue_etl_job_poc.")
        # print(res)

        res = self.sr.filter_res("glue_etl_job_poc.all_column")
        # print(res)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
