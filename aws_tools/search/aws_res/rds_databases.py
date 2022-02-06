# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...settings import SettingValues
from ...cache import cache
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Instance(ResData):
    id = attr.ib()
    dbname = attr.ib()
    engine = attr.ib()
    class_ = attr.ib()
    endpoint = attr.ib()
    status = attr.ib()

    def to_console_url(self):
        return "https://{domain}/rds/home?region={region}#database:id={inst_id};is-cluster=false".format(
            domain=SettingValues.get_console_domain(),
            inst_id=self.id,
            region=SettingValues.aws_region,
        )


inst_state_emoji_mapper = {
    "available": "🟢",
    "backing-up": "🟡",
    "configuring-enhanced-monitoring": "",
    "configuring-iam-database-auth": "",
    "configuring-log-exports": "",
    "converting-to-vpc": "",
    "creating": "🟡",
    "deleting": "🟤",
    "failed": "🔴",
    "inaccessible-encryption-credentials": "",
    "incompatible-network": "",
    "incompatible-option-group": "",
    "incompatible-parameters": "",
    "incompatible-restore": "",
    "maintenance": "🟡",
    "modifying": "🟡",
    "moving-to-vpc": "",
    "rebooting": "🟡",
    "resetting-master-credentials": "",
    "renaming": "🟡",
    "restore-error": "",
    "starting": "🟡",
    "stopped": "🔴",
    "stopping": "🟠",
    "storage-full": "🔴",
    "storage-optimization": "",
    "upgrading": "🟡",
}


class RdsDatabasesSearcher(AwsResourceSearcher):
    id = "rds-databases"
    limit_arg_name = "MaxRecords"
    paginator_arg_name = "Marker"

    def boto3_call(self, **kwargs):
        return self.sdk.rds_client.describe_db_instances(**kwargs)

    def get_paginator(self, res):
        return res.get("Marker")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of rds_client.describe_db_instances

        :rtype: list[Instance]
        """
        inst_list = list()
        for inst_dict in res["DBInstances"]:
            inst = Instance(
                id=inst_dict["DBInstanceIdentifier"],
                dbname=inst_dict.get("DBName"),
                engine=inst_dict["Engine"],
                class_=inst_dict["DBInstanceClass"],
                endpoint=inst_dict["Endpoint"],
                status=inst_dict["DBInstanceStatus"],
            )
            inst_list.append(inst)
        return inst_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Instance]
        """
        inst_list = self.recur_list_res(page_size=100, limit=limit)
        inst_list = list(sorted(inst_list, key=lambda i: i.id))
        return inst_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Instance]
        """
        inst_list = self.list_res(limit=1000)
        keys = [inst.id for inst in inst_list]
        mapper = {inst.id: inst for inst in inst_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_inst_list = fz_sr.match(query_str, limit=20)
        return matched_inst_list

    def to_item(self, inst):
        """
        :type inst: Instance
        :rtype: ItemArgs
        """
        console_url = inst.to_console_url()
        largetext = inst.to_large_text()
        item_arg = ItemArgs(
            title=inst.id,
            subtitle="{state} {engine} {class_}".format(
                state=inst_state_emoji_mapper.get(inst.status) if inst_state_emoji_mapper.get(inst.status) else "❓",
                engine=inst.engine,
                class_=inst.class_,
            ),
            autocomplete="{} {}".format(self.resource_id, inst.id),
            arg=console_url,
            largetext=largetext,
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_id(inst.id)
        return item_arg


rds_databases_searcher = RdsDatabasesSearcher()
