# -*- coding: utf-8 -*-

import attr


@attr.s
class Base(object):
    @classmethod
    def from_dict(cls, dct):
        """
        Factory method that create an instance from python dict.

        :type dct: dict
        """
        return cls(**dct)

    def to_dict(self):
        """
        :rtype: dict
        """
        return attr.asdict(self)

    @classmethod
    def from_many_dict(cls, list_of_dict):
        """
        :type list_of_dict: list[dict]
        :rtype: list
        """
        return [
            cls.from_dict(dct)
            for dct in list_of_dict
        ]
