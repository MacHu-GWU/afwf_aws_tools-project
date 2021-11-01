# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import yaml
from pathlib_mate import Path
from collections import OrderedDict

p_console_urls_yml = Path(__file__).change(new_basename="console-urls.yml")
p_console_urls_dump_yml = Path(__file__).change(new_basename="console-urls-dump.yml")

main_dict_list = yaml.load(p_console_urls_yml.read_text(), Loader=yaml.SafeLoader)


def sort_ids():
    """
    Since in python3.6 dict key value are ordered, please use python3.6+ to run
    this!

    python3.8 console_urls_helper.py
    """
    main_svc_ordered_keys = "id,name,short_name,description,url,globally,weight,top20,sub_services".split(",")
    sub_svc_ordered_keys = "id,name,url,weight".split(",")

    def to_od(dct, ordered_keys):
        od = dict()
        for k in ordered_keys:
            if k in dct:
                od[k] = dct[k]
        return od

    for main_dict in main_dict_list:
        sub_dict_list = main_dict.get("sub_services", list())
        sub_dict_list = [to_od(d, sub_svc_ordered_keys) for d in sub_dict_list]
        main_dict["sub_services"] = list(sorted(
            sub_dict_list, key=lambda d: d["id"]))
    new_main_dict_list = [to_od(d, main_svc_ordered_keys) for d in main_dict_list]
    new_main_dict_list = list(sorted(
        new_main_dict_list, key=lambda d: d["id"]
    ))
    p_console_urls_dump_yml.write_text(yaml.dump(new_main_dict_list, sort_keys=False))


def show_main_svc_ids():
    for main_dict in main_dict_list:
        id = main_dict["id"]
        print(id)


def show_sub_svc_ids():
    for main_dict in main_dict_list:
        main_id = main_dict["id"]
        for sub_dict in main_dict.get("sub_services", []):
            print("{}-{}".format(main_id, sub_dict["id"]))


if __name__ == "__main__":
    # sort_ids()
    # show_main_svc_ids()
    show_sub_svc_ids()
    pass
