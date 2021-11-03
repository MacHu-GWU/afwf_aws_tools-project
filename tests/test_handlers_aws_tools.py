# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from workflow import Workflow3
from aws_tools.handlers.aws_tools import (
    aws_tools_handlers,
)
from aws_tools.settings import settings, SettingKeys
from aws_tools.credential import load_config


class TestAWSToolHandlers(object):
    wf = Workflow3()

    def setup_method(self):
        self.wf = Workflow3()

    def test_set_default_aws_profile(self):
        aws_tools_handlers.mh_info(self.wf, "")
        # config = load_config(config_file=aws_profile_handlers.aws_config_file.abspath)
        # assert config.get("default", "region") == "us-west-1"
        #
        # aws_profile_handlers.mh_set_default_aws_profile(self.wf, query_str="p1")
        # config = load_config(config_file=aws_profile_handlers.aws_config_file.abspath)
        # assert config.get("default", "region") == "us-east-1"

    # def test_mh_set_aws_profile_as_aws_tools_default(self):
    #     before_profile = settings.get(SettingKeys.aws_profile)
    #
    #     aws_profile_handlers.mh_set_aws_profile_as_aws_tools_default(
    #         wf=self.wf, query_str="my_profile",
    #     )
    #     assert settings[SettingKeys.aws_profile] == "my_profile"
    #     aws_profile_handlers.mh_set_aws_profile_as_aws_tools_default(
    #         wf=self.wf, query_str=None,
    #     )
    #     assert settings[SettingKeys.aws_profile] == None
    #
    #     settings[SettingKeys.aws_profile] = before_profile
    #
    # def test_mh_set_aws_region_as_aws_tools_default(self):
    #     before_region = settings.get(SettingKeys.aws_region)
    #
    #     aws_profile_handlers.mh_set_aws_region_as_aws_tools_default(
    #         wf=self.wf, query_str="my_region",
    #     )
    #     assert settings[SettingKeys.aws_region] == "my_region"
    #     aws_profile_handlers.mh_set_aws_region_as_aws_tools_default(
    #         wf=self.wf, query_str=None,
    #     )
    #     assert settings[SettingKeys.aws_region] == None
    #
    #     settings[SettingKeys.aws_region] = before_region
    #
    # def test_mh_select_aws_profile_for_mfa_auth(self):
    #     aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
    #         self.wf, query_str="")
    #     aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
    #         self.wf, query_str="invalid_profile")
    #     aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
    #         self.wf, query_str="valid_profile ")
    #     aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
    #         self.wf, query_str="valid_profile 123")
    #     aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
    #         self.wf, query_str="valid_profile 123456789")
    #     aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
    #         self.wf, query_str="valid_profile abcdef")
    #     aws_profile_handlers.mh_select_aws_profile_for_mfa_auth(
    #         self.wf, query_str="valid_profile 123456")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
