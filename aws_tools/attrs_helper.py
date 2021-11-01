# -*- coding: utf-8 -*-

import attr


@attr.s
class Base(object):
    @classmethod
    def from_dict(cls, dct):
        """
        Factory method that create an instance from python dict.
        """
        return cls(**dct)

    def to_dict(self):
        """
        :rtype: dict
        """
        return attr.asdict(self)
