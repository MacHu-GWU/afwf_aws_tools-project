# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from workflow import Workflow3
from aws_tools.handlers.aws import aws_handlers
from aws_tools.tests import setup_test_config_and_credential_file


class TestAWSHandlers(object):
    wf = Workflow3()

    def setup_method(self):
        self.wf = Workflow3()
        setup_test_config_and_credential_file()

    def test_set_default_aws_profile(self):
        aws_handlers.mh_aws(self.wf, query_str="")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
