# -*- coding: utf-8 -*-

"""
This module provides glue code to better use Alfred-Workflow library
https://pypi.org/project/Alfred-Workflow/
"""

from __future__ import print_function, unicode_literals
import attr
import typing
from workflow.workflow3 import Workflow3, Item3
from .attrs_helper import Base


# Alfred variables helpers
# Ref: https://www.deaxnishe.net/alfred-workflow/api/index.html?highlight=quicklookurl#workflow-variables
class VarKeyEnum(object):
    na = "na"
    open_file = "open_file"
    open_file_path = "open_file_path"
    open_browser = "open_browser"
    open_browser_url = "open_browser_url"
    run_script = "run_script"
    copy_text = "copy_text"
    copy_text_content = "copy_text_content"
    notify = "notify"
    notify_title = "notify_title"
    notify_subtitle = "notify_subtitle"


class VarValueEnum(object):
    y = "y"
    n = "n"


@attr.s
class ModArgs(Base):
    key = attr.ib()
    subtitle = attr.ib(default=None)
    arg = attr.ib(default=None)
    valid = attr.ib(default=None)
    icon = attr.ib(default=None)
    icontype = attr.ib(default=None)


@attr.s
class ItemArgs(Base):
    """
    A data class provides key value access pattern. It is the keyword arguments
    of ``Workflow3.add_item``.

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
    variables = attr.ib(factory=dict)  # type: dict
    modifiers = attr.ib(factory=list)  # type: list[ModArgs]

    def add_to_wf(self, wf):
        """
        Convert it to a ``Item3`` object and add to ``Workflow3``.

        :type wf: Workflow3
        :rtype: Item3
        """
        dct = self.to_dict()
        del dct["variables"]
        del dct["modifiers"]
        item = wf.add_item(**dct)
        for k, v in self.variables.items():
            item.setvar(k, v)
        for mod in self.modifiers:
            item.add_modifier(**mod.to_dict())
        return item

    # Set variable in a human friendly way.
    def open_file(self, path):
        """
        Add follow up action that open a file in default application.
        """
        self.variables[VarKeyEnum.open_file] = VarValueEnum.y
        self.variables[VarKeyEnum.open_file_path] = path

    def open_browser(self, url):
        """
        Add follow up action that open a url in default web browser.
        """
        self.variables[VarKeyEnum.open_browser] = VarValueEnum.y
        self.variables[VarKeyEnum.open_browser_url] = url

    def copy_text(self, content):
        """
        Add follow up action that copy a text to clipboard.
        """
        self.variables[VarKeyEnum.copy_text] = VarValueEnum.y
        self.variables[VarKeyEnum.copy_text_content] = content

    def notify(self, title, subtitle=""):
        """
        Add follow up action that send a MacOS notification.
        """
        self.variables[VarKeyEnum.notify] = VarValueEnum.y
        self.variables[VarKeyEnum.notify_title] = title
        self.variables[VarKeyEnum.notify_subtitle] = subtitle

    def run_script(self, cmd):
        """
        Add follow up action that run a command in bash.
        """
        self.variables[VarKeyEnum.run_script] = VarValueEnum.y
        self.arg = cmd

    def copy_arn(self, arn):
        """
        Add a 'Alt' modifier to copy the ARN to clipboard.
        """
        self.modifiers.append(
            ModArgs(key="alt", subtitle="hit 'Enter' to copy ARN to clipboard", arg=arn)
        )
