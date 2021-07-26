# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import workflow
from .. import icons
from ..credential import read_all_aws_profile, all_regions
from ..settings import settings, Keys


def select_profile(wf, args=None):
    """
    :type wf: workflow.Workflow3
    :type args: list[str]
    """
    if args is None:
        args = wf.args[1:]

    n_args = len(args)

    # No argument behavior
    if n_args == 0:
        aws_profile_list = read_all_aws_profile()
        for aws_profile in aws_profile_list:
            title = aws_profile
            subtitle = "set current aws named profile to: [{}]".format(aws_profile)
            autocomplete = aws_profile
            arg = aws_profile
            valid = True

            wf.add_item(
                title=title,
                subtitle=subtitle,
                autocomplete=autocomplete,
                arg=arg,
                valid=valid,
                icon=icons.ICON_IAM,
            )

    return wf


def set_profile(wf, args=None):
    """
    :type wf: workflow.Workflow3
    :type args: list[str]
    """
    if args is None:
        args = wf.args[1:]

    n_args = len(args)
    settings[Keys.aws_profile] = args[0]

    return wf


def select_region(wf, args=None):
    """
    :type wf: workflow.Workflow3
    :type args: list[str]
    """
    if args is None:
        args = wf.args[1:]

    n_args = len(args)

    # No argument behavior
    if n_args == 0:
        for region_description, region_name in all_regions:
            title = region_name
            subtitle = region_description
            autocomplete = region_name
            arg = region_name
            valid = True
            match = "{} {}".format(region_name, region_description)

            wf.add_item(
                title=title,
                subtitle=subtitle,
                autocomplete=autocomplete,
                arg=arg,
                valid=valid,
                match=match,
                icon=icons.ICON_IAM,
            )

    return wf


def set_region(wf, args=None):
    """
    :type wf: workflow.Workflow3
    :type args: list[str]
    """
    if args is None:
        args = wf.args[1:]

    n_args = len(args)
    settings[Keys.aws_region] = args[0]

    return wf
