# -*- coding: utf-8 -*-

from workflow.workflow3 import Workflow3
from ...constants import FollowUpActionKey
from ...icons import HotIcons


class ItemBuilders(object):
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
        wf.setvar("action", FollowUpActionKey.run_script)
        for aws_profile in aws_profile_list:
            wf.add_item(
                title=aws_profile,
                subtitle="set AWS CLI default profile as [{}]]".format(aws_profile),
                autocomplete=aws_profile,
                arg="{} {}".format(
                    set_default_aws_profile_handler_id,
                    aws_profile,
                ),
                icon=HotIcons.iam,
                valid=True,
            )
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
        wf.setvar("action", FollowUpActionKey.run_script)
        for aws_profile in aws_profile_list:
            wf.add_item(
                title=aws_profile,
                subtitle="Use base profile [{}] for MFA auth".format(aws_profile),
                autocomplete="{} ".format(aws_profile),
                arg="{} {}".format(
                    execute_mfa_auth_handler_id,
                    aws_profile,
                ),
                icon=HotIcons.iam,
                valid=True,
            )
        return wf

    def set_aws_profile_as_aws_tools_default(
            self,
            wf,
            aws_profile_list,
            set_aws_profile_as_aws_tools_default_handler_id,
    ):
        """
        :type wf: Workflow3
        :type aws_profile_list: list[str]
        :type set_default_aws_profile_handler_id: str
        :rtype: Workflow3
        """
        wf.setvar("action", FollowUpActionKey.run_script)
        for aws_profile in aws_profile_list:
            wf.add_item(
                title=aws_profile,
                subtitle="set AWS Tools default profile as [{}]".format(aws_profile),
                autocomplete=aws_profile,
                arg="{} {}".format(
                    set_aws_profile_as_aws_tools_default_handler_id,
                    aws_profile,
                ),
                icon=HotIcons.iam,
                valid=True,
            )
        return wf


item_builders = ItemBuilders()
