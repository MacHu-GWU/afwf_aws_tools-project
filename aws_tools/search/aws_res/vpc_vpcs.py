# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...helpers import tokenize
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Vpc(ResData):
    id = attr.ib()
    name = attr.ib()
    cidr_block = attr.ib()
    state = attr.ib()
    is_default = attr.ib()

    @property
    def short_id(self):
        return self.id[:8] + "..." + self.id[-4:]

    def to_console_url(self):
        return "https://{domain}/vpc/home?region={region}#vpcs:search={vpc_id}".format(
            domain=SettingValues.get_console_domain(),
            vpc_id=self.id,
            region=SettingValues.aws_region,
        )


vpc_state_emoji_mapper = {
    "pending": "🟡",
    "available": "🟢",
}


class VpcVpcsSearcher(AwsResourceSearcher):
    id = "vpc-vpcs"
    has_search_box = True
    limit_arg_name = "MaxResults"
    paginator_arg_name = "NextToken"

    def boto3_call(self, **kwargs):
        return self.sdk.ec2_client.describe_vpcs(**kwargs)

    def to_search_url(self, query_str):
        return "https://console.aws.amazon.com/vpc/home?region={region}#vpcs:search={query_str}".format(
            region=SettingValues.aws_region,
            query_str=",".join(tokenize(query_str, space_only=True))
        )

    def get_paginator(self, res):
        return res.get("NextToken")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of vpc_client.describe_vpcs

        :rtype: list[Vpc]
        """
        vpc_list = list()
        for vpc_dict in res["Vpcs"]:
            vpc_name = ""
            for tag in vpc_dict.get("Tags", []):
                if tag["Key"] == "Name":
                    vpc_name = tag["Value"]
            vpc = Vpc(
                id=vpc_dict["VpcId"],
                name=vpc_name,
                cidr_block=vpc_dict["CidrBlock"],
                state=vpc_dict["State"],
                is_default=vpc_dict["IsDefault"],
            )
            vpc_list.append(vpc)
        return vpc_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Vpc]
        """
        vpc_list = self.recur_list_res(limit=limit)
        vpc_list = list(sorted(
            vpc_list, key=lambda r: r.name))
        return vpc_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Vpc]
        """
        vpc_list = self.list_res(limit=1000)
        keys = [vpc.name for vpc in vpc_list]
        mapper = {vpc.name: vpc for vpc in vpc_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_vpc_list = fz_sr.match(query_str, limit=20)
        return matched_vpc_list

    def to_item(self, vpc):
        """
        :type vpc: Vpc
        :rtype: ItemArgs
        """
        console_url = vpc.to_console_url()
        item_arg = ItemArgs(
            title=vpc.name,
            subtitle="{state} {id}{default}".format(
                state=vpc_state_emoji_mapper.get(vpc.state, "❓"),
                id=vpc.short_id,
                default=" (default)" if vpc.is_default else "",
            ),
            autocomplete="{} {}".format(self.resource_id, vpc.id),
            arg=console_url,
            largetext=vpc.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_id(vpc.id)
        return item_arg


vpc_vpcs_searcher = VpcVpcsSearcher()
