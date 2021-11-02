# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pathlib_mate import Path
from .paths import DIR_AWS_TOOL_USER_DATA
from diskcache import Cache

PATH_CACHE_DIR = Path(DIR_AWS_TOOL_USER_DATA, ".cache")


class CustomCache(Cache):
    def fast_get(self, key, callable, kwargs=None, expire=None):
        value = self.get(key)
        if value is None:
            if kwargs is None:
                kwargs = {}
            value = callable(**kwargs)
            self.set(key, value, expire=expire)
        return value



cache = CustomCache(PATH_CACHE_DIR.abspath)


class CacheKeys:
    aws_profile_list_from_config = None


for k in CacheKeys.__dict__.keys():
    if not k.startswith("_"):
        setattr(CacheKeys, k, k)
