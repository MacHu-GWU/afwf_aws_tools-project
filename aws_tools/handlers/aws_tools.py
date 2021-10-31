# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from workflow.workflow3 import Workflow3
from ..cache import cache
from ..icons import HotIcons
from ..alfred import ItemArgs
from ..settings import settings, SettingKeys


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
        cmd = "{} {}".format(self.mh_clear_aws_tools_cache.__name__, magic_command)
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
        aws_profile = settings.get(SettingKeys.aws_profile)
        aws_region = settings.get(SettingKeys.aws_region)

        item_arg = ItemArgs(
            title="Current AWS Tools's aws profile = '{}'".format(aws_profile),
            subtitle="use 'aws-tool-set-profile' trigger to set it",
            arg="aws-tool-set-profile",
            icon=HotIcons.aws,
            valid=True,
        )
        item_arg.add_to_wf(wf)

        item_arg = ItemArgs(
            title="Current AWS Tools's aws region = '{}'".format(aws_region),
            subtitle="use 'aws-tool-set-region' trigger to set it",
            arg="aws-tool-set-region",
            icon=HotIcons.aws,
            valid=True,
        )
        item_arg.add_to_wf(wf)

        return wf


aws_tools_handlers = AWSToolsHandlers()
