# -*- coding: utf-8 -*-

import attr


@attr.s
class Base(object):
    def to_dict(self):
        """
        :rtype: dict
        """
        return attr.asdict(self)
