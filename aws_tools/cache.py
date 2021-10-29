# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pathlib_mate import Path
from .paths import DIR_AWS_TOOL_USER_DATA
from diskcache import Cache

PATH_CACHE_DIR = Path(DIR_AWS_TOOL_USER_DATA, ".cache")

cache = Cache(PATH_CACHE_DIR.abspath)
