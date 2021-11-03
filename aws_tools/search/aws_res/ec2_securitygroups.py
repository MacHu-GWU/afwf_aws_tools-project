# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_security_groups
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...icons import Icons
from ...settings import SettingValues
from ...cache import cache
from ...helpers import union, intersect, tokenize


@attr.s(hash=True)
class SecurityGroup(ResData):
    id = attr.ib()
    name = attr.ib()
    description = attr.ib()
    vpc_id = attr.ib()
    n_ingress = attr.ib()
    n_egress = attr.ib()

    @property
    def short_id(self):
        return self.id[:7] + "..." + self.id[-4:]

    @property
    def short_vpc_id(self):
        return self.vpc_id[:8] + "..." + self.vpc_id[-4:]

    def to_console_url(self):
        return "https://console.aws.amazon.com/ec2/v2/home?region={region}#SecurityGroup:groupId={sg_id}".format(
            sg_id=self.id,
            region=SettingValues.aws_region,
        )


class Ec2SecurityGroupsSearcher(AwsResourceSearcher):
    id = "ec2-securitygroups"
    has_search_box = True

    def to_search_url(self, query_str):
        return "https://console.aws.amazon.com/ec2/v2/home?region={region}#SecurityGroups:search={query_str}".format(
            region=SettingValues.aws_region,
            query_str=",".join(tokenize(query_str, space_only=True))
        )

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of ec2_client.describe_security_groups

        :rtype: list[SecurityGroup]
        """
        sg_list = list()
        for sg_dict in res["SecurityGroups"]:
            sg = SecurityGroup(
                id=sg_dict["GroupId"],
                name=sg_dict["GroupName"],
                description=sg_dict["Description"],
                vpc_id=sg_dict["VpcId"],
                n_ingress=len(sg_dict["IpPermissions"]),
                n_egress=len(sg_dict["IpPermissionsEgress"]),
            )
            sg_list.append(sg)
            # sort by volume name
        sg_list = list(sorted(
            sg_list, key=lambda v: v.name, reverse=False))
        return sg_list

    @cache.memoize(expire=10)
    def list_res(self):
        """
        :rtype: list[SecurityGroup]
        """
        res = self.sdk.ec2_client.describe_security_groups(MaxResults=SettingValues.search_limit)
        return self.simplify_response(res)

    @cache.memoize(expire=10)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[SecurityGroup]
        """
        args = tokenize(query_str)
        if len(args) == 1:
            filter_ = dict(Name="group-name", Values=["*{}*".format(args[0])])
            res = self.sdk.ec2_client.describe_security_groups(
                Filters=[filter_, ],
                MaxResults=SettingValues.search_limit,
            )
            sg_list_by_name = self.simplify_response(res)

            filter_ = dict(Name="group-id", Values=["*{}*".format(args[0])])
            res = self.sdk.ec2_client.describe_security_groups(
                Filters=[filter_, ],
                MaxResults=SettingValues.search_limit,
            )
            sg_list_by_id = self.simplify_response(res)

            sg_list = union(sg_list_by_name, sg_list_by_id)
        elif len(args) > 1:
            sg_list_list = [self.filter_res(query_str=arg) for arg in args]
            sg_list = intersect(*sg_list_list)
        else:
            raise Exception
        return sg_list

    def to_item(self, sg):
        """
        :type sg: SecurityGroup
        :rtype: ItemArgs
        """
        console_url = sg.to_console_url()
        item_arg = ItemArgs(
            title="🛡️ {sg_id} {sg_name}".format(
                sg_id=sg.short_id,
                sg_name=sg.name,
            ),
            subtitle="{vpc_id} {description}".format(
                vpc_id=sg.short_vpc_id,
                description=sg.description
            ),
            autocomplete="{} {}".format(self.resource_id, sg.id),
            arg=console_url,
            largetext=sg.to_large_text(),
            icon=Icons.abspath(Icons.Arch_Amazon_Virtual_Private_Cloud),
            valid=True,
        )
        item_arg.open_browser(console_url)
        return item_arg


ec2_securitygroups_searcher = Ec2SecurityGroupsSearcher()
