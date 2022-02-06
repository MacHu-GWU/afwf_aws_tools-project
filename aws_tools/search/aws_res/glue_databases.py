# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_databases
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Database(ResData):
    name = attr.ib()
    description = attr.ib()
    create_time = attr.ib()
    catalog_id = attr.ib()
    location_uri = attr.ib()

    @property
    def id(self):
        return self.name

    def to_console_url(self):
        return "https://{domain}/glue/home?region={region}#database:catalog={catalog_id};name={database_name}".format(
            domain=SettingValues.get_console_domain(),
            catalog_id=self.catalog_id,
            database_name=self.name,
            region=SettingValues.aws_region
        )


class GlueDatabasesSearcher(AwsResourceSearcher):
    id = "glue-databases"
    limit_arg_name = "MaxResults"
    paginator_arg_name = "NextToken"
    
    def boto3_call(self, **kwargs):
        return self.sdk.glue_client.get_databases(**kwargs)

    def get_paginator(self, res):
        return res.get("NextToken")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of glue_client.get_databases

        :rtype: list[Database]
        """
        db_list = list()
        for db_dict in res["DatabaseList"]:
            db = Database(
                name=db_dict["Name"],
                description=db_dict.get("Description"),
                create_time=str(db_dict["CreateTime"]),
                catalog_id=db_dict["CatalogId"],
                location_uri=db_dict.get("LocationUri"),
            )
            db_list.append(db)
        return db_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Database]
        """
        db_list = self.recur_list_res(limit=limit)
        db_list = list(sorted(
            db_list, key=lambda r: r.name, reverse=True))
        return db_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Database]
        """
        db_list = self.list_res(limit=1000)
        keys = [db.name for db in db_list]
        mapper = {db.name: db for db in db_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_db_list = fz_sr.match(query_str, limit=20)
        return matched_db_list

    def to_item(self, db):
        """
        :type db: Database
        :rtype: ItemArgs
        """
        console_url = db.to_console_url()
        item_arg = ItemArgs(
            title="🇩 Database({db_name})".format(
                db_name=db.name,
            ),
            subtitle="{description}".format(
                description=db.description
            ),
            autocomplete="{} {}".format(self.resource_id, db.name),
            arg=console_url,
            largetext=db.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_id(db.id)
        return item_arg


glue_databases_searcher = GlueDatabasesSearcher()
