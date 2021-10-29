# -*- coding: utf-8 -*-

import pytest
from aws_tools.handlers.item_filter.aws_region import find_region


def test_find_region():
    assert "east" in find_region("east")[0][1]
    assert find_region("virg")[0][1] == "us-east-1"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
