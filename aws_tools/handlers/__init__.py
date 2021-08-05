# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from . import (
    set_profile,
    s3,
)
from workflow import Workflow3, ICON_ERROR

handler_func_mapper = {
    set_profile.select_profile.__name__: set_profile.select_profile,
    set_profile.set_profile.__name__: set_profile.set_profile,
    set_profile.select_region.__name__: set_profile.select_region,
    set_profile.set_region.__name__: set_profile.set_region,
    set_profile.set_default_profile.__name__: set_profile.set_default_profile,
    set_profile.mfa_auth_select_profile.__name__: set_profile.mfa_auth_select_profile,
    set_profile.mfa_auth_execute_mfa.__name__: set_profile.mfa_auth_execute_mfa,
    s3.list_bucket.__name__: s3.list_bucket,
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
