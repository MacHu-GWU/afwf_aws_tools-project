# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import traceback
from workflow import Workflow3

from ..icons import HotIcons
from ..register import Registry
from ..alfred import ItemArgs
from .aws import aws_handlers
from .aws_profile import aws_profile_handlers
from .aws_tools import aws_tools_handlers


class HandlerFuncRegistry(Registry):
    def get_key(self, obj):
        return obj.__name__


handler_func_registry = HandlerFuncRegistry()
reg = handler_func_registry

# --- aws_tools
reg.check_in(aws_tools_handlers.mh_clear_aws_tools_cache)
reg.check_in(aws_tools_handlers.mh_info)
reg.check_in(aws_tools_handlers.mh_rebuild_index)
reg.check_in(aws_tools_handlers.mh_clear_log)

# --- aws_profile
reg.check_in(aws_profile_handlers.mh_select_aws_profile_to_set_as_default)
reg.check_in(aws_profile_handlers.mh_set_default_aws_profile)
reg.check_in(aws_profile_handlers.mh_select_aws_profile_for_mfa_auth)
reg.check_in(aws_profile_handlers.mh_execute_mfa_auth)
reg.check_in(aws_profile_handlers.mh_select_aws_profile_to_set_as_aws_tools_default)
reg.check_in(aws_profile_handlers.mh_set_aws_profile_as_aws_tools_default)
reg.check_in(aws_profile_handlers.mh_select_aws_region_to_set_as_aws_tools_default)
reg.check_in(aws_profile_handlers.mh_set_aws_region_as_aws_tools_default)

# --- aws
reg.check_in(aws_handlers.mh_aws)


def debug_args(wf):
    wf.add_item(
        title="args = {}".format(wf.args),
        icon=HotIcons.error,
        valid=True,
    )


def debug_traceback(wf):
    from ..paths import PATH_ERROR_TRACEBACK

    traceback_msg = traceback.format_exc()
    PATH_ERROR_TRACEBACK.write_bytes(traceback_msg)

    lines = traceback_msg.splitlines()

    item_args = ItemArgs(
        title="ERROR! hit 'Enter' to open error traceback log",
        subtitle=PATH_ERROR_TRACEBACK.abspath,
        icon=HotIcons.error,
        valid=True,
    )
    item_args.open_file(PATH_ERROR_TRACEBACK.abspath)
    item_args.add_to_wf(wf)

    for line in lines:
        wf.add_item(
            title=line,
            arg=line,
            icon=HotIcons.error,
            valid=True,
        )
    return wf


def handler(wf, args=None):
    """
    Main handler that pass down argument to all other handler functions.

    handler function is a simple python function takes two arguments:

    1. wf
    2. query_str

    :type wf: Workflow3
    """
    if args is None:
        args = wf.args
    wf.log.debug("args = {}".format(args))

    if len(args) != 1:
        wf.add_item(
            title="Workflow arguments has to have exact one arg!",
            subtitle="correct format = '${handler_id} ${query_str}'",
            icon=HotIcons.error,
            valid=True,
        )
        debug_args(wf)
        return wf

    arg = args[0]
    if " " not in arg:
        wf.add_item(
            title="Invalid workflow arguments",
            subtitle="correct format = '${handler_id} ${query_str}'",
            icon=HotIcons.error,
            valid=True,
        )
        debug_args(wf)
        return wf

    handler_id, query_str = arg.split(" ", 1)
    query_str = query_str.lstrip()
    wf.log.debug("handler_id = {}".format(handler_id))

    if not reg.has(handler_id):
        wf.add_item(
            title="'{}' is not a valid handler identifier!".format(handler_id),
            icon=HotIcons.error,
            valid=True,
        )

    handler_func = reg.get(handler_id)
    handler_func(wf, query_str)

    return wf
