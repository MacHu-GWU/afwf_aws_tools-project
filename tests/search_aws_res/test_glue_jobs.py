# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.glue_jobs import glue_job_searcher as sr


class TestGlueJobSearcher(object):
    def test_list_res(self):
        res = sr.list_res()
        # print(res[0].name)

    def test_filter_res(self):
        res = sr.filter_res("json")
        # print(res[0].name)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
