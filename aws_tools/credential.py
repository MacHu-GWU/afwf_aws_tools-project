# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import attr
import typing
from pathlib_mate import Path
import ConfigParser

HOME = Path.home()
PATH_DEFAULT_AWS_CREDENTIAL_FILE = Path(HOME, ".aws", "credentials")
PATH_DEFAULT_AWS_CONFIG_FILE = Path(HOME, ".aws", "config")


class SectionNotFoundError(ValueError): pass


def read_all_section_name(config_file):
    """
    :type config_file: absolute path of the config file
    :param config_file:
    :rtype: typing.List[str]
    :return:
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config.sections()


def read_all_profile_name_from_credential_file(aws_credential_file=PATH_DEFAULT_AWS_CREDENTIAL_FILE.abspath):
    return read_all_section_name(aws_credential_file)


def read_all_profile_name_from_config_file(aws_config_file=PATH_DEFAULT_AWS_CONFIG_FILE.abspath):
    return read_all_section_name(aws_config_file)


def read_all_aws_profile(aws_credential_file=PATH_DEFAULT_AWS_CREDENTIAL_FILE.abspath):
    """
    :type aws_credential_file: str
    :rtype: list[str]
    :return:
    """
    aws_credential = ConfigParser.ConfigParser()
    aws_credential.read(aws_credential_file)

    aws_profile_list = list()  # type: list[str]

    aws_credential_sections = aws_credential.sections()

    for cred_section_name in aws_credential_sections:
        aws_profile = cred_section_name
        aws_profile_list.append(aws_profile)

    return aws_profile_list


def replace_section(config_file,
                    source_section_name,
                    target_section_name):
    """
    Replace a config section values (target_section_name) with the value of
    another config section (source_section_name). For example,

    ``replace_section_and_return_content("config.ini", "default", "sec1")``
    will do this:

    before::

        [sec1]
        k = 1

        [sec2]
        k = 2
        flag = 1

    after::

        [default]
        k = 1

        [sec1]
        k = 1

        [sec2]
        k = 2
        flag = 1
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    if source_section_name not in config.sections():
        raise SectionNotFoundError

    target_section_line = "[{}]".format(target_section_name)
    with open(config_file, "rb") as f:
        content = f.read().decode("utf-8")
        new_lines = list()
        append_flag = True
        is_in_target_section_flag = False
        found_target_section_flag = False
        for line in content.split("\n"):
            line = line.strip()
            # locate the target_section_name
            if line == target_section_line:
                # update the target_section_name section
                new_lines.append(line)
                for option_name in config.options(source_section_name):
                    option_value = config.get(source_section_name, option_name)
                    new_lines.append("{} = {}".format(option_name, option_value))

                is_in_target_section_flag = True
                found_target_section_flag = True
                append_flag = False

            # encounter next section after the target_section_name
            if is_in_target_section_flag and (line.startswith("[") and line.endswith("]")) and (
                    line != target_section_line):
                new_lines.append("")  # add an empty line
                is_in_target_section_flag = False
                append_flag = True

            if append_flag:
                print(line)
                new_lines.append(line)

    # create a new target_section_name if it doesn't exist
    if not found_target_section_flag:
        new_lines.append(target_section_line)
        for option_name in config.options(source_section_name):
            option_value = config.get(source_section_name, option_name)
            new_lines.append("{} = {}".format(option_name, option_value))
        new_lines.append("")  # add an empty line

    with open(config_file, "wb") as f:
        f.write("\n".join(new_lines).encode("utf-8"))


# Go https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html#Concepts.RegionsAndAvailabilityZones.Regions
# Copy the data
# Go https://www.tablesgenerator.com/markdown_tables
# File -> Paste Table data, delete other columns, keep only first two columns
all_regions = [
    ("US East (Ohio)", "us-east-2"),
    ("US East (N. Virginia)", "us-east-1"),
    ("US West (N. California)", "us-west-1"),
    ("US West (Oregon)", "us-west-2"),
    ("Africa (Cape Town)", "af-south-1"),
    ("Asia Pacific (Hong Kong)", "ap-east-1"),
    ("Asia Pacific (Mumbai)", "ap-south-1"),
    ("Asia Pacific (Osaka)", "ap-northeast-3"),
    ("Asia Pacific (Seoul)", "ap-northeast-2"),
    ("Asia Pacific (Singapore)", "ap-southeast-1"),
    ("Asia Pacific (Sydney)", "ap-southeast-2"),
    ("Asia Pacific (Tokyo)", "ap-northeast-1"),
    ("Canada (Central)", "ca-central-1"),
    ("Europe (Frankfurt)", "eu-central-1"),
    ("Europe (Ireland)", "eu-west-1"),
    ("Europe (London)", "eu-west-2"),
    ("Europe (Milan)", "eu-south-1"),
    ("Europe (Paris)", "eu-west-3"),
    ("Europe (Stockholm)", "eu-north-1"),
    ("Middle East (Bahrain)", "me-south-1"),
    ("South America (São Paulo)", "sa-east-1"),
    ("AWS GovCloud (US-East)", "us-gov-east-1"),
    ("AWS GovCloud (US-West)", "us-gov-west-1"),
]
