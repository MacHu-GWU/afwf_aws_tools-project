# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import attr
from pathlib_mate import Path
from sqlitedict import SqliteDict
from collections import OrderedDict
from fuzzywuzzy.process import extract
from .paths import DIR_AWS_TOOL_USER_DATA

PATH_SETTINGS_DB_FILE = Path(DIR_AWS_TOOL_USER_DATA, "settings.sqlite")

settings = SqliteDict(PATH_SETTINGS_DB_FILE.abspath, autocommit=True)


class SettingKeys:
    aws_profile = None
    aws_region = None
    cache_expire = None
    search_limit = None
    _debug = None


setting_key_list = list()
for k in SettingKeys.__dict__.keys():
    if not k.startswith("_"):
        setattr(SettingKeys, k, k)
        setting_key_list.append(k)


class SettingValues:
    """
    A current settings data snapshot. Allow other module to access those value
    easier.

    aws_profile: provide AWS credential
    aws_region: the console you opened is in this region
    """
    aws_profile = settings.get(SettingKeys.aws_profile)
    aws_region = settings.get(SettingKeys.aws_region)
    cache_expire = settings.get(SettingKeys.cache_expire, 10)
    # number of search results returns
    search_limit = settings.get(SettingKeys.search_limit, 20)

    @classmethod
    def get_console_domain(cls):
        if cls.aws_region in {"us-gov-east-1", "us-gov-west-1"}:
            return "console.amazonaws-us-gov.com"
        else:
            return "console.aws.amazon.com"

@attr.s
class SettingMetadata(object):
    key = attr.ib()  # type: str
    converter = attr.ib(default=lambda x: x)  # type: callable
    short_description = attr.ib(default="")  # type: str
    long_description = attr.ib(default="")  # type: str


setting_metadata_list = [
    SettingMetadata(
        key=SettingKeys.aws_profile,
        converter=str,
        short_description=("The named aws profile for boto3 api call"),
        long_description="""
        """,
    ),
    SettingMetadata(
        key=SettingKeys.aws_region,
        converter=str,
        short_description=("The aws region"),
        long_description="""
        """,
    ),
    SettingMetadata(
        key=SettingKeys.cache_expire,
        converter=int,
        short_description=("How long you want search results to cache. Suggest 10 sec"),
        long_description="""
        """,
    ),
    SettingMetadata(
        key=SettingKeys.search_limit,
        converter=int,
        short_description=("How many search results to return. Suggest 20"),
        long_description="""
        """,
    ),
]  # type: list[SettingMetadata]

setting_metadata_mapper = OrderedDict([
    (setting_metadata.key, setting_metadata)
    for setting_metadata in setting_metadata_list
])  # type: dict[str, SettingMetadata]


def find_setting(query_str, limit=10):
    """
    :type query_str: str
    :type limit: int
    :rtype: list[str, str]
    """
    filtered_setting_list = [
        tp[0]
        for tp in extract(query_str.strip(), setting_key_list, limit=limit)
    ]
    return filtered_setting_list
