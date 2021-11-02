# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_databases
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch
from .glue_databases import Database, GlueDatabasesSearcher


def to_console_url(db):
    """
    :type db: Database
    :rtype: str
    """
    return "https://console.aws.amazon.com/lakeformation/home?region={region}#database-details/{database_name}?catalogId={catalog_id}".format(
        catalog_id=db.catalog_id,
        database_name=db.name,
        region=SettingValues.aws_region
    )


class LakeformationDatabasesSearcher(GlueDatabasesSearcher):
    id = "lakeformation-databases"

    def to_item(self, db):
        """
        :type db: Database
        :rtype: ItemArgs
        """
        item_arg = super(LakeformationDatabasesSearcher, self).to_item(db)
        console_url = to_console_url(db)
        item_arg.arg = console_url
        item_arg.icon = find_svc_icon(self.id)
        item_arg.open_browser(console_url)
        return item_arg


lakeformation_databases_searcher = LakeformationDatabasesSearcher()
