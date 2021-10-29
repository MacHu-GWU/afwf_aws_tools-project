# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import traceback
from workflow import Workflow3, ICON_ERROR

from . import (
    aws,
    set_profile,
    # s3,
)

handler_func_mapper = {
    aws.aws.__name__: aws.aws,
    set_profile.select_profile.__name__: set_profile.select_profile,
    set_profile.set_profile.__name__: set_profile.set_profile,
    set_profile.select_region.__name__: set_profile.select_region,
    set_profile.set_region.__name__: set_profile.set_region,
    set_profile.set_default_profile.__name__: set_profile.set_default_profile,
    set_profile.mfa_auth_select_profile.__name__: set_profile.mfa_auth_select_profile,
    set_profile.mfa_auth_execute_mfa.__name__: set_profile.mfa_auth_execute_mfa,
    # s3.list_bucket.__name__: s3.list_bucket,
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

    try:
        return handler_func_mapper[key](wf)
    except: # 对于 handler 级别的错误, 捕捉异常并展现之
        wf._items = []
        lines = traceback.format_exc().splitlines()
        for line in lines:
            wf.add_item(title=line, arg=line, icon=ICON_ERROR)
        return wf
