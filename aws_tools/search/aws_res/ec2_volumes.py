# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import attr
from collections import OrderedDict
from ..aws_resources import AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...settings import SettingValues
from ...cache import cache
from ...alfred import Base


@attr.s
class Volume(Base):
    id = attr.ib()
    name = attr.ib()
    type = attr.ib()
    size = attr.ib()
    state = attr.ib()
    create_time = attr.ib()

    @property
    def short_id(self):
        return self.id[:8] + "..." + self.id[-4:]

    def to_console_url(self):
        return "https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#VolumeDetails:volumeId={vol_id}".format(
            vol_id=self.id,
            region=SettingValues.aws_region,
        )

    def to_largetext(self):
        return "\n".join([
            "id = {}".format(self.id),
            "name = {}".format(self.name),
            "type = {}".format(self.type),
            "size = {}".format(self.size),
            "state = {}".format(self.state),
            "create_time = {}".format(self.create_time),
        ])


def simplify_describe_volumes_response(res):
    """
    :type res: dict
    :param res: the return of ec2_client.describe_volumes

    :rtype: list[Volume]
    """
    if len(res["Volumes"]) == 0:
        return []
    vol_list = list()
    for vol_dict in res["Volumes"]:
        vol_id = vol_dict["VolumeId"]
        vol_name = "~"
        for tag in vol_dict.get("Tags", []):
            if tag["Key"] == "Name":
                vol_name = tag["Value"]
        vol_type = vol_dict["VolumeType"]
        state = vol_dict["State"]
        size = vol_dict["Size"]
        create_time = str(vol_dict["CreateTime"])
        vol = Volume(
            id=vol_id,
            name=vol_name,
            type=vol_type,
            size=size,
            state=state,
            create_time=create_time,
        )
        vol_list.append(vol)
    # sort by volume name
    vol_list = list(sorted(
        vol_list, key=lambda v: v.create_time, reverse=False))
    return vol_list


vol_state_emoji_mapper = {
    "creating": "💛",
    "available": "💚",
    "in-use": "💚",
    "deleting": "🤎",
    "deleted": "⚫",
    "error": "❤️",
}


class Ec2VolumesSearcher(AwsResourceSearcher):
    id = "ec2-volumes"
    cache_key_all = "aws-res-ec2-volumes-all"
    cache_key_filtered = "aws-res-ec2-volumes-filtered-{query_str}"

    def list_res(self):
        """
        :rtype: list[Volume]
        """
        res = cache.fast_get(
            key=self.cache_key_all,
            callable=self.sdk.ec2_client.describe_volumes,
            kwargs=dict(MaxResults=20),
            expire=10,
        )
        vol_list = simplify_describe_volumes_response(res)
        return vol_list

    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Volume]
        """
        cache_key = self.cache_key_filtered.format(query_str=query_str)
        if cache_key in cache:
            vol_list = cache[cache_key]
        else:
            res = self.sdk.ec2_client.describe_volumes(
                Filters=[
                    dict(Name="tag:Name", Values=["*{}*".format(query_str)]),
                ],
                MaxResults=20,
            )
            vol_list_by_name = simplify_describe_volumes_response(res)

            res = self.sdk.ec2_client.describe_volumes(
                Filters=[
                    dict(Name="volume-id", Values=["*{}*".format(query_str)]),
                ],
                MaxResults=20,
            )
            vol_list_by_id = simplify_describe_volumes_response(res)

            vol_list = vol_list_by_name + vol_list_by_id

            # deduplicate
            vol_mapper = OrderedDict([
                (vol.id, vol)
                for vol in vol_list
            ])
            vol_list = list(vol_mapper.values())

        return vol_list

    def to_item(self, vol):
        """
        :type vol: Volume
        :rtype: ItemArgs
        """
        console_url = vol.to_console_url()
        largetext = vol.to_largetext()
        item_arg = ItemArgs(
            title=vol.name,
            subtitle="{state} {id} {type}".format(
                state=vol_state_emoji_mapper.get(vol.state, "❓"),
                id=vol.id,
                type=vol.type,
            ),
            autocomplete="{} {}".format(self.id, vol.id),
            arg=console_url,
            largetext=largetext,
            icon=find_svc_icon(self.id),
            valid=True,
        )
        item_arg.open_browser(console_url)
        return item_arg
