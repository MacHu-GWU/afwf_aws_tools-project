# -*- coding: utf-8 -*-

import pytest
from aws_tools.search.aws_res import register


def test_register():
    register.get("ec2-instances").list_res()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
