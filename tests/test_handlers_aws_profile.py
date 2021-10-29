# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from workflow import Workflow3
from aws_tools.handlers.aws_profile import (
    aws_profile_handlers,
)
from aws_tools.tests import setup_test_config_and_credential_file
from aws_tools.tests.paths import PATH_TEST_CONFIG_FILE, PATH_TEST_CREDENTIALS_FILE
from aws_tools.constants import FollowUpActionKey
from aws_tools.credential import load_config


class TestAWSProfileHandlers(object):
    def setup_method(self):
        setup_test_config_and_credential_file()
        aws_profile_handlers.aws_config_file = PATH_TEST_CONFIG_FILE
        aws_profile_handlers.aws_credentials_file = PATH_TEST_CREDENTIALS_FILE

    def test_set_default_aws_profile(self):
        wf = Workflow3()
        config = load_config(aws_profile_handlers.aws_config_file.abspath)
        assert config.get("default", "region") == "us-west-1"

        aws_profile_handlers.mh_set_default_aws_profile(wf, query_str="p1")
        config = load_config(aws_profile_handlers.aws_config_file.abspath)
        assert config.get("default", "region") == "us-east-1"

    def test_show_all_aws_profile(self):
        wf = Workflow3()
        aws_profile_handlers.sh_show_all_aws_profile(
            wf,
            item_builder=aws_profile_handlers.ib_select_aws_profile_for_default,
        )
        assert {"default", "p1", "p2", "p3"} == {item.title for item in wf._items}
        for item in wf._items:
            assert item.subtitle.startswith("set the default profile to: ")
            assert item.variables["action"] == FollowUpActionKey.run_script

    def test_show_filtered_aws_profile(self):
        wf = Workflow3()
        aws_profile_handlers.sh_show_filtered_aws_profile(wf, "d")

    def test_select_aws_profile(self):
        assert aws_profile_handlers.mh_select_aws_profile_to_set_as_default.__name__ == "select_aws_profile_to_set_as_default"
        wf = Workflow3()
        aws_profile_handlers.mh_select_aws_profile_to_set_as_default(wf=wf, query_str="")
        aws_profile_handlers.mh_select_aws_profile_to_set_as_default(wf=wf, query_str="2")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
