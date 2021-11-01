# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_databases
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...cache import cache
from ...search.fuzzy import FuzzyObjectSearch
from ...settings import SettingValues


@attr.s
class Database(object):
    name = attr.ib()
    description = attr.ib()
    create_time = attr.ib()
    catalog_id = attr.ib()
    location_uri = attr.ib()

    def to_console_url(self):
        return "https://console.aws.amazon.com/glue/home?region={region}#database:catalog={catalog_id};name={database_name}".format(
            catalog_id=self.catalog_id,
            database_name=self.name,
            region=SettingValues.aws_region
        )

    def to_largetext(self):
        return "\n".join([
            "name = {}".format(self.name),
            "description = {}".format(self.description),
            "create_time = {}".format(self.create_time),
            "catalog_id = {}".format(self.catalog_id),
            "location_uri = {}".format(self.location_uri),
        ])


def simplify_get_databases_response(res):
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


class GlueDatabasesSearcher(AwsResourceSearcher):
    id = "glue-databases"
    cache_key = "aws-res-glue-databases"

    def get_databases_dict(self):
        """
        :rtype: list[dict]
        """
        databases = list()
        next_token = None
        while 1:
            kwargs = dict(
                MaxResults=1000,
            )
            if next_token:
                kwargs["NextToken"] = next_token
            res = self.sdk.glue_client.get_databases(**kwargs)
            databases.extend(res.get("DatabaseList", list()))
            next_token = res.get("NextToken", None)
            if not next_token:
                break
        merged_res = {"DatabaseList": databases}
        db_list = simplify_get_databases_response(merged_res)
        db_dict_list = [
            attr.asdict(db)
            for db in db_list
        ]
        db_dict_list = list(sorted(
            db_dict_list, key=lambda x: x["create_time"], reverse=True))
        return db_dict_list

    def list_res(self):
        """
        :rtype: list[Database]
        """
        db_dict_list = cache.fast_get(
            key=self.cache_key,
            callable=self.get_databases_dict,
            expire=10,
        )
        db_list = [
            Database(**db_dict)
            for db_dict in db_dict_list
        ]
        db_list = list(sorted(db_list, key=lambda tb: tb.name))
        return db_list

    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Database]
        """
        db_list = self.list_res()
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
        largetext = db.to_largetext()
        item_arg = ItemArgs(
            title="{db_name}".format(
                db_name=db.name,
            ),
            subtitle="{description}".format(
                description=db.description
            ),
            autocomplete="{} {}".format(self.resource_id, db.name),
            arg=console_url,
            largetext=largetext,
            icon=find_svc_icon(self.id),
            valid=True,
        )
        item_arg.open_browser(console_url)
        return item_arg
