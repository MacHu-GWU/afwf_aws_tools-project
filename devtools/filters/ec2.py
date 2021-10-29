# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json
from aws_tools.handlers.aws_resource_filters import filter_resources, ec2

def jprint_items(items):
    for item in items:
        print(item.obj)

jprint_items(filter_resources(res_searcher_id="ec2-instances", query_str=None))
# pprint(ec2.instances(None))
