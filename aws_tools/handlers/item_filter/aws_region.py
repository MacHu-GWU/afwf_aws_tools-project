# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from fuzzywuzzy.process import extract
from ...constants import all_regions

all_region_dict_view = {
    "{} {}".format(long_name, short_name): (long_name, short_name)
    for long_name, short_name in all_regions
}
all_region_search_choice = list(all_region_dict_view)


def find_region(query_str, limit=10):
    """
    :type query_str: str
    :type limit: int
    :rtype: list[tuple[[str, str]]]
    """
    filtered_aws_region_list = [
        (all_region_dict_view[tp[0]][0], all_region_dict_view[tp[0]][1])
        for tp in extract(query_str.strip(), all_region_search_choice, limit=limit)
    ]
    return filtered_aws_region_list
