# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.cloud9_environments import cloud9_environments_searcher as sr


class TestCloud9EnvironmentsSearcher(object):
    def test_list_res(self):
        res = sr.list_res()
        print(res[0].name)

    def test_filter_res(self):
        res = sr.filter_res("dev")
        print(res[0].name)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
