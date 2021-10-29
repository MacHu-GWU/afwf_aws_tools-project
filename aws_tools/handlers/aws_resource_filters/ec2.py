# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from workflow.workflow3 import Item3
from pprint import pprint

from ...sdk import sdk
from ...cache import cache
from ...helpers import json_dumps, json_loads
from ...icons import Icons


def _simplify_describe_instances_response(res):
    if len(res["Reservations"]) == 0:
        return []
    inst_data_list = list()
    for reservation_dict in res["Reservations"]:
        for inst_dict in reservation_dict["Instances"]:
            instance_id = inst_dict["InstanceId"]
            instance_type = inst_dict["InstanceType"]
            state = inst_dict["State"]["Name"]
            public_ip = inst_dict.get("PublicIpAddress")
            private_ip = inst_dict.get("PrivateIpAddress")
            instance_name = ""
            for tag in inst_dict.get("Tags", []):
                if tag["Key"] == "Name":
                    instance_name = tag["Value"]
            inst_data = dict(
                instance_id=instance_id,
                instance_type=instance_type,
                state=state,
                public_ip=public_ip,
                private_ip=private_ip,
                instance_name=instance_name,
            )
            inst_data_list.append(inst_data)
    return inst_data_list


state_emoji_mapper = {
    "pending": "💛",
    "running": "💛",
    "shutting-down": "🧡",
    "terminated": "⚫",
    "stopping": "🧡",
    "stopped": "⚫", # "⚫"
}


def instances(query_str):
    """

    Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

    :type query_str: str
    :param query_str:
    :rtype: list[Item3]
    :return:
    """
    if query_str is None:
        res = sdk.ec2_client.describe_instances(MaxResults=100)
        inst_data_list = _simplify_describe_instances_response(res)
    else:
        res_by_name = sdk.ec2_client.describe_instances(
            Filters=[
                {
                    "Name": "tag:Name",
                    "Values": [
                        "*{}*".format(query_str),
                    ]
                },
            ],
            MaxResults=100,
        )
        res_by_id = sdk.ec2_client.describe_instances(
            Filters=[
                {
                    "Name": "instance-id",
                    "Values": [
                        "*{}*".format(query_str),
                    ]
                },
            ],
            MaxResults=100,
        )
        inst_data_list = _simplify_describe_instances_response(res_by_name) \
                         + _simplify_describe_instances_response(res_by_id)

    inst_mapper = dict()
    for inst_data in inst_data_list:
        inst_mapper[inst_data["instance_id"]] = inst_data
    inst_data_list = list(sorted(inst_mapper.values(), key=lambda x: x["instance_name"]))

    item_list = list()
    for inst_data in inst_data_list:
        title = inst_data["instance_name"]
        subtitle = "{state} {id} {type}".format(
            state=state_emoji_mapper[inst_data["state"]],
            id=inst_data["instance_id"],
            type=inst_data["instance_type"],
        )
        autocomplete = inst_data["instance_name"]
        arg = "https://console.aws.amazon.com/ec2/v2/home#InstanceDetails:instanceId={}".format(
            inst_data["instance_id"])
        item_list.append(
            Item3(
                title=title,
                subtitle=subtitle,
                autocomplete=autocomplete,
                arg=arg,
                valid=True,
                icon=Icons.abspath(Icons.Res_Amazon_EC2_Instance),
            )
        )

    return item_list
