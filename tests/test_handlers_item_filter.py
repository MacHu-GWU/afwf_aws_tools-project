# -*- coding: utf-8 -*-

import pytest
from workflow.workflow3 import Workflow3
from aws_tools.handlers.item_filter import item_filters
from aws_tools.tests import setup_test_config_and_credential_file
from aws_tools.tests.paths import PATH_TEST_CONFIG_FILE, PATH_TEST_CREDENTIALS_FILE


class TestItemFilters(object):
    wf = Workflow3()

    def setup_method(self):
        self.wf = Workflow3()
        setup_test_config_and_credential_file()

    def test_aws_profile(self):
        items = item_filters.aws_profile(
            query_str="1",
            aws_config_file=PATH_TEST_CONFIG_FILE.abspath
        )
        assert items[0] == "p1"

    def test_aws_region(self):
        items = item_filters.aws_region(query_str="east")
        assert "east" in items[0][1]

        items = item_filters.aws_region(query_str="virg")
        assert items[0][1] == "us-east-1"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
