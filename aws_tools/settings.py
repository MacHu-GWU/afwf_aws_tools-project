# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import attr
from pathlib_mate import Path
from sqlitedict import SqliteDict
from .paths import DIR_AWS_TOOL_USER_DATA

PATH_SETTINGS_DB_FILE = Path(DIR_AWS_TOOL_USER_DATA, "settings.sqlite")

settings = SqliteDict(PATH_SETTINGS_DB_FILE.abspath, autocommit=True)


class SettingKeys:
    aws_profile = "aws_profile"
    aws_region = "aws_region"
    cache_expire = "expire"
    search_limit = "limit"


class SettingValues:
    """
    A current settings data snapshot. Allow other module to access those value
    easier.
    """
    aws_profile = settings.get(SettingKeys.aws_profile)
    aws_region = settings.get(SettingKeys.aws_region)
    cache_expire = settings.get(SettingKeys.cache_expire, 10)
    # number of search results returns
    search_limit = settings.get(SettingKeys.search_limit, 20)


@attr.s
class SettingMetadata(object):
    key = attr.ib()  # type: str
    converter = attr.ib(default=lambda x: x)  # type: callable
    short_description = attr.ib(default="")  # type: str
    long_description = attr.ib(default="")  # type: str


setting_metadata_list = [
    SettingMetadata(
        key=SettingKeys.aws_profile,
        converter=None,
        short_description=("The named aws profile for boto3 api call"),
        long_description="""
        """,
    ),
    SettingMetadata(
        key=SettingKeys.aws_region,
        converter=None,
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
]

setting_metadata_mapper = {
    setting_metadata.key: setting_metadata
    for setting_metadata in setting_metadata_list
}
