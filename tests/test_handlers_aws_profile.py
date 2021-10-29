# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
from workflow import Workflow3
from aws_tools.handlers.aws_profile import aws_profile_handlers
from aws_tools.tests import setup_test_config_and_credential_file
from aws_tools.tests.paths import P_TEST_CONFIG_FILE, P_TEST_CREDENTIALS_FILE


class TestAWSProfileHandlers(object):
    def setup_method(self):
        setup_test_config_and_credential_file()

    def test_select_aws_profile(self):
        assert aws_profile_handlers.select_aws_profile.__name__ == "select_aws_profile"

        # wf = Workflow3()
        # set_profile(wf, args=[])
        # for item in wf._items:
        #     assert len(item.arg) == 12
        #     assert item.title == item.arg


if __name__ == '__main__':
    unittest.main()
