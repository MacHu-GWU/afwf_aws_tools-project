# -*- coding: utf-8 -*-

import pytest
from workflow.workflow3 import Workflow3
from aws_tools.handlers.item_builder import item_builders


class TestItemBuilders:
    wf = Workflow3()

    def setup_method(self):
        self.wf = Workflow3()

    def test_select_aws_profile_as_default(self):
        item_builders.select_aws_profile_as_default(
            wf=self.wf,
            aws_profile_list=["a", "b", "c"],
            set_default_aws_profile_handler_id="handler_id"
        )

    def test_select_aws_profile_for_mfa(self):
        item_builders.select_aws_profile_for_mfa(
            wf=self.wf,
            aws_profile_list=["a", "b", "c"],
            execute_mfa_auth_handler_id="handler_id"
        )

    def test_set_aws_profile_as_aws_tools_default(self):
        item_builders.set_aws_profile_as_aws_tools_default(
            wf=self.wf,
            aws_profile_list=["a", "b", "c"],
            set_aws_profile_as_aws_tools_default_handler_id="handler_id"
        )


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
