# -*- coding: utf-8 -*-

"""
This module provides glue code to better use Alfred-Workflow library
https://pypi.org/project/Alfred-Workflow/
"""

from __future__ import print_function, unicode_literals
import attr
from workflow.workflow3 import Workflow3

Workflow3.add_item()


@attr.s
class ItemArgs(object):
    """
    A data class provides key value access pattern.

    There's a ``workflow.workflow3.Item3`` class, why another class?

    The ``workflow.workflow3.Workflow3`` only support ``.add_item(**kwargs)``
    but not ``.add_item(Item3(**kwargs))`` API. the ``Item3.obj`` returns a
    dict data container but cannot immediately use in ``.add_item`` api. It is
    because of the underlying implementation. This new data class ensure the
    consistent API.

    Usage::

        item = ItemArgs(title=...)
        workflow.add_item(**item.to_dict())
    """
    title = attr.ib()
    subtitle = attr.ib(default="")
    arg = attr.ib(default=None)
    autocomplete = attr.ib(default=None)
    valid = attr.ib(default=False)
    uid = attr.ib(default=None)
    icon = attr.ib(default=None)
    icontype = attr.ib(default=None)
    type = attr.ib(default=None)
    largetext = attr.ib(default=None)
    copytext = attr.ib(default=None)
    quicklookurl = attr.ib(default=None)
    match = attr.ib(default=None)

    def to_dict(self):
        return attr.asdict(self)

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)
