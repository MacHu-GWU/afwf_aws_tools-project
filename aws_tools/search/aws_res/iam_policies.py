# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policies
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...cache import cache
from ...search.fuzzy import FuzzyObjectSearch


@attr.s
class Policy(object):
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


def simplify_list_policys_response(res):
    """
    :type res: dict
    :param res: the return of iam_client.list_policies

    :rtype: list[Policy]
    """
    policy_list = list()
    for policy_dict in res["Policys"]:
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


class IamPolicysSearcher(AwsResourceSearcher):
    id = "iam-policies"
    cache_key = "aws-res-iam-policies"

    def list_policys_dict(self):
        """
        :rtype: list[Policy]
        """
        policies = list()
        is_truncated = False
        marker = None
        while 1:
            kwargs = dict(
                Scope="All",
                MaxItems=1000,
            )
            if is_truncated:
                kwargs["Marker"] = marker
            res = self.sdk.iam_client.list_policies(**kwargs)
            policies.extend(res.get("Policies", list()))
            is_truncated = res.get("IsTruncated", False)
            marker = res.get("Marker")
            if not is_truncated:
                break
        merged_res = {"Policys": policies}
        policy_list = simplify_list_policys_response(merged_res)
        policy_dict_list = [
            attr.asdict(policy)
            for policy in policy_list
        ]
        policy_dict_list = list(sorted(
            policy_dict_list, key=lambda x: x["update_date"], reverse=True))
        return policy_dict_list

    def list_res(self):
        """
        :rtype: list[Policy]
        """
        policy_dict_list = cache.fast_get(
            key=self.cache_key,
            callable=self.list_policys_dict,
            expire=10,
        )
        policy_list = [
            Policy(**policy_dict)
            for policy_dict in policy_dict_list
        ]
        return policy_list

    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Policy]
        """
        policy_list = self.list_res()
        keys = [policy.name for policy in policy_list]
        mapper = {policy.name: policy for policy in policy_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_policy_list = fz_sr.match(query_str, limit=20)
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
        return item_arg
