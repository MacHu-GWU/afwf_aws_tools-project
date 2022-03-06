# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from typing import List, Tuple
from workflow.workflow3 import Workflow3
from ...alfred import ItemArgs
from ...icons import HotIcons


class ItemBuilders(object):
    """
    This class take some parameter as input, and return list of ``ItemArgs`` as output.
    """
    def __init__(self):
        self.kwargs = dict()

    def select_aws_profile_as_default(
        self,
        wf,
        aws_profile_list,
        set_default_aws_profile_handler_id,
    ):
        """
        :type wf: Workflow3
        :type aws_profile_list: list[str]
        :type set_default_aws_profile_handler_id: str
        :rtype: Workflow3
        """
        for aws_profile in aws_profile_list:
            cmd = "/usr/bin/python main.py '{} {}'".format(
                set_default_aws_profile_handler_id,
                aws_profile,
            )
            item_arg = ItemArgs(
                title=aws_profile,
                subtitle="set AWS CLI default profile as [{}]]".format(aws_profile),
                autocomplete=aws_profile,
                icon=HotIcons.iam,
                valid=True,
            )
            item_arg.run_script(cmd)
            item_arg.notify(title="now AWS CLI default profile is", subtitle=aws_profile)
            item_arg.add_to_wf(wf)
        return wf

    def select_aws_profile_for_mfa(
        self,
        wf,
        aws_profile_list,
        execute_mfa_auth_handler_id,
    ):
        """
        :type wf: Workflow3
        :type aws_profile_list: list[str]
        :type execute_mfa_auth_handler_id: str
        :rtype: Workflow3
        """
        for aws_profile in aws_profile_list:
            cmd = "/usr/bin/python main.py '{} {}'".format(
                execute_mfa_auth_handler_id,
                aws_profile,
            )
            item_arg = ItemArgs(
                title=aws_profile,
                subtitle="Use base profile [{}] for MFA auth".format(aws_profile),
                autocomplete="{} ".format(aws_profile),
                icon=HotIcons.iam,
                valid=True,
            )
            item_arg.run_script(cmd)
            item_arg.notify(title="A new mfa profile is created", subtitle="{}_mfa".format(aws_profile))
            item_arg.add_to_wf(wf)
        return wf

    def set_aws_profile_as_aws_tools_default(
        self,
        wf,
        aws_profile_list,
        set_aws_profile_as_aws_tools_default_handler_id,
    ):
        """
        :type wf: Workflow3
        :type aws_profile_list: List[str]
        :type set_aws_profile_as_aws_tools_default_handler_id: str
        :rtype: Workflow3
        """
        for aws_profile in aws_profile_list:
            cmd = "/usr/bin/python main.py '{} {}'".format(
                set_aws_profile_as_aws_tools_default_handler_id,
                aws_profile,
            )
            item_arg = ItemArgs(
                title=aws_profile,
                subtitle="set AWS Tools default profile as [{}]".format(aws_profile),
                autocomplete=aws_profile,
                icon=HotIcons.iam,
                valid=True,
            )
            item_arg.run_script(cmd)
            item_arg.notify(title="now AWS Tools default profile is", subtitle=aws_profile)
            item_arg.add_to_wf(wf)
        return wf

    def set_aws_region_as_aws_tools_default(
        self,
        wf,
        all_regions,
        set_aws_region_as_aws_tools_default_handler_id,
    ):
        """
        :type wf: Workflow3
        :type all_regions: list[tuple[str, str]]
        :type set_aws_region_as_aws_tools_default_handler_id: str
        :rtype: Workflow3
        """
        for long_name, short_name in all_regions:
            cmd = "/usr/bin/python main.py '{} {}'".format(
                set_aws_region_as_aws_tools_default_handler_id,
                short_name,
            )
            item_arg = ItemArgs(
                title="{} | {}".format(short_name, long_name),
                subtitle="set AWS Tools default region as [{}]".format(short_name),
                autocomplete=short_name,
                icon=HotIcons.iam,
                valid=True,
            )
            item_arg.run_script(cmd)
            item_arg.notify(title="now AWS Tools default region is", subtitle=short_name)
            item_arg.add_to_wf(wf)
        return wf

    def set_aws_profile_as_default_for_everything(
        self,
        wf,
        aws_profile_and_region_list,
        set_aws_profile_as_default_for_everything_handler_id,
    ):
        """
        :type wf: Workflow3
        :type aws_profile_and_region_list: List[Tuple[str, str]]
        :type set_aws_profile_as_default_for_everything_handler_id: str
        :rtype: Workflow3
        """
        for aws_profile, region in aws_profile_and_region_list:
            cmd = "/usr/bin/python main.py '{} {}'".format(
                set_aws_profile_as_default_for_everything_handler_id,
                "{}____{}".format(aws_profile, region),
            )
            item_arg = ItemArgs(
                title="{} {}".format(aws_profile, region),
                subtitle="set default profile as [{}] for everything".format(aws_profile),
                autocomplete=aws_profile,
                icon=HotIcons.iam,
                valid=True,
            )
            item_arg.run_script(cmd)
            item_arg.notify(
                title="now default profile and region is",
                subtitle="{} {}".format(aws_profile, region),
            )
            item_arg.add_to_wf(wf)
        return wf


item_builders = ItemBuilders()
