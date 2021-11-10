# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_users
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class User(ResData):
    id = attr.ib()
    name = attr.ib()
    create_date = attr.ib()
    path = attr.ib()
    arn = attr.ib()

    def to_console_url(self):
        return "https://console.aws.amazon.com/iam/home#/users/{user_name}".format(
            user_name=self.name,
        )


class IamUsersSearcher(AwsResourceSearcher):
    id = "iam-users"
    limit_arg_name = "MaxItems"
    paginator_arg_name = "Marker"

    def boto3_call(self, **kwargs):
        return self.sdk.iam_client.list_users(**kwargs)

    def get_paginator(self, res):
        return res.get("Marker")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of iam_client.list_users

        :rtype: list[User]
        """
        user_list = list()
        for user_dict in res["Users"]:
            role = User(
                id=user_dict["UserId"],
                name=user_dict["UserName"],
                create_date=str(user_dict["CreateDate"]),
                path=user_dict["Path"],
                arn=user_dict["Arn"],
            )
            user_list.append(role)
        return user_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[User]
        """
        user_list = self.recur_list_res(limit=limit)
        user_list = list(sorted(
            user_list, key=lambda u: u.create_date, reverse=True))
        return user_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[User]
        """
        user_list = self.list_res(limit=1000)
        keys = [user.name for user in user_list]
        mapper = {user.name: user for user in user_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_user_list = fz_sr.match(query_str, limit=20)
        return matched_user_list

    def to_item(self, user):
        """
        :type user: User
        :rtype: ItemArgs
        """
        console_url = user.to_console_url()
        item_arg = ItemArgs(
            title="👤 {user_name}".format(
                user_name=user.name,
            ),
            subtitle=user.path,
            autocomplete="{} {}".format(self.resource_id, user.name),
            arg=console_url,
            largetext=user.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(user.arn)
        item_arg.copy_id(user.id)
        return item_arg


iam_users_searcher = IamUsersSearcher()
