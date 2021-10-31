# -*- coding: utf-8 -*-

"""
This module provide a pattern to implement aws resources searcher
"""

from ..sdk import sdk, SDK
from ..alfred import ItemArgs


class AwsResourceSearcher(object):
    """
    Aws Resource searcher base class.
    """
    id = None  # type: str
    sdk = sdk  # type: SDK

    def list_res(self):
        """
        :rtype: list
        """
        raise NotImplementedError

    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list
        """
        raise NotImplementedError

    def to_item(self, data):
        """
        :type data: dict
        :rtype: ItemArgs
        """
        raise NotImplementedError
