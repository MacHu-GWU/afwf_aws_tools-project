# -*- coding: utf-8 -*-

"""
This module implements a the Registry design pattern. In ``aws_tools``,
we only register object but not generic python type.

Example::

    >>> p_reg = PeopleRegistry()
    >>> alice = Person(name="alice")
    >>> p_reg.check_in(alice)
    >>> p_reg.look_up("alice").name
    alice
    >>> p_reg.has("alice")
    True
    >>> p_reg.has("bob")
    False
"""


class Registry(object):
    def __init__(self):
        self._mapper = dict()

    def get_key(self, obj):
        raise NotImplementedError

    def set(self, key, value):
        self._mapper[key] = value

    def get(self, key):
        return self._mapper[key]

    def has(self, key):
        return key in self._mapper

    def check_in(self, obj):
        self.set(key=self.get_key(obj), value=obj)

    def look_up(self, key):
        return self._mapper.get(key)
