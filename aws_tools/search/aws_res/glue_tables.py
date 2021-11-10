# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_tables
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...helpers import intersect, tokenize
from .glue_databases import Database, glue_databases_searcher


@attr.s(hash=True)
class Table(ResData):
    table_name = attr.ib()
    database_name = attr.ib()
    description = attr.ib()
    update_time = attr.ib()
    catalog_id = attr.ib()

    @property
    def full_name(self):
        return "{}.{}".format(self.database_name, self.table_name)

    @property
    def id(self):
        return self.full_name

    @property
    def key(self):
        return "{} {}".format(self.database_name, self.table_name)

    def to_console_url(self):
        return "https://console.aws.amazon.com/glue/home?region={region}#table:catalog={catalog_id};name={table_name};namespace={database_name}".format(
            catalog_id=self.catalog_id,
            database_name=self.database_name,
            table_name=self.table_name,
            region=SettingValues.aws_region
        )


class GlueTablesSearcher(AwsResourceSearcher):
    id = "glue-tables"

    limit_arg_name = "MaxResults"
    paginator_arg_name = "NextToken"

    def boto3_call(self, **kwargs):
        return self.sdk.glue_client.get_tables(**kwargs)

    def get_paginator(self, res):
        return res.get("NextToken")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of glue_client.get_tables

        :rtype: list[Table]
        """
        tb_list = list()
        for tb_dict in res["TableList"]:
            tb = Table(
                table_name=tb_dict["Name"],
                database_name=tb_dict["DatabaseName"],
                description=tb_dict.get("Description"),
                update_time=tb_dict["UpdateTime"],
                catalog_id=tb_dict["CatalogId"],
            )
            tb_list.append(tb)
        return tb_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        For searching glue table, the API requires the database name.
        So in this case we list the database name first and use the dot notation
        to search the table.

        :rtype: list[Database]
        """
        return glue_databases_searcher.list_res(limit=limit)

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[typing.Union[Database, Table]]
        """
        if "." in query_str:
            db_name, tb_name_query_str = query_str.split(".", 1)

            tb_name_query_str = tb_name_query_str.replace("-", " ").replace("_", " ")
            args = tokenize(tb_name_query_str)

            if len(args):
                tb_list_list = list()
                for arg in args:
                    tb_list = self.recur_list_res(
                        kwargs=dict(
                            DatabaseName=db_name,
                            Expression="*{}*".format(args)
                        ),
                        limit=100,
                    )
                    tb_list_list.append(tb_list)

                tb_list = intersect(*tb_list_list)
            else:
                tb_list = self.recur_list_res(
                    kwargs=dict(DatabaseName=db_name),
                    limit=100,
                )
            tb_list = list(sorted(tb_list, key=lambda tb: tb.full_name))
            return tb_list
        else:
            db_list = glue_databases_searcher.filter_res(query_str=query_str)
            return db_list

    def to_item(self, tb_or_db):
        """
        :type tb_or_db: typing.Union[Database, Table]
        :rtype: ItemArgs
        """
        if isinstance(tb_or_db, Database):
            db = tb_or_db
            console_url = db.to_console_url()
            item_arg = ItemArgs(
                title="🇩 Database({db_name})".format(
                    db_name=db.name,
                ),
                subtitle="{description}".format(
                    description=db.description
                ),
                autocomplete="{} {}.".format(self.resource_id, db.name),
                arg=console_url,
                largetext=tb_or_db.to_large_text(),
                icon=self.icon,
                valid=True,
            )
            item_arg.open_browser(console_url)
            item_arg.copy_id(tb_or_db.id)
        elif isinstance(tb_or_db, Table):
            tb = tb_or_db
            console_url = tb.to_console_url()
            item_arg = ItemArgs(
                title="🇹 Table({full_name})".format(full_name=tb.full_name),
                subtitle="{description}".format(
                    description=tb.description
                ),
                autocomplete="{} {}".format(self.resource_id, tb.full_name),
                arg=console_url,
                largetext=tb_or_db.to_large_text(),
                icon=self.icon,
                valid=True,
            )
            item_arg.open_browser(console_url)
            item_arg.copy_id(tb_or_db.id)
        else:
            raise Exception
        return item_arg

glue_tables_searcher = GlueTablesSearcher()
