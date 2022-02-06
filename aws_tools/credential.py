# -*- coding: utf-8 -*-

"""
This module implements the simple read / write / update for ``~/aws/credentials``
and ``~/aws/config`` files.

They are both in ``named config file`` format::

    [section_name]
    key1 = value1
    key2 = value2
    ...

Reference: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html

FAQ:

- Q: Why use line level editing instead of loading config file to python dict,
    process it, then dump?
- A: because with load and dump, you lose all comments.

**Chinese Doc**

config 和 credentials 文件的不同之处:

1. config 不保存敏感信息. 主要保存 region, output.
2. credentials 保存敏感信息. 主要保存 Access Key 和 Secret Key. 又或是临时的 session token.
3. 两者的 default profile 都是 [default] 但是其他 named profile
    在 config 中是 [profile profile_name], 而 credentials 中则是 [profile_name]

对于 assumed role 的情况要特别注意:

1. 已有一个 profile ``a``, 同时创建了 named profile ``b`` 用于测试 assumed role,
    在 cli 中我们用 --profile b 来显式指定. 此时只需要在 config 文件中创建这个
    named profile, 而无需在 credentials 中创建. 因为 config 会定义 source_profile,
    只要 credentials 文件中有这个 source_profile 即可.
    并且 profile ``b`` 中的 region 可以和 ``a`` 中的不同.
2. 已有一个 profile ``a``, 同时用 ``default`` profile 来测试 assumed role,
    在 cli 中我们不用 --profile, 直接使用 default. 此时需要在 config 和 credentials
    中同时创建 [default] 这个 named profile. config 中的 region 如果和 ``a`` 中的不同,
    会没有效果. 而 credential 中也必须创建 [default] 其中的
    credential 和 ``a`` 中的一样, 不然会找不到 credential.

结论: 避免在 default 中使用 assumed role!

对于 mfa temp profile 的情况也要特别注意:

该情况等于是创建了个临时的新的 profile, 新的 profile 的 credential 是通过用原始的
    profile 执行 sts 命令获得的. 所以需要在 config 和 credentials 中都创建
    named profile, 而 credentials 中多了 ``aws_session_token = ...`` 一行.
    当然 config 中的 region 可以和原来的不一样.

结论: 避免在 default 中使用 mfa temp profile
"""

from __future__ import unicode_literals, print_function
import typing
import ConfigParser
from .paths import (
    PATH_DEFAULT_AWS_CONFIG_FILE,
    PATH_DEFAULT_AWS_CREDENTIALS_FILE,
)
from .cache import cache, CacheKeys


class SectionNotFoundError(ValueError):
    """
    Raise when failed to access a section in a named config file.
    """
    pass


def load_config(config_file):
    """
    Use ConfigParser standard lib to load a config file.

    :rtype: ConfigParser.ConfigParser
    """

    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config


def read_all_section_name(config_file):
    """
    Return the list of all section name in a named config file.

    :type config_file: str
    :param config_file: absolute path of the config file

    :rtype: typing.List[str]
    :return:
    """
    config = load_config(config_file)
    return config.sections()


def replace_section(
    config_file,
    source_section_name,
    target_section_name,
):
    """
    Replace a config section values (target_section_name) with the value of
    another config section (source_section_name). For example::

        replace_section_and_return_content(
            "config.ini",
            "default",
            "sec1"
        )

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
        raise SectionNotFoundError(source_section_name)

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


def overwrite_section(
    config_file,
    section_name,
    data,
):
    """
    Overwrite a config section values (section_name) with the key, value pairs
     defined in data. If the section_name doesn't exists before, create it.
     For example::

        overwrite_section(
            "config.ini",
            "default",
            [("k1", "v1"), ("k2", "v2")
        )

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


def read_aws_profile_list_from_config(
    aws_config_file=PATH_DEFAULT_AWS_CONFIG_FILE.abspath,
):
    """
    :type aws_config_file: str
    """
    aws_profile_list_from_config = read_all_section_name(aws_config_file)
    aws_profile_list_from_config = [
        aws_profile[8:] if aws_profile.startswith("profile ") else aws_profile
        for aws_profile in aws_profile_list_from_config
    ]
    return aws_profile_list_from_config


def read_aws_profile_list_from_config_with_cache(
    aws_config_file=PATH_DEFAULT_AWS_CONFIG_FILE.abspath,
    expire=1,
):
    """
    :type aws_config_file: str
    :type expire: int
    """
    return cache.fast_get(
        key=CacheKeys.aws_profile_list_from_config,
        callable=read_aws_profile_list_from_config,
        kwargs=dict(
            aws_config_file=aws_config_file,
        ),
        expire=expire,
    )


def set_named_profile_as_default(
    aws_profile,
    aws_config_file=PATH_DEFAULT_AWS_CONFIG_FILE.abspath,
    aws_credentials_file=PATH_DEFAULT_AWS_CREDENTIALS_FILE.abspath,
):  # pragma: no cover
    if aws_profile == "default":
        return
    replace_section(
        config_file=aws_config_file,
        source_section_name="profile {}".format(aws_profile),
        target_section_name="default",
    )
    replace_section(
        config_file=aws_credentials_file,
        source_section_name=aws_profile,
        target_section_name="default",
    )


def mfa_auth(
    aws_profile,
    mfa_code,
    hours=12,
    aws_config_file=PATH_DEFAULT_AWS_CONFIG_FILE.abspath,
    aws_credentials_file=PATH_DEFAULT_AWS_CREDENTIALS_FILE.abspath,
):  # pragma: no cover
    """
    Given a root ``aws_profile``, do MFA authentication with ``mfa_code``,
    create / update the new aws profile ``${aws_profile}_mfa`` using the returned
    temp token. This function will update the ``~/.aws/credential`` and
    ``~/.aws/config`` file inplace.

    :param aws_profile: The source AWS profile which has MFA enabled
    :param mfa_code: six digit MFA code
    :param hours: time-to-expire hours.
    """
    # step1, get access key, secret key, session token
    if aws_profile == "default":
        raise ValueError

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
        DurationSeconds=hours * 3600,
    )
    aws_access_key_id = response["Credentials"]["AccessKeyId"]
    aws_secret_access_key = response["Credentials"]["SecretAccessKey"]
    aws_session_token = response["Credentials"]["SessionToken"]

    # update ~/.aws/credentials file
    new_aws_profile = "{}_mfa".format(aws_profile)
    data = [
        ("aws_access_key_id", aws_access_key_id),
        ("aws_secret_access_key", aws_secret_access_key),
        ("aws_session_token", aws_session_token),
    ]
    overwrite_section(
        config_file=aws_credentials_file,
        section_name=new_aws_profile,
        data=data,
    )

    # update ~/.aws/config file
    replace_section(
        config_file=aws_config_file,
        source_section_name="profile {}".format(aws_profile),
        target_section_name="profile {}_mfa".format(aws_profile),
    )
