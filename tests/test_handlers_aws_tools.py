# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from workflow import Workflow3
from aws_tools.handlers.aws_tools import (
    aws_tools_handlers,
)
from aws_tools.settings import settings, SettingKeys, setting_key_list
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

    def test_set(self):
        before_value = settings.get(SettingKeys.aws_profile)
        st_value = "an_impossible_aws_profile_value"
        aws_tools_handlers.mh_set_value(
            self.wf,
            query_str="{} {}".format(
                SettingKeys.aws_profile,
                st_value,
            )
        )
        assert settings[SettingKeys.aws_profile] == st_value
        settings[SettingKeys.aws_profile] = before_value
        assert settings[SettingKeys.aws_profile] == before_value

    def test_set_case1(self):
        aws_tools_handlers.mh_set(self.wf, query_str="")
        assert len(self.wf._items) == len(setting_key_list)

    def test_set_case2(self):
        aws_tools_handlers.mh_set(self.wf, query_str=" ")
        assert len(self.wf._items) == len(setting_key_list)

    def test_set_case3(self):
        aws_tools_handlers.mh_set(self.wf, query_str="aws")
        for item in self.wf._items[:2]:
            assert "aws" in item.title

    def test_set_case4(self):
        # still list all available setting keys
        aws_tools_handlers.mh_set(self.wf, query_str="aws_profile")
        assert "aws_profile" in self.wf._items[0].title
        assert len(self.wf._items) == len(setting_key_list)

    def test_set_case5(self):
        # proceed with set value
        aws_tools_handlers.mh_set(self.wf, query_str="aws_profile ")
        assert len(self.wf._items) == 1
        assert "aws_profile" in self.wf._items[0].title

    def test_set_case6(self):
        # proceed with set value
        aws_tools_handlers.mh_set(self.wf, query_str="invalid_setting_key ")
        assert len(self.wf._items) == 1
        assert "not a valid" in self.wf._items[0].title

    def test_set_case7(self):
        st_value = "an_impossible_aws_profile_value"
        aws_tools_handlers.mh_set(
            self.wf,
            query_str="{} {}".format(
                SettingKeys.aws_profile,
                st_value,
            )
        )
        item = self.wf._items[0]
        assert item.arg.endswith(st_value + "'")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
