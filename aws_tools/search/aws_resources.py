# -*- coding: utf-8 -*-

"""
This module provide a pattern to implement aws resources searcher
"""

import attr
from ..sdk import sdk, SDK
from ..alfred import ItemArgs
from ..cache import cache


@attr.s(hash=True)
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

    def to_console_url(self):
        """
        Convert this object to AWS Resource console url
        """
        raise NotImplementedError

    def to_large_text(self):
        """
        Convert this object to large text for Alfred preview
        """
        raise NotImplementedError

    def __hash__(self):
        return hash(self.id)


class AwsResourceSearcher(object):
    """
    Aws Resource searcher base class.
    """
    id = None  # type: str
    sdk = sdk  # type: SDK

    @property
    def resource_id(self):
        return self.id

    def simplify_response(self, res):
        """
        Extract many :class`ResData` objects from boto3 API call response.

        :type res: dict
        :rtype: list[ResData]
        """
        raise NotImplementedError

    @cache.memoize(expire=10)
    def list_res(self):
        """
        :rtype: list
        """
        raise NotImplementedError

    @cache.memoize(expire=10)
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
