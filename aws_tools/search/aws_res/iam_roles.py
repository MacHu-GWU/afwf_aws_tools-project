# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_roles
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Role(ResData):
    id = attr.ib()
    name = attr.ib()
    description = attr.ib()
    create_date = attr.ib()
    path = attr.ib()
    arn = attr.ib()

    def to_console_url(self):
        return "https://console.aws.amazon.com/iam/home#/roles/{role_name}".format(
            role_name=self.name,
        )


class IamRolesSearcher(AwsResourceSearcher):
    id = "iam-roles"
    limit_arg_name = "MaxItems"
    paginator_arg_name = "Marker"

    def boto3_call(self, **kwargs):
        return self.sdk.iam_client.list_roles(**kwargs)

    def get_paginator(self, res):
        return res.get("Marker")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of iam_client.list_roles

        :rtype: list[Role]
        """
        role_list = list()
        for role_dict in res["Roles"]:
            role = Role(
                id=role_dict["RoleId"],
                name=role_dict["RoleName"],
                description=role_dict.get("Description"),
                create_date=str(role_dict["CreateDate"]),
                path=role_dict["Path"],
                arn=role_dict["Arn"],
            )
            role_list.append(role)
        return role_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Role]
        """
        role_list = self.recur_list_res(limit=limit)
        role_list = list(sorted(
            role_list, key=lambda r: r.create_date, reverse=True))
        return role_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Role]
        """
        role_list = self.list_res(limit=1000)
        keys = [role.name for role in role_list]
        mapper = {role.name: role for role in role_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_role_list = fz_sr.match(query_str, limit=20)
        return matched_role_list

    def to_item(self, role):
        """
        :type role: Role
        :rtype: ItemArgs
        """
        console_url = role.to_console_url()
        item_arg = ItemArgs(
            title="{role_name}".format(
                role_name=role.name,
            ),
            subtitle="{description}".format(
                description=role.description
            ),
            autocomplete="{} {}".format(self.resource_id, role.name),
            arg=console_url,
            largetext=role.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(role.arn)
        item_arg.copy_id(role.id)
        return item_arg

iam_roles_searcher = IamRolesSearcher()
