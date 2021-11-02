# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_roles
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...cache import cache
from ...search.fuzzy import FuzzyObjectSearch


@attr.s
class Role(object):
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

    def to_largetext(self):
        return "\n".join([
            "id = {}".format(self.id),
            "name = {}".format(self.name),
            "description = {}".format(self.description),
            "create_date = {}".format(self.create_date),
            "path = {}".format(self.path),
            "arn = {}".format(self.arn),
        ])


def simplify_list_roles_response(res):
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


class IamRolesSearcher(AwsResourceSearcher):
    id = "iam-roles"
    cache_key = "aws-res-iam-roles"

    def list_roles_dict(self):
        """
        :rtype: list[dict]
        """
        roles = list()

        is_truncated = False
        marker = None
        while 1:
            kwargs = dict(MaxItems=1000)
            if is_truncated:
                kwargs["Marker"] = marker
            res = self.sdk.iam_client.list_roles(**kwargs)
            roles.extend(res.get("Roles", list()))
            is_truncated = res.get("IsTruncated", False)
            marker = res.get("Marker")
            if not is_truncated:
                break
        merged_res = {"Roles": roles}
        role_list = simplify_list_roles_response(merged_res)
        role_dict_list = [
            attr.asdict(role)
            for role in role_list
        ]
        role_dict_list = list(sorted(
            role_dict_list, key=lambda x: x["create_date"], reverse=True))
        return role_dict_list

    def list_res(self):
        """
        :rtype: list[Role]
        """
        role_dict_list = cache.fast_get(
            key=self.cache_key,
            callable=self.list_roles_dict,
            expire=10,
        )
        role_list = [
            Role(**role_dict)
            for role_dict in role_dict_list
        ]
        return role_list

    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Role]
        """
        role_list = self.list_res()
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
        largetext = role.to_largetext()
        item_arg = ItemArgs(
            title="{role_name}".format(
                role_name=role.name,
            ),
            subtitle="{description}".format(
                description=role.description
            ),
            autocomplete="{} {}".format(self.resource_id, role.name),
            arg=console_url,
            largetext=largetext,
            icon=find_svc_icon(self.id),
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(role.arn)
        return item_arg
