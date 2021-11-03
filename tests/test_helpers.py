# -*- coding: utf-8 -*-

import pytest
from aws_tools.helpers import (
    tokenize,
    union, intersect,
)


class Test(object):
    def test_tokenize(self):
        assert tokenize("a-b_c-d") == ["a", "b", "c", "d"]
        assert tokenize("a-b-c-d") == ["a", "b", "c", "d"]
        assert tokenize("a_b-c_d") == ["a", "b", "c", "d"]

        assert tokenize("a_b c_d", space_only=True) == ["a_b", "c_d"]


def test_union():
    assert union([1, 2], [2, 3]) == [1, 2, 3]
    assert union([1, 2]) == [1, 2]
    with pytest.raises(Exception):
        union()


def test_intersect():
    assert intersect([1, 2, 3], [2, 3, 4]) == [2, 3]
    assert intersect([1, 2]) == [1, 2]
    with pytest.raises(Exception):
        intersect()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
