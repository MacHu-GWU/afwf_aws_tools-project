# -*- coding: utf-8 -*-

import pytest
from aws_tools.cache import cache


class MyClass(object):
    @cache.memoize(expire=10)
    def my_method(self, arg):
        print("my method: arg = {}".format(arg))


@cache.memoize(expire=10)
def my_func(arg):
    print("my func: arg = {}".format(arg))


def test_memoize():
    my_class = MyClass()
    my_class.my_method(arg=1)
    my_func(arg=1)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
