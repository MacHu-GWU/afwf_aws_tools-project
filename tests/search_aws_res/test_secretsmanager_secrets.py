# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_res.secretsmanager_secrets import secretmanager_secrets_searcher as sr


class TestSecretmanagerSecretsSearcher(object):
    def test_list_res(self):
        res = sr.list_res()
        # for key in res:
        #     print(key)

    def test_filter_res(self):
        res = sr.filter_res("example")
        # for key in res:
        #     print(key)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
