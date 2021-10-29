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
    mfa_auth,
)
from ..constants import (
    all_regions, FollowUpActionKey,
)
from ..settings import settings, SettingKeys


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

    # Case: /usr/bin/python main.py select_profile
    if n_args == 0:
        aws_profile_list_from_credential = read_all_profile_name_from_credential_file()
        aws_profile_list_from_config = read_all_profile_name_from_config_file()
        good_item_lst = list()
        bad_item_lst = list()
        for aws_profile in aws_profile_list_from_credential:
            aws_profile_in_config = aws_profile if aws_profile == "default" else "profile {}".format(aws_profile)
            if aws_profile_in_config not in aws_profile_list_from_config:
                item_dct = dict(
                    title="[{}] not found in config file".format(aws_profile_in_config),
                    subtitle="Open ~/.aws/config file",
                    autocomplete=aws_profile,
                    arg=PATH_DEFAULT_AWS_CONFIG_FILE.abspath,
                    valid=True,
                    icon=workflow.ICON_ERROR,
                )
                bad_item_lst.append(item_dct)
            else:
                item_dct = dict(
                    title=aws_profile,
                    subtitle="set current aws named profile to: [{}]".format(aws_profile),
                    autocomplete=aws_profile,
                    arg="{} {}".format(
                        set_default_profile.__name__,
                        aws_profile,
                    ),
                    valid=True,
                    icon=icons.ICON_IAM,
                )
                good_item_lst.append(item_dct)

        for item_dct in good_item_lst:
            wf.setvar("action", FollowUpActionKey.run_script)
            wf.add_item(**item_dct)

        for item_dct in bad_item_lst:
            wf.setvar("action", FollowUpActionKey.open_file)
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
    settings[SettingKeys.aws_profile] = args[0]

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
    settings[SettingKeys.aws_region] = args[0]

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

    if len(args) == 1:
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
    else:
        raise Exception

    return wf


def mfa_auth_select_profile(wf, args=None):
    """
    Update the ~/.aws/credentials and ~/.aws/config file, set default profile
    to one of named profile

    :type wf: workflow.Workflow3
    :type args: list[str]
    """
    if args is None:
        args = wf.args[1:]

    n_args = len(args)

    aws_profile_list_from_credential = read_all_profile_name_from_credential_file()
    aws_profile_list_from_credential = [
        aws_profile
        for aws_profile in aws_profile_list_from_credential if not aws_profile.endswith("_mfa")
    ]
    aws_profile_list_from_config = read_all_profile_name_from_config_file()

    good_item_lst = list()
    bad_item_lst = list()
    good_aws_profile_list = list()
    bad_aws_profile_list = list()
    for aws_profile in aws_profile_list_from_credential:
        aws_profile_in_config = aws_profile if aws_profile == "default" else "profile {}".format(aws_profile)

        if aws_profile_in_config not in aws_profile_list_from_config:
            item_dct = dict(
                title="[{}] not found in config file".format(aws_profile_in_config),
                subtitle="Open ~/.aws/config file",
                autocomplete=aws_profile,
                arg=PATH_DEFAULT_AWS_CONFIG_FILE.abspath,
                valid=True,
                icon=workflow.ICON_ERROR,
            )
            bad_item_lst.append(item_dct)
            bad_aws_profile_list.append(aws_profile)
        else:
            item_dct = dict(
                title=aws_profile,
                subtitle="Use base profile '{}' for MFA auth".format(aws_profile),
                autocomplete=aws_profile,
                arg=aws_profile,
                valid=True,
                icon=icons.ICON_IAM,
            )
            good_item_lst.append(item_dct)
            good_aws_profile_list.append(aws_profile)

    all_item_lst = good_item_lst + bad_item_lst

    # No argument behavior
    # Case: /usr/bin/python main.py mfa_auth_select_profile
    if n_args == 0:
        for item_dct in good_item_lst:
            wf.setvar("action", FollowUpActionKey.run_script)
            wf.add_item(**item_dct)

        for item_dct in bad_item_lst:
            wf.setvar("action", FollowUpActionKey.open_file)
            wf.add_item(**item_dct)

    # Case: /usr/bin/python main.py mfa_auth_select_profile ${aws_profile}
    elif len(args) == 1:
        aws_profile = args[0]

        # ${profile_name_part} is a valid
        if aws_profile in good_aws_profile_list:
            wf.setvar("action", FollowUpActionKey.open_url)
            wf.add_item(
                title="Enter your six digits MFA Token",
                subtitle="Doc https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/",
                arg="https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/",
                valid=True,
                icon=icons.ICON_IAM,
            )
        elif aws_profile in bad_aws_profile_list:
            wf.setvar("action", FollowUpActionKey.open_file)
            wf.add_item(
                title="[profile {}] not found in config file".format(aws_profile),
                subtitle="Open ~/.aws/config file, check '{}'".format(aws_profile),
                arg=PATH_DEFAULT_AWS_CONFIG_FILE.abspath,
                valid=True,
                icon=workflow.ICON_ERROR,
            )
        else:
            all_item_lst = [
                item_dct
                for item_dct in all_item_lst
                if aws_profile in item_dct["title"]
            ]
            if len(all_item_lst):
                for item_dct in all_item_lst:
                    wf.add_item(**item_dct)
            else:
                wf.setvar("action", FollowUpActionKey.open_file)
                wf.add_item(
                    title="'{}' is not a valid named profile!".format(aws_profile),
                    subtitle="Open ~/.aws/credentials file, check '{}'".format(aws_profile),
                    arg=PATH_DEFAULT_AWS_CREDENTIAL_FILE.abspath,
                    valid=True,
                    icon=workflow.ICON_ERROR,
                )

    # Case: /usr/bin/python main.py mfa_auth_select_profile ${aws_profile} ${mfa_code}
    elif len(args) == 2:
        aws_profile = args[0]
        # ${aws_profile} is a good profile name in ~/.aws/credentials
        if aws_profile not in good_aws_profile_list:
            wf.setvar("action", FollowUpActionKey.open_file)
            wf.add_item(
                title="'{}' is not a valid named profile!".format(aws_profile),
                subtitle="Open ~/.aws/credentials file, check '{}'".format(aws_profile),
                arg=PATH_DEFAULT_AWS_CREDENTIAL_FILE.abspath,
                valid=True,
                icon=workflow.ICON_ERROR,
            )
            return wf

        mfa_code = args[1]
        if len(mfa_code) != 6:
            wf.add_item(
                title="Enter your six digits MFA Token",
                subtitle="'{}' is not a valid MFA token".format(mfa_code),
                arg="https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/",
                valid=True,
                icon=icons.ICON_IAM,
            )
        else:
            wf.setvar("action", FollowUpActionKey.run_script)
            wf.add_item(
                title="Create '{}_mfa' MFA profile".format(aws_profile),
                subtitle="",
                arg="{} {} {}".format(
                    mfa_auth_execute_mfa.__name__,
                    aws_profile,
                    mfa_code,
                ),
                valid=True,
                icon=icons.ICON_IAM,
            )
    else:
        wf.add_item(
            title="Too many arguments!",
            arg="",
            valid=True,
            icon=workflow.ICON_ERROR,
        )

    return wf


def mfa_auth_execute_mfa(wf, args=None):
    """
    Update the ~/.aws/credentials and ~/.aws/config file, create / update
    the new mfa profile

    :type wf: workflow.Workflow3
    :type args: list[str]
    """
    if args is None:
        args = wf.args[1:]

    n_args = len(args)

    if len(args) == 2:
        aws_profile = args[0]
        mfa_code = args[1]
        mfa_auth(aws_profile=aws_profile, mfa_code=mfa_code)
    else:
        raise Exception

    return wf

