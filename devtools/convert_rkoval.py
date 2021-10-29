# -*- coding: utf-8 -*-

"""

Main service:

- id (required): str
- name (required): str
- short_name: str
- description: str
- url (required): str
- search_terms: list[str]
- globally: bool
- sub_services: list()

Sub service:

- id (required): str
- name (required):
- url (required):
"""

import yaml
from pathlib_mate import Path
from collections import OrderedDict

p_rkoval_console_services = Path(__file__).change(new_basename="console-services.yml")
p_sanhe_aws_console_urls = Path(__file__).change(new_basename="console-urls.yml")

rkoval_console_services_data = yaml.load(p_rkoval_console_services.read_text(), Loader=yaml.SafeLoader)

#--- Explore the rkoval dataset ---
# main_service_fields = set()
# sub_service_fields = set()
# for main_service_dict in rkoval_console_services_data:
#     main_service_fields.update(set(main_service_dict.keys()))
#     for sub_service_dict in main_service_dict.get("sub_services", []):
#         sub_service_fields.update(set(sub_service_dict.keys()))
#
# print(main_service_fields)
# print(sub_service_fields)

#--- convert to sanhe dataset ---
main_service_mapper = OrderedDict([
    ("id", "id"),
    ("name", "name"),
    ("short_name", "short_name"),
    ("description", "description"),
    ("url", "url"),
    ("search_terms", "extra_search_terms"),
    ("globally", "has_global_region"),
])
sub_service_mapper = OrderedDict([
    ("id", "id"),
    ("name", "name"),
    ("url", "url"),
])

sanhe_aws_console_urls_data = list()
for main_service_dict in rkoval_console_services_data:
    sanhe_main_service_dict = dict()
    for sanhe, rkoval in main_service_mapper.items():
        if rkoval in main_service_dict:
            sanhe_main_service_dict[sanhe] = main_service_dict[rkoval]
    sub_services = list()
    for sub_service_dict in main_service_dict.get("sub_services", []):
        sanhe_sub_service_dict = dict()
        for sanhe, rkoval in sub_service_mapper.items():
            if rkoval in sub_service_dict:
                sanhe_sub_service_dict[sanhe] = sub_service_dict[rkoval]
        if len(sanhe_sub_service_dict):
            sub_services.append(sanhe_sub_service_dict)
    if len(sub_services):
        sanhe_main_service_dict["sub_services"] = sub_services
    if len(sanhe_main_service_dict):
        sanhe_aws_console_urls_data.append(sanhe_main_service_dict)

p_sanhe_aws_console_urls.write_bytes(
    yaml.dump(sanhe_aws_console_urls_data)
)
#
# sanhe_main_service_dict = OrderedDict()
