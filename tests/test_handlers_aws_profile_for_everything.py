# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from workflow import Workflow3
from aws_tools.handlers.aws_profile import (
    aws_profile_handlers,
)
from aws_tools.tests import setup_test_config_and_credential_file
from aws_tools.tests.paths import PATH_TEST_CONFIG_FILE, PATH_TEST_CREDENTIALS_FILE
from aws_tools.settings import settings, SettingKeys
from aws_tools.credential import load_config


class TestAWSProfileForEverythingHandlers(object):
    wf = Workflow3()

    def setup_method(self):
        self.wf = Workflow3()
        setup_test_config_and_credential_file()
        aws_profile_handlers.aws_config_file = PATH_TEST_CONFIG_FILE
        aws_profile_handlers.aws_credentials_file = PATH_TEST_CREDENTIALS_FILE

    def test_mh_select_aws_profile_to_set_as_default_for_everything(self):
        aws_profile_handlers.mh_select_aws_profile_to_set_as_default_for_everything(
            self.wf, query_str="")
        # for item in self.wf._items:
        #     print(item.title)
        #     print(item.subtitle)
        #     print(item.arg)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
