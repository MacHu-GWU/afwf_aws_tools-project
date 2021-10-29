# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import traceback
from workflow import Workflow3, ICON_ERROR, ICON_HELP

from . import (
    aws,
    aws_profile,
    # s3,
)
from .aws_profile import aws_profile_handlers

handler_func_mapper = {
    aws_profile_handlers.select_aws_profile.__name__: aws_profile_handlers.select_aws_profile,
    # set_profile.set_default_profile.__name__: set_profile.aws_set_default_profile,
    aws.aws.__name__: aws.aws,

    # aws_profile.set_profile.__name__: aws_profile.set_profile,
    # aws_profile.select_region.__name__: aws_profile.select_region,
    # aws_profile.set_region.__name__: aws_profile.set_region,
    # aws_profile.mfa_auth_select_profile.__name__: aws_profile.mfa_auth_select_profile,
    # aws_profile.mfa_auth_execute_mfa.__name__: aws_profile.mfa_auth_execute_mfa,
    # s3.list_bucket.__name__: s3.list_bucket,
}


def debug_args(wf):
    wf.add_item(
        title="args = {}".format(wf.args),
        icon=ICON_HELP,
        valid=True,
    )


def debug_traceback(wf):
    lines = traceback.format_exc().splitlines()
    for line in lines:
        wf.add_item(
            title=line,
            arg=line,
            icon=ICON_ERROR,
            valid=True,
        )
    return wf


def handler(wf):
    """
    Main handler that pass down argument to all other handler functions.

    handler function is a simple python function takes two arguments:

    1. wf
    2. query_str
    """
    if wf.args != 1:
        wf.add_item(
            title="Workflow arguments has to have exact one arg!",
            subtitle="correct format = '${handler_id} ${query_str}'",
            icon=ICON_ERROR,
            valid=True,
        )

    arg = wf.args[0]
    if " " not in arg:
        wf.add_item(
            title="Invalid workflow arguments",
            subtitle="correct format = '${handler_id} ${query_str}'",
            icon=ICON_ERROR,
            valid=True,
        )

    handler_id, query_str = arg.split(" ")
    query_str = query_str.lstrip()

    if handler_id not in handler_func_mapper:
        wf.add_item(
            title="'{}' is not a valid handler identifier!".format(handler_id),
            icon=ICON_ERROR,
            valid=True,
        )

    try:
        return handler_func_mapper[handler_id](wf, query_str)
    except:  # capture exceptions in handler function and display in alfred UI
        debug_traceback(wf)

    debug_args(wf)
    return wf
