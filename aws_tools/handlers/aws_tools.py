# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from workflow.workflow3 import Workflow3
from ..constants import FollowUpActionKey
from ..cache import cache
from ..icons import HotIcons


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

        wf.setvar("action", FollowUpActionKey.run_script)
        wf.add_item(
            title="Clear AWS tools workflow cache data",
            subtitle="hit 'Enter' to clear cache",
            arg="{} {}".format(self.mh_clear_aws_tools_cache.__name__, magic_command),
            icon=HotIcons.help,
            valid=True,
        )
        return wf


aws_tools_handlers = AWSToolsHandlers()
