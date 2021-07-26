# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from . import (
    set_profile,
    s3,
)
from workflow import Workflow3, ICON_ERROR

handler_func_mapper = {
    "select_profile": set_profile.select_profile,
    "set_profile": set_profile.set_profile,
    "select_region": set_profile.select_region,
    "set_region": set_profile.set_region,
    "s3_list_bucket": s3.list_bucket,
}

def handler(wf):
    """

    :type wf: Workflow3
    """
    try:
        key = wf.args[0]
    except Exception as e:
        wf.add_item(
            title="workflow arguments has to have at least one arg, as handler function key".format(),
            icon=ICON_ERROR
        )
        return wf

    if key not in handler_func_mapper:
        wf.add_item(
            title="'{}' is not a valid handler function key!".format(key),
            icon=ICON_ERROR
        )
        return wf

    return handler_func_mapper[key](wf)
