# -*- coding: utf-8 -*-

import unittest
import ConfigParser
from pathlib_mate import Path
from aws_tools.credential import (
    read_all_section_name, read_all_aws_profile, replace_section
)


class Test(unittest.TestCase):
    def test_read_all_section_name(self):
        aws_credential_file = Path(__file__).change(new_basename="credentials").abspath
        section_name_list = read_all_section_name(aws_credential_file)
        self.assertTrue({"p1", "p2", "p3"}.issubset(set(section_name_list)))

    def test_set_default_profile(self):
        aws_credential_file = Path(__file__).change(new_basename="credentials").abspath

        # first replace
        replace_section(
            config_file=aws_credential_file,
            source_section_name="p1",
            target_section_name="default",
        )

        config = ConfigParser.ConfigParser()
        config.read(aws_credential_file)
        self.assertEqual(
            config.get("default", "aws_access_key_id"),
            config.get("p1", "aws_access_key_id"),
        )

        # second replace
        replace_section(
            config_file=aws_credential_file,
            source_section_name="p2",
            target_section_name="default",
        )

        config = ConfigParser.ConfigParser()
        config.read(aws_credential_file)
        self.assertEqual(
            config.get("default", "role_arn"),
            config.get("p2", "role_arn"),
        )

    def test_set_default_profile_for_config(self):
        aws_config_file = Path(__file__).change(new_basename="config").abspath

        # first replace
        replace_section(
            config_file=aws_config_file,
            source_section_name="profile p1",
            target_section_name="profile default",
        )

        config = ConfigParser.ConfigParser()
        config.read(aws_config_file)
        self.assertEqual(
            config.get("profile default", "region"),
            config.get("profile p1", "region"),
        )

        # second replace
        replace_section(
            config_file=aws_config_file,
            source_section_name="profile p2",
            target_section_name="profile default",
        )

        config = ConfigParser.ConfigParser()
        config.read(aws_config_file)
        self.assertEqual(
            config.get("profile default", "region"),
            config.get("profile p2", "region"),
        )


if __name__ == '__main__':
    unittest.main()
