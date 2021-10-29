# -*- coding: utf-8 -*-

from __future__ import print_function
from . import (
    ec2
)

filter_func_mapper = {
    "ec2-instances": ec2.instances,
}


def filter_resources(res_searcher_id, query_str):
    """
    :rtype: list[workflow.workflow3.Item3]
    :return:
    """
    return filter_func_mapper[res_searcher_id](query_str)
