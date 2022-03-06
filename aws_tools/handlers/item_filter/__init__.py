# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from typing import List, Tuple
from fuzzywuzzy.process import extract
from .aws_region import find_region, all_regions
from ...credential import (
    read_aws_profile_list_from_config_with_cache,
    read_aws_profile_and_region_list_from_config_with_cache,
)
from ...settings import setting_metadata_list

_ = setting_metadata_list


class ItemFilters(object):
    def __init__(self):
        self.kwargs = dict()

    def aws_profile(self, query_str, aws_config_file):
        """
        Given a list of ``aws_profile`` from ``aws_config_file`` (a file path),
        use ``query_str`` to filter by ``aws_profile`` and return
        filtered ``aws_profile`` list.

        :type query_str: str
        :type aws_config_file: str
        :rtype: List[str]
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
        Given a list of ``aws_region`` from hardcoded list,
        use ``query_str`` to filter by ``aws_region`` and return
        filtered ``aws_region`` list of tuple, include exact name and description name.

        :type query_str: str
        :rtype: List[Tuple[[str, str]]]
        """
        if query_str:
            aws_region_list = find_region(query_str)
        else:
            aws_region_list = all_regions
        return aws_region_list

    def aws_profile_and_region(self, query_str, aws_config_file):
        """
        Given a list of ``aws_profile`` and ``aws_region`` pair from
        ``aws_config_file`` (a file path), use ``query_str``
        to filter by ``aws_profile`` and return filtered pairs.

        :type query_str: str
        :type aws_config_file: str
        :rtype: List[Tuple[str, str]]
        """
        aws_profile_and_region_list_from_config = read_aws_profile_and_region_list_from_config_with_cache(
            aws_config_file=aws_config_file,
            expire=10,
        )
        aws_profile_list_from_config = [
            profile
            for profile, region in aws_profile_and_region_list_from_config
        ]
        aws_profile_to_region_mapper = {
            profile: region
            for profile, region in aws_profile_and_region_list_from_config
        }
        if query_str:
            filtered_aws_profile_list = [
                tp[0]
                for tp in extract(query_str.strip(), aws_profile_list_from_config, limit=20)
            ]
            filtered_aws_profile_and_region_list = [
                (aws_profile, aws_profile_to_region_mapper[aws_profile])
                for aws_profile in filtered_aws_profile_list
            ]
        else:
            filtered_aws_profile_and_region_list = aws_profile_list_from_config

        return filtered_aws_profile_and_region_list

    def aws_tool_settings(self, query_str):
        """
        :type query_str: str
        :rtype: list[tuple[[str, str]]]
        """


item_filters = ItemFilters()
