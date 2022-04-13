# -*- coding: utf-8 -*-

"""
All workflow handlers for ``aws-tool-...`` trigger.
"""

from __future__ import unicode_literals
from workflow.workflow3 import Workflow3
from ..cache import cache
from ..icons import HotIcons
from ..alfred import ItemArgs
from ..logger import clear_log
from ..settings import (
    settings, SettingKeys, setting_key_list, find_setting, SettingMetadata, setting_metadata_list,
    setting_metadata_mapper
)
from ..search.aws_urls import main_service_searcher, sub_service_searcher
from ..helpers import tokenize
from ..paths import DIR_AWS_TOOL_USER_DATA


class AWSToolsHandlers(object):
    # ------ aws-tool-clear-cache script filter implementation ------
    def mh_clear_aws_tools_cache(self, wf, query_str):
        """
        :type wf: Workflow3
        :type query_str: str
        :rtype wf: Workflow3
        """
        magic_command = "do-clear-cache"
        if query_str == magic_command:
            cache.clear()
            return wf
        cmd = "~/.pyenv/shims/python2.7 main.py '{} {}'".format(self.mh_clear_aws_tools_cache.__name__, magic_command)
        item_arg = ItemArgs(
            title="Clear AWS tools workflow cache data",
            subtitle="hit 'Enter' to clear cache",
            icon=HotIcons.info,
            valid=True,
        )
        item_arg.run_script(cmd)
        item_arg.notify(title="AWS Tools workflow cache is cleared!")
        item_arg.add_to_wf(wf)
        return wf

    def mh_info(self, wf, query_str):
        """
        :type wf: Workflow3
        :type query_str: str
        :rtype wf: Workflow3
        """
        for s_meta in setting_metadata_mapper.values():
            item_args = ItemArgs(
                title="AWSToolsSetting({setting_key}) = {setting_value}".format(
                    setting_key=s_meta.key,
                    setting_value=settings.get(s_meta.key),
                ),
                subtitle="hit 'CMD + L' for detilas, use 'aws-tool-set {}' to set it.".format(s_meta.key),
                largetext=s_meta.short_description,
                arg="aws-tool-set {}".format(s_meta.key),
                icon=HotIcons.aws,
                valid=False,
            )
            item_args.add_to_wf(wf)
        return wf

    def mh_set_value(self, wf, query_str):
        """
        Update the setting sqlite db. Set key / value.

        :type wf: Workflow3
        :type query_str: str
        :rtype wf: Workflow3
        """
        st_key, st_value = query_str.split(" ")
        st_meta = setting_metadata_mapper[st_key]
        settings[st_key] = st_meta.converter(st_value)
        return wf

    def mh_set(self, wf, query_str):
        """
        :type wf: Workflow3
        :type query_str: str
        :rtype wf: Workflow3
        """

        def to_item_args(st_meta):
            """
            :type st_meta: SettingMetadata
            :rtype: ItemArgs
            """
            return ItemArgs(
                title="set value for '{}', current value = '{}'".format(
                    st_meta.key, settings.get(st_meta.key)),
                subtitle=st_meta.short_description,
                autocomplete="{} ".format(st_meta.key),
                largetext=st_meta.long_description,
                icon=HotIcons.aws,
                valid=True,
            )

        def handle_wrong_setting_key(wf, st_key):
            item_args = ItemArgs(
                title="'{}' is not a valid setting key!".format(st_key),
                subtitle="try 'aws-tool-set ' again",
                icon=HotIcons.info,
                valid=False,
            )
            item_args.add_to_wf(wf)
            return wf

        args = tokenize(query_str, space_only=True)
        if len(args) == 0:  # query = "aws-tool-set "
            for st_meta in setting_metadata_list:
                item_args = to_item_args(st_meta)
                item_args.add_to_wf(wf)
        elif len(args) == 1:
            if query_str[-1] != " ":  # query = "aws-tool-set "
                setting_query = args[0]
                st_key_list = find_setting(setting_query)
                for st_key in st_key_list:
                    st_meta = setting_metadata_mapper[st_key]
                    item_args = to_item_args(st_meta)
                    item_args.add_to_wf(wf)
            else:
                st_key = args[0]
                if st_key in setting_metadata_mapper:
                    item_args = ItemArgs(
                        title="Set AWSToolsSetting({}) = ?".format(st_key),
                        icon=HotIcons.info,
                        valid=False,
                    )
                    item_args.add_to_wf(wf)
                else:
                    handle_wrong_setting_key(wf, st_key)

        elif len(args) == 2:  # query = "aws-tool-set cache_expire 60"
            st_key, st_value = args
            if st_key in setting_metadata_mapper:
                item_args = ItemArgs(
                    title="Set AWSToolsSetting({}) = {}".format(st_key, st_value),
                    subtitle="hit 'Enter' to confirm",
                    icon=HotIcons.run,
                    valid=True,
                )
                cmd = "~/.pyenv/shims/python2.7 main.py '{} {} {}'".format(
                    self.mh_set_value.__name__,
                    st_key,
                    st_value,
                )
                item_args.run_script(cmd)
                item_args.notify(
                    title="Set AWSToolsSetting({}) = {}".format(st_key, st_value),
                )
                item_args.add_to_wf(wf)
            else:
                handle_wrong_setting_key(wf, st_key)
        else:
            pass
        return wf

    def mh_rebuild_index(self, wf, query_str):
        magic_command = "do-build-index"
        if query_str == magic_command:
            main_service_searcher.build_index(force_rebuild=True)
            sub_service_searcher.build_index(force_rebuild=True)
            return wf
        cmd = "~/.pyenv/shims/python2.7 main.py '{} {}'".format(self.mh_rebuild_index.__name__, magic_command)
        item_arg = ItemArgs(
            title="Rebuild AWS console url index",
            subtitle="hit 'Enter' to rebuild the index",
            icon=HotIcons.run,
            valid=True,
        )
        item_arg.run_script(cmd)
        item_arg.open_file(path=DIR_AWS_TOOL_USER_DATA.abspath)
        item_arg.notify(title="AWS Console url index is rebuilt!")
        item_arg.add_to_wf(wf)
        return wf

    def mh_clear_log(self, wf, query_str):
        magic_command = "do-clear-log"
        if query_str == magic_command:
            clear_log()
            return wf
        cmd = "~/.pyenv/shims/python2.7 main.py '{} {}'".format(self.mh_clear_log.__name__, magic_command)
        item_arg = ItemArgs(
            title="Clear all log files",
            subtitle="hit 'Enter' to clear the log",
            icon=HotIcons.info,
            valid=True,
        )
        item_arg.run_script(cmd)
        item_arg.open_file(path=DIR_AWS_TOOL_USER_DATA.abspath)
        item_arg.notify(title="AWS Tools log is cleared!")
        item_arg.add_to_wf(wf)
        return wf


aws_tools_handlers = AWSToolsHandlers()
