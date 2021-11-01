# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import yaml
from pathlib_mate import Path

p_console_urls_yml = Path(__file__).change(new_basename="console-urls.yml")
p_console_urls_dump_yml = Path(__file__).change(new_basename="console-urls-dump.yml")


def sort_by_ids():
    """
    This method has to be called in Python3.8 because dict is ordered.
    """
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
    main_dict_list = yaml.load(p_console_urls_yml.read_text(), Loader=yaml.SafeLoader) # type: list[dict]
    new_main_dict_list = list()
    for main_dict in main_dict_list:
        sub_dict_list = list()
        for sub_dict in main_dict.get("sub_services", list()):
            sub_dict = to_od(sub_dict, sub_svc_ordered_keys)
            if "{region}" not in sub_dict["url"]:
                print(sub_dict["url"])
            sub_dict_list.append(sub_dict)
            sub_dict_list = list(sorted(sub_dict_list, key=lambda d: d["id"]))
        main_dict["sub_services"] = sub_dict_list
        main_dict = to_od(main_dict, main_svc_ordered_keys)
        if "{region}" not in main_dict["url"]:
            print(main_dict["url"])
        new_main_dict_list.append(main_dict)
    new_main_dict_list = list(sorted(new_main_dict_list, key=lambda d: d["id"]))
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
    sort_by_ids()
    # show_main_svc_ids()
    # show_sub_svc_ids()
    pass
