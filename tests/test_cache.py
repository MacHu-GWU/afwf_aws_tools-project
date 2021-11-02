# -*- coding: utf-8 -*-

import pytest
from aws_tools.cache import cache

call_counter = {"count": 0}


class MyClass(object):
    @cache.memoize(expire=10)
    def my_method(self, arg):
        call_counter["count"] += 1


@cache.memoize(expire=10)
def my_func(arg):
    call_counter["count"] += 1


def test_memoize():
    my_class = MyClass()
    assert call_counter["count"] == 0
    my_class.my_method(arg=1)
    assert call_counter["count"] == 1
    my_class.my_method(arg=1)
    assert call_counter["count"] == 1
    my_func(arg=1)
    assert call_counter["count"] == 2
    my_func(arg=1)
    assert call_counter["count"] == 2


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
