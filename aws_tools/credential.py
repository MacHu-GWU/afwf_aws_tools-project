# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
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


def overwrite_section(config_file,
                      section_name,
                      data):
    """
    Overwrite a config section values (section_name) with the key, value pairs
     defined in data. For example,

    ``overwrite_section("config.ini", "default", [("k1", "v1"), ("k2", "v2"))``
    will do this:

    before::

        [sec1]
        k = 1

        [sec2]
        k = 2
        flag = 1

    after::

        [sec1]
        k = 1

        [sec2]
        k = 2
        flag = 1

        [default]
        k1 = v1
        k2 = v2
    """
    section_line = "[{}]".format(section_name)
    with open(config_file, "rb") as f:
        content = f.read().decode("utf-8")
        new_lines = list()
        append_flag = True
        is_in_section_flag = False
        found_section_flag = False
        for line in content.split("\n"):
            line = line.strip()
            # locate the target_section_name
            if line == section_line:
                # update the target_section_name section
                new_lines.append(line)
                for key, value in data:
                    new_lines.append("{} = {}".format(key, value))

                is_in_section_flag = True
                found_section_flag = True
                append_flag = False

            # encounter next section after the target_section_name
            if is_in_section_flag and (line.startswith("[") and line.endswith("]")) and (
                    line != section_line):
                new_lines.append("")  # add an empty line
                is_in_section_flag = False
                append_flag = True

            if append_flag:
                new_lines.append(line)

    # create a new target_section_name if it doesn't exist
    if not found_section_flag:
        new_lines.append(section_line)
        for key, value in data:
            new_lines.append("{} = {}".format(key, value))
        new_lines.append("")  # add an empty line

    with open(config_file, "wb") as f:
        f.write("\n".join(new_lines).encode("utf-8"))


def mfa_auth(aws_profile, mfa_code, hours=12):
    """

    :param aws_profile:
    :return:
    """
    import boto3

    boto_ses = boto3.session.Session(profile_name=aws_profile)
    sts = boto_ses.client("sts")

    response = sts.get_caller_identity()
    user_arn = response["Arn"]
    mfa_arn = user_arn.replace(":user/", ":mfa/", 1)

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.get_session_token
    response = sts.get_session_token(
        SerialNumber=mfa_arn,
        TokenCode=mfa_code,
        DurationSeconds=hours*3600,
    )
    aws_access_key_id = response["Credentials"]["AccessKeyId"]
    aws_secret_access_key = response["Credentials"]["SecretAccessKey"]
    aws_session_token = response["Credentials"]["SessionToken"]

    data = [
        ("aws_access_key_id", aws_access_key_id),
        ("aws_secret_access_key", aws_secret_access_key),
        ("aws_session_token", aws_session_token),
    ]

    new_aws_profile = "{}_mfa".format(aws_profile)
    overwrite_section(
        config_file=PATH_DEFAULT_AWS_CREDENTIAL_FILE.abspath,
        section_name=new_aws_profile,
        data=data,
    )

    config = ConfigParser.ConfigParser()
    config.read(PATH_DEFAULT_AWS_CONFIG_FILE.abspath)

    config_section_name = "profile {}".format(aws_profile)
    if config_section_name not in config.sections():
        raise SectionNotFoundError

    data = [
        (option_name, config.get(config_section_name, option_name))
        for option_name in config.options(config_section_name)
    ]

    overwrite_section(
        config_file=PATH_DEFAULT_AWS_CONFIG_FILE.abspath,
        section_name="profile {}_mfa".format(aws_profile),
        data=data,
    )