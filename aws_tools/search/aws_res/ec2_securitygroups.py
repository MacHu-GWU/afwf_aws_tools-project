# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import attr
from collections import OrderedDict
from ..aws_resources import AwsResourceSearcher, ItemArgs
from ...icons import Icons
from ...settings import SettingValues
from ...alfred import Base
from ...cache import cache


@attr.s
class SecurityGroup(Base):
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

    def to_largetext(self):
        return "\n".join([
            "id = {}".format(self.id),
            "name = {}".format(self.name),
            "description = {}".format(self.description),
            "vpc_id = {}".format(self.vpc_id),
            "n_ingress = {}".format(self.n_ingress),
            "n_egress = {}".format(self.n_egress),
        ])


def simplify_describe_security_groups_response(res):
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


class Ec2SecurityGroupsSearcher(AwsResourceSearcher):
    id = "ec2-securitygroups"

    @cache.memoize(expire=10)
    def list_res(self):
        """
        :rtype: list[SecurityGroup]
        """
        res = self.sdk.ec2_client.describe_security_groups(MaxResults=20)
        return simplify_describe_security_groups_response(res)

    @cache.memoize(expire=10)
    def filter_res(self, query_str):
        """
        Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_security_groups

        :type query_str: str
        :rtype: list[SecurityGroup]
        """
        filter_ = dict(Name="group-name", Values=["*{}*".format(query_str)])
        res = self.sdk.ec2_client.describe_security_groups(
            Filters=[filter_, ],
            MaxResults=20,
        )
        sg_list_by_name = simplify_describe_security_groups_response(res)

        filter_ = dict(Name="group-id", Values=["*{}*".format(query_str)])
        res = self.sdk.ec2_client.describe_security_groups(
            Filters=[filter_, ],
            MaxResults=20,
        )
        sg_list_by_id = simplify_describe_security_groups_response(res)

        sg_list = sg_list_by_name + sg_list_by_id

        # deduplicate
        sg_mapper = OrderedDict([
            (sg.id, sg)
            for sg in sg_list
        ])
        sg_list = list(sg_mapper.values())

        return sg_list

    def to_item(self, sg):
        """
        :type sg: SecurityGroup
        :rtype: ItemArgs
        """
        console_url = sg.to_console_url()
        largetext = sg.to_largetext()
        item_arg = ItemArgs(
            title="{sg_id} {sg_name}".format(
                sg_id=sg.short_id,
                sg_name=sg.name,
            ),
            subtitle="{vpc_id} {description}".format(
                vpc_id=sg.short_vpc_id,
                description=sg.description
            ),
            autocomplete="{} {}".format(self.resource_id, sg.id),
            arg=console_url,
            largetext=largetext,
            icon=Icons.abspath(Icons.Arch_Amazon_Virtual_Private_Cloud),
            valid=True,
        )
        item_arg.open_browser(console_url)
        return item_arg
