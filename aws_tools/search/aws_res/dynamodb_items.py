# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_tables
"""

from __future__ import unicode_literals
from ..aws_resources import ItemArgs
from ...settings import SettingValues
from .dynamodb_tables import DynamodbTablesSearcher


def to_console_url(tb):
    return "https://{domain}/dynamodbv2/home?region={region}#item-explorer?initialTagKey=&table={table_name}".format(
        domain=SettingValues.get_console_domain(),
        table_name=tb.name,
        region=SettingValues.aws_region,
    )


class DynamodbItemsSearcher(DynamodbTablesSearcher):
    id = "dynamodb-items"

    def to_item(self, table):
        """
        :type table: Table
        :rtype: ItemArgs
        """
        item_args = super(DynamodbItemsSearcher, self).to_item(table)
        console_url = to_console_url(table)
        item_args.arg = console_url
        item_args.open_browser(console_url)
        return item_args


dynamodb_items_searcher = DynamodbItemsSearcher()
