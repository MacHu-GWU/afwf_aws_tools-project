# -*- coding: utf-8 -*-

"""
Full text search module to support fuzzy search AWS main service and sub service.
powered by whoosh.
"""

from __future__ import unicode_literals
import shutil
from whoosh import fields, index, qparser, query
import yaml
from ..paths import (
    DIR_MAIN_SERVICE_INDEX, DIR_SUB_SERVICE_INDEX,
    PATH_CONSOLE_URLS_YAML,
)
from .aws_resource_filters import filter_func_mapper
from workflow.workflow3 import Item3


class MainServiceSchema(fields.SchemaClass):
    id = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    id_kw = fields.KEYWORD(stored=False)
    name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    short_name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    description = fields.STORED()
    url = fields.STORED()
    search_terms = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    globally = fields.BOOLEAN(stored=True)
    weight = fields.NUMERIC(
        sortable=True,
        stored=True,
    )
    top20 = fields.BOOLEAN(stored=True)
    has_sub_svc = fields.BOOLEAN(stored=True)


main_service_schema = MainServiceSchema()


class SubServiceSchema(fields.SchemaClass):
    id = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    id_kw = fields.KEYWORD(stored=False)
    name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    short_name = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
    )
    url = fields.STORED()
    weight = fields.NUMERIC(
        sortable=True,
        stored=True,
    )
    main_svc_id = fields.KEYWORD(stored=False)


sub_service_schema = SubServiceSchema()


def convert_unicode(dct, fields):
    for k in fields:
        if k in dct:
            dct[unicode(k)] = unicode(dct[k])


class Searcher(object):
    index_dir = None
    schema = None
    searchable_columns = list()

    def get_index(self):
        if self.index_dir.exists():
            idx = index.open_dir(self.index_dir.abspath)
        else:
            self.index_dir.mkdir()
            idx = index.create_in(dirname=self.index_dir.abspath, schema=self.schema)
        return idx

    def build_index(self):
        raise NotImplementedError


class MainServiceSearcher(Searcher):
    index_dir = DIR_MAIN_SERVICE_INDEX
    schema = main_service_schema
    searchable_columns = ["id", "name", "short_name", "search_terms"]

    def build_index(self, force_rebuild=False):
        """
        Build Whoosh Index, add document.
        """
        if force_rebuild:
            if DIR_MAIN_SERVICE_INDEX.exists():
                shutil.rmtree(DIR_MAIN_SERVICE_INDEX.abspath)
        if DIR_MAIN_SERVICE_INDEX.exists():
            return
        console_urls_data = yaml.load(PATH_CONSOLE_URLS_YAML.read_text(encoding="utf-8"), Loader=yaml.SafeLoader)
        idx = self.get_index()
        writer = idx.writer()

        for main_service_dict in console_urls_data:
            unicode_main_service_dict = dict()
            for k, v in main_service_dict.items():
                v = unicode(v) if isinstance(v, (str, unicode)) else v
                unicode_main_service_dict[unicode(k)] = v
            unicode_main_service_dict["id_kw"] = unicode_main_service_dict["id"]
            unicode_main_service_dict.setdefault("weight", 1)
            unicode_main_service_dict.setdefault("top20", False)
            if "search_terms" in unicode_main_service_dict:
                unicode_main_service_dict["search_terms"] = " ".join(main_service_dict["search_terms"])
            if "sub_services" in unicode_main_service_dict:
                del unicode_main_service_dict["sub_services"]
                unicode_main_service_dict["has_sub_svc"] = True
            else:
                unicode_main_service_dict["has_sub_svc"] = False
            writer.add_document(**unicode_main_service_dict)
        writer.commit()

    def top_20(self):
        q = query.Term("top20", True)
        idx = self.get_index()
        with idx.searcher() as searcher:
            result = [
                hit.fields()
                for hit in searcher.search(q, limit=20, sortedby="weight", reverse=True)
            ]
        return result

    def search_one(self, id):
        q = query.Term("id_kw", id)
        idx = self.get_index()
        with idx.searcher() as searcher:
            result = [
                hit.fields()
                for hit in searcher.search(q, limit=1)
            ]
        try:
            return result[0]
        except IndexError:
            return None

    def search(self, query_str, limit=20):
        """
        Use full text search for result.

        The ``query_str`` should be processed by Alfred Workflow handler
        """
        idx = self.get_index()
        q = qparser.MultifieldParser(
            self.searchable_columns,
            schema=self.schema,
        ).parse(query_str)
        with idx.searcher() as searcher:
            result = [
                hit.fields()
                for hit in searcher.search(q, limit=limit, sortedby="weight", reverse=True)
            ]

        ordered_result = list()
        to_append_result = list()
        for doc in result:
            if doc["id"].startswith(query_str):
                ordered_result.append(doc)
            else:
                to_append_result.append(doc)
        ordered_result.extend(to_append_result)
        return ordered_result


class SubServiceSearcher(Searcher):
    index_dir = DIR_SUB_SERVICE_INDEX
    schema = sub_service_schema
    searchable_columns = ["id", "name", "short_name"]

    def build_index(self, force_rebuild=False):
        """
        Build Whoosh Index, add document.
        """
        if force_rebuild:
            if DIR_SUB_SERVICE_INDEX.exists():
                shutil.rmtree(DIR_SUB_SERVICE_INDEX.abspath)
        if DIR_SUB_SERVICE_INDEX.exists():
            return
        console_urls_data = yaml.load(PATH_CONSOLE_URLS_YAML.read_text(encoding="utf-8"), Loader=yaml.SafeLoader)
        idx = self.get_index()
        writer = idx.writer()
        for main_service_dict in console_urls_data:
            if "sub_services" in main_service_dict:
                for sub_service_dict in main_service_dict["sub_services"]:
                    unicode_sub_service_dict = dict()
                    for k, v in sub_service_dict.items():
                        v = unicode(v) if isinstance(v, (str, unicode)) else v
                        unicode_sub_service_dict[unicode(k)] = v
                    unicode_sub_service_dict["main_svc_id"] = unicode(main_service_dict["id"])
                    unicode_sub_service_dict["id_kw"] = unicode_sub_service_dict["id"]
                    unicode_sub_service_dict.setdefault("weight", 1)
                    writer.add_document(**unicode_sub_service_dict)
        writer.commit()

    def top_20(self, main_svc_id):
        q = query.Term("main_svc_id", main_svc_id)
        idx = self.get_index()
        with idx.searcher() as searcher:
            result = [
                hit.fields()
                for hit in searcher.search(q, limit=100, sortedby="weight", reverse=True)
            ]
        return result

    def search_one(self, main_svc_id, id):
        q = query.And([
            query.Term("main_svc_id", main_svc_id),
            query.Term("id_kw", id),
        ])
        idx = self.get_index()
        with idx.searcher() as searcher:
            result = [
                hit.fields()
                for hit in searcher.search(q, limit=10)
            ]
        try:
            return result[0]
        except IndexError:
            return None

    def search(self, main_svc_id, query_str, limit=20):
        """
        Use full text search for result.

        The ``query_str`` should be processed by Alfred Workflow handler
        """
        idx = self.get_index()
        q = query.And([
            query.Term("main_svc_id", main_svc_id),
            qparser.MultifieldParser(
                self.searchable_columns,
                schema=self.schema,
            ).parse(query_str),
        ])
        with idx.searcher() as searcher:
            result = [
                hit.fields()
                for hit in searcher.search(q, limit=limit, sortedby="weight", reverse=True)
            ]
        ordered_result = list()
        to_append_result = list()
        for doc in result:
            if doc["id"].startswith(query_str):
                ordered_result.append(doc)
            else:
                to_append_result.append(doc)
        ordered_result.extend(to_append_result)
        return ordered_result


main_service_searcher = MainServiceSearcher()
sub_service_searcher = SubServiceSearcher()


def main_svc_doc_to_item(doc):
    """
    Convert main service document (dict) to alfred workflow item object.
    """
    title = doc["id"]
    subtitle = "{emoji}{name}{shortname}{description}".format(
        emoji="📂" if doc["has_sub_svc"] else "",
        name=doc["name"],
        shortname=" ({})".format(doc.get("short_name")) if doc.get("short_name") else "",
        description=" - {}".format(doc.get("description")) if doc.get("description") else "",
    )
    autocomplete = "{}-".format(doc["id"])
    arg = "https://console.aws.amazon.com" + doc["url"]
    return Item3(
        title=title,
        subtitle=subtitle,
        arg=arg,
        autocomplete=autocomplete,
        # icon=icon,
        valid=True,
    )


def sub_svc_doc_to_item(doc, main_svc_id):
    """
    Convert sub service document (dict) to alfred workflow item object.
    """
    title = "{}-{}".format(
        main_svc_id,
        doc["id"],
    )
    res_searcher_id = title
    subtitle = "{emoji}{name}{shortname}{description}".format(
        emoji="🔍" if res_searcher_id in filter_func_mapper else "",
        name=doc["name"],
        shortname=" ({})".format(doc.get("short_name")) if doc.get("short_name") else "",
        description=" - {}".format(doc.get("description")) if doc.get("description") else "",
    )
    autocomplete = "{}-{} ".format(
        main_svc_id,
        doc["id"],
    )
    arg = "https://console.aws.amazon.com" + doc["url"]
    return Item3(
        title=title,
        subtitle=subtitle,
        arg=arg,
        autocomplete=autocomplete,
        # icon=icon,
        valid=True,
    )
