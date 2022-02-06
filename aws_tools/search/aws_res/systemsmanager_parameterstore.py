# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_parameters
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Parameter(ResData):
    name = attr.ib()
    description = attr.ib()
    type = attr.ib()
    version = attr.ib()
    last_modified_date = attr.ib()
    last_modified_user = attr.ib()
    tier = attr.ib()

    @property
    def id(self):
        return self.name

    def to_console_url(self):
        return "https://{domain}/systems-manager/parameters/{param_name}/description?region={region}&tab=Table".format(
            domain=SettingValues.get_console_domain(),
            param_name=self.name,
            region=SettingValues.aws_region,
        )


class SystemManagerParameterStoreSearcher(AwsResourceSearcher):
    id = "systemsmanager-parameterstore"
    limit_arg_name = "MaxResults"
    paginator_arg_name = "NextToken"

    def boto3_call(self, **kwargs):
        return self.sdk.ssm_client.describe_parameters(**kwargs)

    def get_paginator(self, res):
        return res.get("NextToken")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of ssm_client.describe_parameters

        :rtype: list[Parameter]
        """
        param_list = list()
        for param_dict in res.get("Parameters", []):
            param = Parameter(
                name=param_dict["Name"],
                description=param_dict.get("Description"),
                type=param_dict["Type"],
                version=param_dict.get("Version"),
                last_modified_date=param_dict.get("LastModifiedDate"),
                last_modified_user=param_dict.get("LastModifiedUser"),
                tier=param_dict.get("Tier"),
            )
            param_list.append(param)
        return param_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Parameter]
        """
        func_list = self.recur_list_res(page_size=50, limit=limit)
        func_list = list(sorted(
            func_list, key=lambda r: r.last_modified_date, reverse=True))
        return func_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Parameter]
        """
        func_list = self.list_res(limit=1000)
        keys = [func.name for func in func_list]
        mapper = {func.name: func for func in func_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_func_list = fz_sr.match(query_str, limit=20)
        return matched_func_list

    def to_item(self, param):
        """
        :type func: Parameter
        :rtype: ItemArgs
        """
        console_url = param.to_console_url()
        item_arg = ItemArgs(
            title="{param_name}".format(
                param_name=param.name,
            ),
            subtitle="description: {description}".format(
                description=param.description
            ),
            autocomplete="{} {}".format(self.resource_id, param.name),
            arg=console_url,
            largetext=param.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_id(param.id)
        return item_arg


systemmanager_parameterstore_searcher = SystemManagerParameterStoreSearcher()
