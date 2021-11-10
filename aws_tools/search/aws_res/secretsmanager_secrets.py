# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.list_secrets
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Secret(ResData):
    name = attr.ib()
    description = attr.ib()
    arn = attr.ib()
    kms_id = attr.ib()
    rotation_enabled = attr.ib()

    @property
    def id(self):
        return self.name

    def to_console_url(self):
        return "https://console.aws.amazon.com/secretsmanager/home?region={region}#!/secret?name={name}".format(
            region=SettingValues.aws_region,
            name=self.name,
        )


class SecretmanagerSecretsSearcher(AwsResourceSearcher):
    id = "secretsmanager-secrets"
    limit_arg_name = "MaxResults"
    paginator_arg_name = "NextToken"

    def boto3_call(self, **kwargs):
        return self.sdk.sm_client.list_secrets(**kwargs)

    def get_paginator(self, res):
        return res.get("NextToken")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of sm_client.list_secrets

        :rtype: list[Secret]
        """
        secret_list = list()
        for secret_dict in res["SecretList"]:
            secret = Secret(
                name=secret_dict["Name"],
                description=secret_dict.get("Description"),
                arn=secret_dict["ARN"],
                kms_id=secret_dict.get("KmsKeyId", "DefaultEncryptionKey"),
                rotation_enabled=secret_dict.get("RotationEnabled", False),
            )
            secret_list.append(secret)
        return secret_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Secret]
        """
        secret_list = self.recur_list_res(page_size=100, limit=limit)
        secret_list = list(sorted(
            secret_list, key=lambda r: r.name, reverse=True))
        return secret_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Secret]
        """
        secret_list = self.list_res(limit=1000)
        keys = [secret.name for secret in secret_list]
        mapper = {secret.name: secret for secret in secret_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_secret_list = fz_sr.match(query_str, limit=20)
        return matched_secret_list

    def to_item(self, secret):
        """
        :type secret: Secret
        :rtype: ItemArgs
        """
        console_url = secret.to_console_url()
        item_arg = ItemArgs(
            title="{secret_name}".format(
                secret_name=secret.name,
            ),
            subtitle=secret.description,
            autocomplete="{} {}".format(self.resource_id, secret.name),
            arg=console_url,
            largetext=secret.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(secret.arn)
        item_arg.copy_id(secret.id)
        return item_arg


secretmanager_secrets_searcher = SecretmanagerSecretsSearcher()
