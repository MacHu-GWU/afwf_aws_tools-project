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


class TestAWSProfileHandlers(object):
    wf = Workflow3()

    def setup_method(self):
        self.wf = Workflow3()
        setup_test_config_and_credential_file()
        aws_profile_handlers.aws_config_file = PATH_TEST_CONFIG_FILE
        aws_profile_handlers.aws_credentials_file = PATH_TEST_CREDENTIALS_FILE

    def test_set_default_aws_profile(self):
        config = load_config(config_file=aws_profile_handlers.aws_config_file.abspath)
        assert config.get("default", "region") == "us-west-1"

        aws_profile_handlers.mh_set_default_aws_profile(self.wf, query_str="p1")
        config = load_config(config_file=aws_profile_handlers.aws_config_file.abspath)
        assert config.get("default", "region") == "us-east-1"

    def test_mh_set_aws_profile_as_aws_tools_default(self):
        aws_profile_handlers.mh_set_aws_profile_as_aws_tools_default(
            wf=self.wf, query_str="my_profile",
        )
        assert settings[SettingKeys.aws_profile] == "my_profile"

    def test_mh_select_aws_profile_for_mfa_auth(self):
        aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
            self.wf, query_str="")
        aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
            self.wf, query_str="invalid_profile")
        aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
            self.wf, query_str="valid_profile ")
        aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
            self.wf, query_str="valid_profile 123")
        aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
            self.wf, query_str="valid_profile 123456789")
        aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
            self.wf, query_str="valid_profile abcdef")
        aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
            self.wf, query_str="valid_profile 123456")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
