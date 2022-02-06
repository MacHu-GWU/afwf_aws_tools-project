# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_tables
"""

from __future__ import unicode_literals
from ..aws_resources import ItemArgs
from ...icons import find_svc_icon
from ...settings import SettingValues
from .lakeformation_databases import to_console_url as to_db_console_url
from .glue_tables import Database, Table, GlueTablesSearcher


def to_tb_console_url(tb):
    return "https://{domain}/lakeformation/home?region={region}#table-details/{database_name}/{table_name}?catalogId={catalog_id}".format(
        domain=SettingValues.get_console_domain(),
        catalog_id=tb.catalog_id,
        database_name=tb.database_name,
        table_name=tb.table_name,
        region=SettingValues.aws_region
    )


class LakeformationTablesSearcher(GlueTablesSearcher):
    id = "lakeformation-tables"

    def to_item(self, tb_or_db):
        """
        :type tb_or_db: typing.Union[Database, Table]
        :rtype: ItemArgs
        """
        item_arg = super(LakeformationTablesSearcher, self).to_item(tb_or_db)
        if isinstance(tb_or_db, Database):
            console_url = to_db_console_url(tb_or_db)
        elif isinstance(tb_or_db, Table):
            console_url = to_tb_console_url(tb_or_db)
        else:
            raise Exception
        item_arg.icon = find_svc_icon(self.id)
        item_arg.open_browser(console_url)
        item_arg.copy_id(tb_or_db.id)
        return item_arg

lakeformation_tables_searcher = LakeformationTablesSearcher()
