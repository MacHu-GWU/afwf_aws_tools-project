# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_functions
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Function(ResData):
    name = attr.ib()
    description = attr.ib()
    arn = attr.ib()
    last_modified = attr.ib()
    memory_size = attr.ib()
    timeout = attr.ib()
    runtime = attr.ib()
    code_size = attr.ib()
    role = attr.ib()

    @property
    def id(self):
        return self.name

    def to_console_url(self):
        return "https://console.aws.amazon.com/lambda/home?region={region}#/functions/{function_name}?tab=code".format(
            function_name=self.name,
            region=SettingValues.aws_region,
        )


class LambdaFunctionsSearcher(AwsResourceSearcher):
    id = "lambda-functions"
    limit_arg_name = "MaxItems"
    paginator_arg_name = "Marker"

    def boto3_call(self, **kwargs):
        return self.sdk.lambda_client.list_functions(**kwargs)

    def get_paginator(self, res):
        return res.get("NextMarker")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of lambda_client.list_functions

        :rtype: list[Function]
        """
        func_list = list()
        for func_dict in res["Functions"]:
            func = Function(
                name=func_dict["FunctionName"],
                description=func_dict.get("Description"),
                arn=func_dict["FunctionArn"],
                last_modified=func_dict["LastModified"],
                memory_size=func_dict["MemorySize"],
                timeout=func_dict["Timeout"],
                runtime=func_dict.get("Runtime"),
                code_size=func_dict["CodeSize"],
                role=func_dict["Role"],
            )
            func_list.append(func)
        return func_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Function]
        """
        func_list = self.recur_list_res(limit=limit)
        func_list = list(sorted(
            func_list, key=lambda r: r.last_modified, reverse=True))
        return func_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Function]
        """
        func_list = self.list_res(limit=1000)
        keys = [func.name for func in func_list]
        mapper = {func.name: func for func in func_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_func_list = fz_sr.match(query_str, limit=20)
        return matched_func_list

    def to_item(self, func):
        """
        :type func: Function
        :rtype: ItemArgs
        """
        console_url = func.to_console_url()
        item_arg = ItemArgs(
            title="{func_name}".format(
                func_name=func.name,
            ),
            subtitle="{description}".format(
                description=func.description
            ),
            autocomplete="{} {}".format(self.resource_id, func.name),
            arg=console_url,
            largetext=func.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(func.arn)
        item_arg.copy_id(func.id)
        return item_arg


lambda_functions_searcher = LambdaFunctionsSearcher()
