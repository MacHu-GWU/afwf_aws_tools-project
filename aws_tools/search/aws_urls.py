# -*- coding: utf-8 -*-

"""
Full text search module to support fuzzy search AWS main service and sub service.
powered by whoosh.
"""

from __future__ import unicode_literals
import attr
import typing
import shutil
import yaml
from whoosh import fields, qparser, query, sorting
from .fts import FtsSearcher
from ..paths import (
    DIR_MAIN_SERVICE_INDEX, DIR_SUB_SERVICE_INDEX,
    PATH_MAIN_SERVICE_INDEX_LOCK, PATH_SUB_SERVICE_INDEX_LOCK,
    PATH_CONSOLE_URLS_YAML,
)


@attr.s
class MainService(object):
    id = attr.ib()
    name = attr.ib()
    short_name = attr.ib()
    description = attr.ib()
    url = attr.ib()
    search_terms = attr.ib()
    globally = attr.ib()
    weight = attr.ib()
    top20 = attr.ib()
    has_sub_svc = attr.ib()


class MainServiceSchema(fields.SchemaClass):
    id = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
        sortable=True,
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


@attr.s
class SubService(object):
    id = attr.ib()
    name = attr.ib()
    short_name = attr.ib()
    url = attr.ib()
    weight = attr.ib()
    main_svc_id = attr.ib()


class SubServiceSchema(fields.SchemaClass):
    id = fields.NGRAM(
        minsize=2,
        maxsize=10,
        stored=True,
        sortable=True,
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
    main_svc_id = fields.KEYWORD(stored=True)


sub_service_schema = SubServiceSchema()


def convert_unicode(dct, fields):
    for k in fields:
        if k in dct:
            dct[unicode(k)] = unicode(dct[k])


class MainServiceSearcher(FtsSearcher):
    """

    """

    def __init__(self):
        super(MainServiceSearcher, self).__init__(
            schema=main_service_schema,
            index_dir=DIR_MAIN_SERVICE_INDEX,
        )

    def build_index(self, force_rebuild=False):
        """
        Build Whoosh Index, add document.

        :type force_rebuild: bool
        """
        if force_rebuild:
            if self.index_dir.exists():
                shutil.rmtree(self.index_dir.abspath)
        if self.index_dir.exists():
            return

        console_urls_data = yaml.load(
            PATH_CONSOLE_URLS_YAML.read_text(encoding="utf-8"),
            Loader=yaml.SafeLoader,
        )
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
                if unicode_main_service_dict["sub_services"]:
                    unicode_main_service_dict["has_sub_svc"] = True
                else:
                    unicode_main_service_dict["has_sub_svc"] = False
                del unicode_main_service_dict["sub_services"]
            else:
                unicode_main_service_dict["has_sub_svc"] = False
            writer.add_document(**unicode_main_service_dict)
        writer.commit()

    def build_index_if_not_exists(self):
        if not PATH_MAIN_SERVICE_INDEX_LOCK.exists():
            self.build_index(force_rebuild=True)

    def search_one(self, id):
        """
        :type id: str
        :param id: main service id
        :rtype: typing.Union[dict, None]
        """
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

    def top_20(self):
        """
        :rtype: list[dict]
        """
        self.build_index_if_not_exists()
        q = query.Term("top20", True)
        idx = self.get_index()
        mf = sorting.MultiFacet()
        mf.add_field("weight", reverse=True)
        mf.add_field("id")
        with idx.searcher() as searcher:
            result = [
                hit.fields()
                for hit in searcher.search(q, sortedby=mf, limit=20)
            ]
        return result

    def search(self, query_str, limit=20):
        """
        Use full text search for result.

        The ``query_str`` should be pre-processed by Alfred Workflow handler

        :type query_str: str
        :type limit: int
        :rtype: list[dict]
        """
        q = qparser.MultifieldParser(
            ["id", "name", "short_name", "search_terms"],
            schema=self.schema,
        ).parse(query_str)
        idx = self.get_index()
        mf = sorting.MultiFacet()
        mf.add_field("weight", reverse=True)
        mf.add_field("id")
        with idx.searcher() as searcher:
            result = [
                hit.fields()
                for hit in searcher.search(q, sortedby=mf, limit=limit)
            ]

        # if the "id" starts with the query str, prioritize it
        ordered_result = list()
        to_append_result = list()
        for doc in result:
            if doc["id"].startswith(query_str):
                ordered_result.append(doc)
            else:
                to_append_result.append(doc)
        ordered_result.extend(to_append_result)
        return ordered_result


class SubServiceSearcher(FtsSearcher):
    """

    """

    def __init__(self):
        super(SubServiceSearcher, self).__init__(
            schema=sub_service_schema,
            index_dir=DIR_SUB_SERVICE_INDEX,
        )

    def build_index(self, force_rebuild=False):
        """
        Build Whoosh Index, add document.

        :type force_rebuild: bool
        """
        if force_rebuild:
            if self.index_dir.exists():
                shutil.rmtree(self.index_dir.abspath)
        if self.index_dir.exists():
            return
        console_urls_data = yaml.load(
            PATH_CONSOLE_URLS_YAML.read_text(encoding="utf-8"),
            Loader=yaml.SafeLoader
        )
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

    def build_index_if_not_exists(self):
        if not PATH_SUB_SERVICE_INDEX_LOCK.exists():
            self.build_index(force_rebuild=True)

    def search_one(self, main_svc_id, sub_svc_id):
        """
        :type main_svc_id: str
        :param sub_svc_id: main service id

        :type sub_svc_id: str
        :param id: sub service id,

        :rtype: typing.Union[dict, None]
        """
        q = query.And([
            query.Term("main_svc_id", main_svc_id),
            query.Term("id_kw", sub_svc_id),
        ])
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

    def top_20(self, main_svc_id):
        """
        :type main_svc_id: str
        :param main_svc_id: main service id

        :rtype: list[dict]
        """
        self.build_index_if_not_exists()
        q = query.Term("main_svc_id", main_svc_id)
        idx = self.get_index()
        mf = sorting.MultiFacet()
        mf.add_field("weight", reverse=True)
        mf.add_field("id")
        with idx.searcher() as searcher:
            result = [
                hit.fields()
                for hit in searcher.search(q, sortedby=mf, limit=20)
            ]
        return result

    def search(self, main_svc_id, query_str, limit=20):
        """
        Use full text search for result.

        The ``query_str`` should be processed by Alfred Workflow handler.

        :type main_svc_id: str
        :type query_str: str
        :type limit: int
        :rtype: list[dict]
        """
        idx = self.get_index()
        q = query.And([
            query.Term("main_svc_id", main_svc_id),
            qparser.MultifieldParser(
                ["id", "name", "short_name"],
                schema=self.schema,
            ).parse(query_str),
        ])
        mf = sorting.MultiFacet()
        mf.add_field("weight", reverse=True)
        mf.add_field("id")
        with idx.searcher() as searcher:
            result = [
                hit.fields()
                for hit in searcher.search(q, sortedby=mf, limit=limit)
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
