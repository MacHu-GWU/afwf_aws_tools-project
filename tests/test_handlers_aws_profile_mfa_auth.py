# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from workflow.workflow3 import Workflow3
from aws_tools.handlers.aws_profile import aws_profile_handlers


class TestAWSProfileHandlers(object):
    def test_execute_mfa_auth(self):
        wf = Workflow3()
        # aws_profile_handlers.mh_execute_mfa_auth(wf, query_str="aws_data_lab_sanhe 980814")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
