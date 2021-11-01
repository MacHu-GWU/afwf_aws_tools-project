# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_tables
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...settings import SettingValues
from .glue_databases import Database, GlueDatabasesSearcher

glue_db_searcher = GlueDatabasesSearcher()


@attr.s
class Table(object):
    table_name = attr.ib()
    database_name = attr.ib()
    description = attr.ib()
    update_time = attr.ib()
    catalog_id = attr.ib()

    @property
    def full_name(self):
        return "{}.{}".format(self.database_name, self.table_name)

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

    def to_largetext(self):
        return "\n".join([
            "table_name = {}".format(self.table_name),
            "database_name = {}".format(self.database_name),
            "description = {}".format(self.description),
            "update_time = {}".format(self.update_time),
            "catalog_id = {}".format(self.catalog_id),
        ])


def simplify_get_tables_response(res):
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


class GlueTablesSearcher(AwsResourceSearcher):
    id = "glue-tables"
    cache_key = "aws-res-glue-tables"

    def get_tables_dict(self, database, query_str):
        """
        :rtype: list[dict]
        """
        tables = list()
        next_token = None
        while 1:
            kwargs = dict(
                DatabaseName=database,
                MaxResults=1000,
            )
            if query_str:
                kwargs["Expression"] = "*{}*".format(query_str)
            if next_token:
                kwargs["NextToken"] = next_token
            res = self.sdk.glue_client.get_tables(**kwargs)
            tables.extend(res.get("TableList", list()))
            next_token = res.get("NextToken", None)
            if not next_token:
                break
        merged_res = {"TableList": tables}
        tb_list = simplify_get_tables_response(merged_res)
        tb_dict_list = [
            attr.asdict(db)
            for db in tb_list
        ]
        tb_dict_list = list(sorted(
            tb_dict_list, key=lambda x: x["update_time"], reverse=True))
        return tb_dict_list

    def list_res(self):
        """
        For searching glue table, the API requires the database name.
        So in this case we list the database name first and use the dot notation
        to search the table.

        :rtype: list[Database]
        """
        return glue_db_searcher.list_res()

    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[typing.Union[Database, Table]]
        """
        if "." in query_str:
            db_name, tb_name_query_str = query_str.split(".", 1)
            tb_dict_list = self.get_tables_dict(database=db_name, query_str=tb_name_query_str)
            tb_list = [Table(**tb_dict) for tb_dict in tb_dict_list]
            tb_list = list(sorted(
                tb_list, key=lambda tb: tb.table_name))
            return tb_list
        else:
            db_list = glue_db_searcher.filter_res(query_str=query_str)
            return db_list

    def to_item(self, tb_or_db):
        """
        :type tb_or_db: typing.Union[Database, Table]
        :rtype: ItemArgs
        """
        if isinstance(tb_or_db, Database):
            db = tb_or_db
            console_url = db.to_console_url()
            largetext = db.to_largetext()
            item_arg = ItemArgs(
                title="{db_name}".format(
                    db_name=db.name,
                ),
                subtitle="{description}".format(
                    description=db.description
                ),
                autocomplete="{} {}.".format(self.resource_id, db.name),
                arg=console_url,
                largetext=largetext,
                icon=find_svc_icon(self.id),
                valid=True,
            )
            item_arg.open_browser(console_url)
        elif isinstance(tb_or_db, Table):
            tb = tb_or_db
            console_url = tb.to_console_url()
            largetext = tb.to_largetext()
            item_arg = ItemArgs(
                title=tb.full_name,
                subtitle="{description}".format(
                    description=tb.description
                ),
                autocomplete="{} {}".format(self.resource_id, tb.full_name),
                arg=console_url,
                largetext=largetext,
                icon=find_svc_icon(self.id),
                valid=True,
            )
            item_arg.open_browser(console_url)
        else:
            raise Exception
        return item_arg
