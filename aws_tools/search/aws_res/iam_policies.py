# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policies
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Policy(ResData):
    id = attr.ib()
    name = attr.ib()
    description = attr.ib()
    update_date = attr.ib()
    path = attr.ib()
    arn = attr.ib()

    def to_console_url(self):
        return "https://console.aws.amazon.com/iam/home#/policies/{policy_arn}".format(
            policy_arn=self.arn
        )

    def to_largetext(self):
        return "\n".join([
            "id = {}".format(self.id),
            "name = {}".format(self.name),
            "description = {}".format(self.description),
            "update_date = {}".format(self.update_date),
            "path = {}".format(self.path),
            "arn = {}".format(self.arn),
        ])


class IamPolicysSearcher(AwsResourceSearcher):
    id = "iam-policies"

    limit_arg_name = "MaxItems"
    paginator_arg_name = "Marker"
    lister = AwsResourceSearcher.sdk.iam_client.list_policies

    def get_paginator(self, res):
        return res.get("Marker")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of iam_client.list_policies

        :rtype: list[Policy]
        """
        policy_list = list()
        for policy_dict in res["Policies"]:
            policy = Policy(
                id=policy_dict["PolicyId"],
                name=policy_dict["PolicyName"],
                description=policy_dict.get("Description"),
                update_date=str(policy_dict["UpdateDate"]),
                path=policy_dict["Path"],
                arn=policy_dict["Arn"],
            )
            policy_list.append(policy)
        return policy_list

    @cache.memoize(expire=SettingValues.expire)
    def list_res(self, limit=SettingValues.limit):
        """
        :rtype: list[Policy]
        """
        policy_list = self.recur_list_res(kwargs=dict(Scope="All"), limit=limit)
        policy_list = list(sorted(
            policy_list, key=lambda p: p.update_date, reverse=True,
        ))
        return policy_list

    @cache.memoize(expire=SettingValues.expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Policy]
        """
        policy_list = self.list_res(limit=1000)
        keys = [policy.name for policy in policy_list]
        mapper = {policy.name: policy for policy in policy_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_policy_list = fz_sr.match(query_str, limit=SettingValues.limit)
        return matched_policy_list

    def to_item(self, policy):
        """
        :type policy: Policy
        :rtype: ItemArgs
        """
        console_url = policy.to_console_url()
        largetext = policy.to_largetext()
        item_arg = ItemArgs(
            title="{policy_name}".format(
                policy_name=policy.name,
            ),
            subtitle="{description}".format(
                description=policy.description
            ),
            autocomplete="{} {}".format(self.resource_id, policy.name),
            arg=console_url,
            largetext=largetext,
            icon=find_svc_icon(self.id),
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(policy.arn)
        return item_arg
