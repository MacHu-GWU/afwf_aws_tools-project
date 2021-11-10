# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_keys
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Key(ResData):
    alias = attr.ib()
    arn = attr.ib()
    key_id = attr.ib()

    def to_console_url(self):
        if self.alias.startswith("alias/aws/"):
            key_type = "defaultKeys"
        else:
            key_type = "keys"
        return "https://console.aws.amazon.com/kms/home?region={region}#/kms/{key_type}/{key_id}".format(
            region=SettingValues.aws_region,
            key_type=key_type,
            key_id=self.key_id,
        )


class KMSCustomerManagedKeysSearcher(AwsResourceSearcher):
    id = "kms-customermanagedkeys"
    limit_arg_name = "Limit"
    paginator_arg_name = "Marker"

    def boto3_call(self, **kwargs):
        return self.sdk.kms_client.list_aliases(**kwargs)

    def get_paginator(self, res):
        return res.get("NextMarker")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of kms_client.list_keys

        :rtype: list[Key]
        """
        kms_key_list = list()
        for kms_key_dict in res["Aliases"]:
            kms_key = Key(
                alias=kms_key_dict["AliasName"],
                arn=kms_key_dict["AliasArn"],
                key_id=kms_key_dict.get("TargetKeyId", "unknown"),
            )
            kms_key_list.append(kms_key)
        return kms_key_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Key]
        """
        kms_key_list = self.recur_list_res(limit=limit)
        kms_key_list = filter(
            lambda k: not k.alias.startswith("alias/aws/"),
            kms_key_list,
        )
        kms_key_list = list(sorted(
            kms_key_list, key=lambda r: r.alias, reverse=True))
        return kms_key_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Key]
        """
        kms_key_list = self.list_res(limit=1000)
        keys = [kms_key.alias for kms_key in kms_key_list]
        mapper = {kms_key.alias: kms_key for kms_key in kms_key_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_kms_key_list = fz_sr.match(query_str, limit=20)
        return matched_kms_key_list

    def to_item(self, kms_key):
        """
        :type kms_key: Key
        :rtype: ItemArgs
        """
        console_url = kms_key.to_console_url()
        item_arg = ItemArgs(
            title="{kms_key_name}".format(
                kms_key_name=kms_key.alias,
            ),
            subtitle="key_id = {key_id}".format(
                key_id=kms_key.key_id,
            ),
            autocomplete="{} {}".format(self.resource_id, kms_key.alias),
            arg=console_url,
            largetext=kms_key.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(kms_key.arn)
        item_arg.copy_id(kms_key.id)
        return item_arg


kms_customermanagedkeys_searcher = KMSCustomerManagedKeysSearcher()
