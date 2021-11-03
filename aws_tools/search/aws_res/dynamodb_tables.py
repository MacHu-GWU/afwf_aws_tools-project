# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_tables
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Table(ResData):
    name = attr.ib()

    @property
    def id(self):
        return self.name

    @property
    def arn(self):
        return "arn:aws:dynamodb:{region}:{account_id}:table/{table_name}".format(
            table_name=self.name,
            region=SettingValues.aws_region,
            account_id=AwsResourceSearcher.sdk.account_id,
        )

    def to_console_url(self):
        return "https://console.aws.amazon.com/dynamodbv2/home?region={region}#table?initialTableGroup=%23all&initialTagKey=&name={table_name}".format(
            table_name=self.name,
            region=SettingValues.aws_region,
        )


class DynamodbTablesSearcher(AwsResourceSearcher):
    id = "dynamodb-tables"
    limit_arg_name = "Limit"
    paginator_arg_name = "ExclusiveStartTableName"

    def boto3_call(self, **kwargs):
        return self.sdk.dynamodb_client.list_tables(**kwargs)

    def get_paginator(self, res):
        return res.get("NextMarker")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of dynamodb_client.list_tables

        :rtype: list[Table]
        """
        table_list = list()
        for table_name in res["TableNames"]:
            table = Table(
                name=table_name,
            )
            table_list.append(table)
        return table_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Table]
        """
        table_list = self.recur_list_res(page_size=100, limit=limit)
        table_list = list(sorted(
            table_list, key=lambda r: r.name, reverse=True))
        return table_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Table]
        """
        table_list = self.list_res(limit=1000)
        keys = [table.name for table in table_list]
        mapper = {table.name: table for table in table_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_table_list = fz_sr.match(query_str, limit=20)
        return matched_table_list

    def to_item(self, table):
        """
        :type table: Table
        :rtype: ItemArgs
        """
        console_url = table.to_console_url()
        item_arg = ItemArgs(
            title="{table_name}".format(
                table_name=table.name,
            ),
            subtitle=table.arn,
            autocomplete="{} {}".format(self.resource_id, table.name),
            arg=console_url,
            largetext=table.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(table.arn)
        return item_arg


dynamodb_tables_searcher = DynamodbTablesSearcher()
