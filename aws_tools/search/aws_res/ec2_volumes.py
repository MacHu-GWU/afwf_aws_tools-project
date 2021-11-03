# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_volumes
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...settings import SettingValues
from ...cache import cache
from ...helpers import union, intersect, tokenize


@attr.s(hash=True)
class Volume(ResData):
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
        return "https://console.aws.amazon.com/ec2/v2/home?region={region}#VolumeDetails:volumeId={vol_id}".format(
            vol_id=self.id,
            region=SettingValues.aws_region,
        )


vol_state_emoji_mapper = {
    "creating": "🟡",
    "available": "🟢",
    "in-use": "🟢",
    "deleting": "🟤",
    "deleted": "⚫",
    "error": "🔴",
}


class Ec2VolumesSearcher(AwsResourceSearcher):
    id = "ec2-volumes"
    has_search_box = True
    limit_arg_name = "MaxResults"
    paginator_arg_name = "NextToken"
    lister = AwsResourceSearcher.sdk.ec2_client.describe_volumes

    def to_search_url(self, query_str):
        return "https://console.aws.amazon.com/ec2/home?region={region}#Volumes:search={query_str}".format(
            region=SettingValues.aws_region,
            query_str=",".join(tokenize(query_str, space_only=True)),
        )

    def get_paginator(self, res):
        return res.get("NextToken")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of ec2_client.describe_volumes

        :rtype: list[Volume]
        """
        vol_list = list()
        for vol_dict in res.get("Volumes", list()):
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
        return vol_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Volume]
        """
        vol_list = self.recur_list_res(limit=limit)
        vol_list = list(sorted(
            vol_list, key=lambda v: v.create_time, reverse=True,
        ))
        return vol_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Volume]
        """
        args = tokenize(query_str)
        if len(args) == 1:
            res = self.sdk.ec2_client.describe_volumes(
                Filters=[
                    dict(Name="tag:Name", Values=["*{}*".format(args[0])]),
                ],
                MaxResults=20,
            )
            vol_list_by_name = self.simplify_response(res)

            res = self.sdk.ec2_client.describe_volumes(
                Filters=[
                    dict(Name="volume-id", Values=["*{}*".format(args[0])]),
                ],
                MaxResults=20,
            )
            vol_list_by_id = self.simplify_response(res)

            vol_list = union(vol_list_by_name, vol_list_by_id)
        elif len(args) > 1:
            vol_list_list = [self.filter_res(query_str=arg) for arg in args]
            vol_list = intersect(*vol_list_list)
        else:
            raise ValueError
        return vol_list

    def to_item(self, vol):
        """
        :type vol: Volume
        :rtype: ItemArgs
        """
        console_url = vol.to_console_url()
        item_arg = ItemArgs(
            title=vol.name,
            subtitle="{state} {id} {type}".format(
                state=vol_state_emoji_mapper.get(vol.state, "❓"),
                id=vol.id,
                type=vol.type,
            ),
            autocomplete="{} {}".format(self.id, vol.id),
            arg=console_url,
            largetext=vol.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        return item_arg

ec2_volumns_searcher = Ec2VolumesSearcher()
