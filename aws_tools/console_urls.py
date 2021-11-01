# -*- coding: utf-8 -*-

"""
The data class for the main service and sub service struct data.
"""

from __future__ import unicode_literals
import attr
import yaml
from .attrs_helper import Base
from .paths import PATH_CONSOLE_URLS_YAML


@attr.s
class MainService(Base):
    id = attr.ib()
    name = attr.ib()
    url = attr.ib()
    search_terms = attr.ib(factory=list)
    globally = attr.ib(default=False)
    weight = attr.ib(default=1)
    top20 = attr.ib(default=False)
    short_name = attr.ib(default=None)
    description = attr.ib(default=None)
    sub_services = attr.ib(factory=list)  # type: list[SubService]


@attr.s
class SubService(Base):
    id = attr.ib()
    name = attr.ib()
    url = attr.ib()
    short_name = attr.ib(default=None)
    weight = attr.ib(default=1)


def load_console_urls_yaml():
    """
    Load :class:`MainService` object from yaml.

    :rtype: list[MainService]
    """
    data = yaml.load(
        PATH_CONSOLE_URLS_YAML.read_text(), Loader=yaml.SafeLoader)
    main_svc_list = list()
    for main_dict in data:
        sub_services = list()
        for sub_dict in main_dict.get("sub_services", list()):
            sub_svc = SubService(**sub_dict)
            sub_services.append(sub_svc)
        main_dict["sub_services"] = sub_services
        print(main_dict.keys())
        main_svc = MainService(**main_dict)
        main_svc_list.append(main_svc)

    return main_svc_list


def sort_by_ids():
    """
    Rebuild the yaml file, Sort main service and sub service by its id.
    """
    from .paths import PATH_CONSOLE_URLS_TEMP_YAML

    def to_od(dct, ordered_keys):
        """
        :type dct: dict
        :type ordered_keys: list
        """
        od = dict()
        for k in ordered_keys:
            if k in dct:
                od[k] = dct[k]
        return od

    main_svc_ordered_keys = "id,name,short_name,description,url,globally,weight,top20,sub_services".split(",")
    sub_svc_ordered_keys = "id,name,short_name,url,weight".split(",")

    main_svc_list = load_console_urls_yaml()
    main_dict_list = list()
    for main_svc in main_svc_list:
        main_dict = main_svc.to_dict()
        sub_dict_list = list()
        for sub_svc in main_svc.sub_services:
            sub_dict = sub_svc.to_dict()
            sub_dict = to_od(sub_dict, sub_svc_ordered_keys)
            sub_dict_list.append(sub_dict)
        main_dict["sub_services"] = list(sorted(
            sub_dict_list, key=lambda d: d["id"]))
        main_dict = to_od(main_dict, main_svc_ordered_keys)
        main_dict_list.append(main_dict)
    main_dict_list = list(sorted(main_dict_list, key=lambda d: d["id"]))

    PATH_CONSOLE_URLS_TEMP_YAML.write_text(yaml.dump(main_dict_list, sort_keys=False))
