# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from fuzzywuzzy.process import extract
from ...credential import read_aws_profile_list_from_config_with_cache
from .aws_region import find_region, all_regions


class ItemFilters(object):
    def __init__(self):
        self.kwargs = dict()

    def aws_profile(self, query_str, aws_config_file):
        """
        :type query_str: str
        :type aws_config_file: str
        :rtype: list[str]
        """
        aws_profile_list_from_config = read_aws_profile_list_from_config_with_cache(
            aws_config_file=aws_config_file,
            expire=10,
        )
        if query_str:
            filtered_aws_profile_list = [
                tp[0]
                for tp in extract(query_str.strip(), aws_profile_list_from_config, limit=20)
            ]
            aws_profile_list = filtered_aws_profile_list
        else:
            aws_profile_list = aws_profile_list_from_config
        return aws_profile_list

    def aws_region(self, query_str):
        """
        :type query_str: str
        :rtype: list[tuple[[str, str]]]
        """
        if query_str:
            aws_region_list = find_region(query_str)
        else:
            aws_region_list = all_regions
        return aws_region_list


item_filters = ItemFilters()
