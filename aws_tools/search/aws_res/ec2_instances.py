# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import attr
from ordered_set import OrderedSet
from ..aws_resources import AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...settings import SettingValues
from ...cache import cache
from ...alfred import Base


@attr.s(hash=True)
class Instance(Base):
    id = attr.ib()
    name = attr.ib()
    type = attr.ib()
    state = attr.ib()
    public_ip = attr.ib()
    private_ip = attr.ib()

    @property
    def short_id(self):
        return self.id[:6] + "..." + self.id[-4:]

    def to_console_url(self):
        return "https://console.aws.amazon.com/ec2/v2/home?region={region}#InstanceDetails:instanceId={inst_id}".format(
            inst_id=self.id,
            region=SettingValues.aws_region,
        )

    def to_largetext(self):
        return "\n".join([
            "public_ip = {}".format(self.public_ip),
            "private_ip = {}".format(self.private_ip),
        ])

    def __hash__(self):
        return hash(self.id)


def simplify_describe_instances_response(res):
    """
    :type res: dict
    :param res: the return of ec2_client.describe_instances

    :rtype: list[Instance]
    """
    if len(res["Reservations"]) == 0:
        return []
    inst_list = list()
    for reservation_dict in res["Reservations"]:
        for inst_dict in reservation_dict["Instances"]:
            instance_id = inst_dict["InstanceId"]
            instance_name = ""
            for tag in inst_dict.get("Tags", []):
                if tag["Key"] == "Name":
                    instance_name = tag["Value"]
            instance_type = inst_dict["InstanceType"]
            state = inst_dict["State"]["Name"]
            public_ip = inst_dict.get("PublicIpAddress")
            private_ip = inst_dict.get("PrivateIpAddress")
            inst = Instance(
                id=instance_id,
                type=instance_type,
                name=instance_name,
                state=state,
                public_ip=public_ip,
                private_ip=private_ip,
            )
            inst_list.append(inst)
    inst_list = list(sorted(inst_list, key=lambda x: x.name))
    return inst_list


inst_state_emoji_mapper = {
    "pending": "💛",
    "running": "💚",
    "shutting-down": "🤎",
    "terminated": "⚫",
    "stopping": "🧡",
    "stopped": "❤️",
}


class Ec2InstancesSearcher(AwsResourceSearcher):
    id = "ec2-instances"

    @cache.memoize(expire=SettingValues.expire)
    def list_res(self):
        """
        :rtype: list[Instance]
        """
        res = self.sdk.ec2_client.describe_instances(MaxResults=20)
        return simplify_describe_instances_response(res)

    @cache.memoize(expire=SettingValues.expire)
    def filter_res(self, query_str):
        """
        Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

        :type query_str: str
        :rtype: list[Instance]
        """
        args = [arg for arg in query_str.split(" ") if arg.strip()]
        if len(args) == 1:
            filter_ = dict(Name="tag:Name", Values=["*{}*".format(query_str)])
            res = self.sdk.ec2_client.describe_instances(
                Filters=[filter_, ],
                MaxResults=20,
            )
            inst_by_name = simplify_describe_instances_response(res)

            filter_ = dict(Name="instance-id", Values=["*{}*".format(query_str)])
            res = self.sdk.ec2_client.describe_instances(
                Filters=[filter_, ],
                MaxResults=20,
            )
            inst_by_id = simplify_describe_instances_response(res)
            inst_list = list(OrderedSet(inst_by_name) | OrderedSet(inst_by_id))
            return inst_list
        elif len(args) > 1:
            inst_set = OrderedSet(self.filter_res(query_str=args[0]))
            for arg in args[1:]:
                inst_set &= self.filter_res(query_str=arg)
            inst_list = list(inst_set)
            return inst_list
        else:
            raise Exception

    def to_item(self, inst):
        """
        :type inst: Instance
        :rtype: ItemArgs
        """
        console_url = inst.to_console_url()
        largetext = inst.to_largetext()
        item_arg = ItemArgs(
            title=inst.name,
            subtitle="{state} {id} {type}".format(
                state=inst_state_emoji_mapper.get(inst.state, "❓"),
                id=inst.short_id,
                type=inst.type,
            ),
            autocomplete="{} {}".format(self.id, inst.id),
            arg=console_url,
            largetext=largetext,
            icon=find_svc_icon(self.id),
            valid=True,
        )
        item_arg.open_browser(console_url)
        return item_arg
