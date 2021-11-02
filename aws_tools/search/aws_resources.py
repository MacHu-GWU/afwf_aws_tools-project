# -*- coding: utf-8 -*-

"""
This module provide a pattern to implement aws resources searcher
"""

import attr
import typing
from collections import OrderedDict
from ..sdk import sdk, SDK
from ..alfred import Base, ItemArgs
from ..cache import cache


@attr.s(hash=True)
class ResData(Base):
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
        return "\n".join([
            "{} = {}".format(k, v)
            for k, v in attr.asdict(self, dict_factory=OrderedDict).items()
        ])

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

    limit_arg_name = None  # type: str
    paginator_arg_name = None  # type: str
    lister = None  # type: callable

    def get_paginator(self, res):
        """
        :type res: dict
        :rtype: str
        """
        raise NotImplementedError

    @cache.memoize(expire=10)
    def recur_list_res(self,
                       kwargs=None,
                       page_size=1000,
                       limit=0):
        """
        Some list_resource API requires paginator to retrieve many items.

        :type kwargs: dict
        :type limit: int

        :rtype: list[ResData]
        """
        max_results = page_size if limit > page_size else limit
        paginator = None
        res_list = list()
        while 1:
            if kwargs is None:
                kwargs = dict()
            if self.limit_arg_name:
                kwargs[self.limit_arg_name] = max_results
            if paginator:
                kwargs[self.paginator_arg_name] = paginator

            response = self.lister(**kwargs)
            res_list.extend(self.simplify_response(response))
            paginator = self.get_paginator(response)

            n_res = len(res_list)
            if n_res >= limit:  # already got enough items
                break
            else:
                max_results = (limit - n_res) if (limit - n_res) < page_size else page_size

            if not paginator:  # no more items
                break
        return res_list

    @cache.memoize(expire=10)
    def list_res(self):
        """
        :rtype: list[ResData]
        """
        raise NotImplementedError

    @cache.memoize(expire=10)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[ResData]
        """
        raise NotImplementedError

    def to_item(self, data):
        """
        :type data: dict
        :rtype: ItemArgs
        """
        raise NotImplementedError
