# -*- coding: utf-8 -*-

"""
This module provide a pattern to implement aws resources searcher
"""

import attr
from ..sdk import sdk, SDK
from ..alfred import ItemArgs, ModArgs


@attr.s
class ResData(object):
    """
    Resource data class, A data container class stores the
    simplified version of boto3 response. It makes the aws resource searcher
    implementation code easier to debug and more maintainable.

    For example, the IAM Role list_roles method API response is like this
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_roles

    The simplified resource data class can be::

        @attr.s
        class Role(ResData):
            id = attr.ib()
            name = attr.ib()
            description = attr.ib()
            path = attr.ib()
            arn = attr.ib()
            create_data = attr.ib()
    """
    @property
    def to_console_url(self):
        raise NotImplementedError


class AwsResourceSearcher(object):
    """
    Aws Resource searcher base class.
    """
    id = None  # type: str
    sdk = sdk  # type: SDK

    @property
    def resource_id(self):
        return self.id

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
