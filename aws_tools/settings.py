# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pathlib_mate import Path
from sqlitedict import SqliteDict
from .paths import DIR_AWS_TOOL_USER_DATA

PATH_SETTINGS_DB_FILE = Path(DIR_AWS_TOOL_USER_DATA, "settings.sqlite")

settings = SqliteDict(PATH_SETTINGS_DB_FILE.abspath, autocommit=True)


class SettingKeys:
    aws_profile = "aws_profile"
    aws_region = "aws_region"
    expire = "expire"
    limit = "limit"
    _debug = "_debug"


class SettingValues:
    aws_profile = settings.get(SettingKeys.aws_profile)
    aws_region = settings.get(SettingKeys.aws_region)
    # cache expire time
    expire = settings.get(SettingKeys.expire, 10)
    # number of search results returns
    limit = settings.get(SettingKeys.expire, 20)
