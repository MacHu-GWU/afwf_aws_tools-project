# -*- coding: utf-8 -*-

import pytest
import ConfigParser
from aws_tools.credential import (
    read_all_section_name, replace_section, overwrite_section,
    read_aws_profile_list_from_config,
    read_aws_profile_list_from_config_with_cache,
    read_aws_profile_and_region_list_from_config,
    read_aws_profile_and_region_list_from_config_with_cache,
    set_named_profile_as_default, mfa_auth,
)
from aws_tools.tests import setup_test_config_and_credential_file
from aws_tools.tests.paths import (
    PATH_TEST_CONFIG_FILE,
    PATH_TEST_CREDENTIALS_FILE,
)


class Test:
    def setup_method(self, method):
        setup_test_config_and_credential_file()

    def test_read_all_section_name(self):
        section_name_list = read_all_section_name(PATH_TEST_CONFIG_FILE.abspath)
        assert {"default", "profile p1", "profile p2", "profile p3"} \
            .issubset(set(section_name_list))

    def test_replace_section(self):
        # replace an existing section
        replace_section(
            config_file=PATH_TEST_CONFIG_FILE.abspath,
            source_section_name="profile p1",
            target_section_name="default",
        )
        config = ConfigParser.ConfigParser()
        config.read(PATH_TEST_CONFIG_FILE.abspath)
        assert config.get("default", "region") \
               == config.get("profile p1", "region")

        # create a new section if target_section_name not exists
        replace_section(
            config_file=PATH_TEST_CONFIG_FILE.abspath,
            source_section_name="profile p2",
            target_section_name="profile p2_copy",
        )
        config = ConfigParser.ConfigParser()
        config.read(PATH_TEST_CONFIG_FILE.abspath)
        assert config.get("profile p2", "role_arn") \
               == config.get("profile p2_copy", "role_arn")

    def test_overwrite_section(self):
        # create a new section if section_name not exists
        overwrite_section(
            config_file=PATH_TEST_CREDENTIALS_FILE.abspath,
            section_name="p2",
            data=[("aws_access_key_id", "BBB"), ("aws_secret_access_key", "BBB")]
        )
        config = ConfigParser.ConfigParser()
        config.read(PATH_TEST_CREDENTIALS_FILE.abspath)
        assert config.get("p2", "aws_access_key_id") == "BBB"

        # overwrite an existing section
        overwrite_section(
            config_file=PATH_TEST_CREDENTIALS_FILE.abspath,
            section_name="p3",
            data=[("aws_access_key_id", "CCCCCC"), ("aws_secret_access_key", "CCCCCC")]
        )
        config = ConfigParser.ConfigParser()
        config.read(PATH_TEST_CREDENTIALS_FILE.abspath)
        assert config.get("p3", "aws_access_key_id") == "CCCCCC"
        assert config.has_option("p3", "aws_session_token") is False

    def test_read_aws_profile_list_from_config(self):
        profile_list = read_aws_profile_list_from_config(
            aws_config_file=PATH_TEST_CONFIG_FILE.abspath
        )
        assert profile_list == ["default", "p1", "p2", "p3"]

    def test_read_aws_profile_and_region_list_from_config(self):
        profile_and_region_list = read_aws_profile_and_region_list_from_config(
            aws_config_file=PATH_TEST_CONFIG_FILE.abspath
        )
        assert profile_and_region_list == [
            ("default", "us-west-1"),
            ("p1", "us-east-1"),
            ("p2", "us-east-2"),
            ("p3", "us-east-3"),
        ]

    def test_read_aws_profile_list_from_config_with_cache(self):
        profile_list = read_aws_profile_list_from_config_with_cache(
            aws_config_file=PATH_TEST_CONFIG_FILE.abspath
        )
        assert profile_list == ["default", "p1", "p2", "p3"]

    def test_read_aws_profile_and_region_list_from_config_with_cache(self):
        profile_and_region_list = read_aws_profile_and_region_list_from_config_with_cache(
            aws_config_file=PATH_TEST_CONFIG_FILE.abspath
        )
        assert profile_and_region_list == [
            ("default", "us-west-1"),
            ("p1", "us-east-1"),
            ("p2", "us-east-2"),
            ("p3", "us-east-3"),
        ]


    # def test_set_named_profile_as_default(self):
    #     set_named_profile_as_default("aws_data_lab_sanhe")

    # def test_mfa_auth(self):
    #     mfa_auth(aws_profile="aws_data_lab_sanhe", mfa_code="224833", hours=24)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
