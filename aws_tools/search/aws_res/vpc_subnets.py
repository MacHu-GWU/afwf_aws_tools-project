# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...helpers import union, intersect, tokenize


@attr.s(hash=True)
class Subnet(ResData):
    id = attr.ib()
    vpc_id = attr.ib()
    name = attr.ib()
    cidr_block = attr.ib()
    state = attr.ib()
    arn = attr.ib()

    @property
    def short_id(self):
        return self.id[:11] + "..." + self.id[-4:]

    def to_console_url(self):
        return "https://console.aws.amazon.com/vpc/home?region={region}#subnets:search={subnet_id}".format(
            subnet_id=self.id,
            region=SettingValues.aws_region,
        )


subnet_state_emoji_mapper = {
    "pending": "🟡",
    "available": "🟢",
}


class VpcSubnetsSearcher(AwsResourceSearcher):
    id = "vpc-subnets"
    has_search_box = True
    limit_arg_name = "MaxResults"
    paginator_arg_name = "NextToken"

    def boto3_call(self, **kwargs):
        return self.sdk.ec2_client.describe_subnets(**kwargs)

    def to_search_url(self, query_str):
        return "https://console.aws.amazon.com/vpc/home?region={region}#subnets:search={query_str}".format(
            region=SettingValues.aws_region,
            query_str=",".join(tokenize(query_str, space_only=True))
        )

    def get_paginator(self, res):
        return res.get("NextToken")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of subnet_client.describe_subnets

        :rtype: list[Subnet]
        """
        subnet_list = list()
        for subnet_dict in res["Subnets"]:
            subnet_name = ""
            for tag in subnet_dict.get("Tags", []):
                if tag["Key"] == "Name":
                    subnet_name = tag["Value"]
            subnet = Subnet(
                id=subnet_dict["SubnetId"],
                vpc_id=subnet_dict["VpcId"],
                name=subnet_name,
                cidr_block=subnet_dict["CidrBlock"],
                state=subnet_dict["State"],
                arn=subnet_dict["SubnetArn"],
            )
            subnet_list.append(subnet)
        return subnet_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Subnet]
        """
        subnet_list = self.recur_list_res(limit=limit)
        subnet_list = list(sorted(subnet_list, key=lambda r: r.name))
        return subnet_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Subnet]
        """
        args = tokenize(query_str)
        if len(args) == 1:
            filter_ = dict(Name="tag:Name", Values=["*{}*".format(args[0])])
            res = self.sdk.ec2_client.describe_subnets(
                Filters=[filter_, ],
                MaxResults=SettingValues.search_limit,
            )
            subnet_list_by_name = self.simplify_response(res)

            filter_ = dict(Name="subnet-id", Values=["*{}*".format(args[0])])
            res = self.sdk.ec2_client.describe_subnets(
                Filters=[filter_, ],
                MaxResults=SettingValues.search_limit,
            )
            subnet_list_by_id = self.simplify_response(res)

            subnet_list = union(subnet_list_by_name, subnet_list_by_id)

        elif len(args) > 1:
            subnet_list_list = [self.filter_res(query_str=arg) for arg in args]
            subnet_list = intersect(*subnet_list_list)
        else:
            raise ValueError

        return subnet_list

    def to_item(self, subnet):
        """
        :type subnet: Subnet
        :rtype: ItemArgs
        """
        console_url = subnet.to_console_url()
        item_arg = ItemArgs(
            title=subnet.name,
            subtitle="{state} {id}".format(
                state=subnet_state_emoji_mapper.get(subnet.state, "❓"),
                id=subnet.short_id,
            ),
            autocomplete="{} {}".format(self.resource_id, subnet.id),
            arg=console_url,
            largetext=subnet.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_id(subnet.id)
        return item_arg


vpc_subnets_searcher = VpcSubnetsSearcher()
