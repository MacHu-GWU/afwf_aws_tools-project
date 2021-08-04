# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import workflow
from .. import icons
from ..credential import (
    PATH_DEFAULT_AWS_CREDENTIAL_FILE,
    PATH_DEFAULT_AWS_CONFIG_FILE,
    read_all_profile_name_from_credential_file,
    read_all_profile_name_from_config_file,
    replace_section,
    all_regions,
)
from ..settings import settings, Keys


def select_profile(wf, args=None):
    """
    Return list of available aws named profile to select.

    Return profile name as argument.

    :type wf: workflow.Workflow3
    :type args: list[str]
    """
    if args is None:
        args = wf.args[1:]

    n_args = len(args)

    # No argument behavior
    if n_args == 0:
        aws_profile_list_from_credential = read_all_profile_name_from_credential_file()
        aws_profile_list_from_config = read_all_profile_name_from_config_file()
        good_item_lst = list()
        bad_item_lst = list()
        for aws_profile in aws_profile_list_from_credential:
            if "profile {}".format(aws_profile) not in aws_profile_list_from_config:
                item_dct = dict(
                    title="[profile {}] not found in config file".format(aws_profile),
                    subtitle="Open ~/.aws/config file".format(aws_profile),
                    autocomplete=aws_profile,
                    arg="_open_aws_config_file",
                    valid=True,
                    icon=workflow.ICON_ERROR,
                )
                bad_item_lst.append(item_dct)
            else:
                item_dct = dict(
                    title=aws_profile,
                    subtitle="set current aws named profile to: [{}]".format(aws_profile),
                    autocomplete=aws_profile,
                    arg=aws_profile,
                    valid=True,
                    icon=icons.ICON_IAM,
                )
                good_item_lst.append(item_dct)

        for item_dct in (good_item_lst + bad_item_lst):
            wf.add_item(**item_dct)

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


def set_default_profile(wf, args=None):
    """
    Update the ~/.aws/credentials and ~/.aws/config file, set default profile
    to one of named profile

    :type wf: workflow.Workflow3
    :type args: list[str]
    """
    if args is None:
        args = wf.args[1:]

    n_args = len(args)

    profile_name = args[0]
    if profile_name != "default":
        replace_section(
            config_file=PATH_DEFAULT_AWS_CREDENTIAL_FILE.abspath,
            source_section_name=profile_name,
            target_section_name="default",
        )
        replace_section(
            config_file=PATH_DEFAULT_AWS_CONFIG_FILE.abspath,
            source_section_name="profile {}".format(profile_name),
            target_section_name="default",
        )

    return wf
