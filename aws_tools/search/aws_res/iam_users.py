# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_users
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...cache import cache
from ...search.fuzzy import FuzzyObjectSearch


@attr.s
class User(object):
    id = attr.ib()
    name = attr.ib()
    create_date = attr.ib()
    path = attr.ib()
    arn = attr.ib()

    def to_console_url(self):
        return "https://console.aws.amazon.com/iam/home#/users/{user_name}".format(
            user_name=self.name,
        )

    def to_largetext(self):
        return "\n".join([
            "id = {}".format(self.id),
            "name = {}".format(self.name),
            "create_date = {}".format(self.create_date),
            "path = {}".format(self.path),
            "arn = {}".format(self.arn),
        ])


def simplify_list_users_response(res):
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


class IamUsersSearcher(AwsResourceSearcher):
    id = "iam-users"
    cache_key = "aws-res-iam-users"

    def list_users_dict(self):
        """
        :rtype: list[dict]
        """
        users = list()

        is_truncated = False
        marker = None
        while 1:
            kwargs = dict(MaxItems=1000)
            if is_truncated:
                kwargs["Marker"] = marker
            res = self.sdk.iam_client.list_users(**kwargs)
            users.extend(res.get("Users", list()))
            is_truncated = res.get("IsTruncated", False)
            marker = res.get("Marker")
            if not is_truncated:
                break
        merged_res = {"Users": users}
        user_list = simplify_list_users_response(merged_res)
        user_dict_list = [
            attr.asdict(user)
            for user in user_list
        ]
        user_dict_list = list(sorted(
            user_dict_list, key=lambda x: x["create_date"], reverse=True))
        return user_dict_list

    def list_res(self):
        """
        :rtype: list[User]
        """
        user_dict_list = cache.fast_get(
            key=self.cache_key,
            callable=self.list_users_dict,
            expire=10,
        )
        user_list = [
            User(**user_dict)
            for user_dict in user_dict_list
        ]
        return user_list

    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[User]
        """
        role_list = self.list_res()
        keys = [role.name for role in role_list]
        mapper = {role.name: role for role in role_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_role_list = fz_sr.match(query_str, limit=20)
        return matched_role_list

    def to_item(self, user):
        """
        :type user: User
        :rtype: ItemArgs
        """
        console_url = user.to_console_url()
        largetext = user.to_largetext()
        item_arg = ItemArgs(
            title="{user_name}".format(
                user_name=user.name,
            ),
            subtitle=user.path,
            autocomplete="{} {}".format(self.resource_id, user.name),
            arg=console_url,
            largetext=largetext,
            icon=find_svc_icon(self.id),
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(user.arn)
        return item_arg
