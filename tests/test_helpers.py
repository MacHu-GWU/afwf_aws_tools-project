# -*- coding: utf-8 -*-

import pytest
from aws_tools.helpers import tokenize


class Test(object):
    def test_tokenize(self):
        assert tokenize("a-b_c-d") == ["a", "b", "c", "d"]
        assert tokenize("a-b-c-d") == ["a", "b", "c", "d"]
        assert tokenize("a_b-c_d") == ["a", "b", "c", "d"]


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
