# -*- coding: utf-8 -*-

import pytest
from aws_tools.settings import settings, SettingKeys


class Test(object):
    def test_read_all_aws_profile(self):
        settings[SettingKeys._debug] = "debug info"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
