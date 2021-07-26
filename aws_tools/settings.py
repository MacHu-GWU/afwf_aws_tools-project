# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pathlib_mate import Path
from sqlitedict import SqliteDict

HOME = Path.home()
ALFRED_DIR = Path(HOME, ".alfred-aws-tools")
if not ALFRED_DIR.exists():
    ALFRED_DIR.mkdir()

current_settings_db_file = Path(ALFRED_DIR, "settings.sqlite")

settings = SqliteDict(current_settings_db_file.abspath, autocommit=True)

class Keys:
    aws_profile = "aws_profile"
    aws_region = "aws_region"
    _debug = "_debug"
