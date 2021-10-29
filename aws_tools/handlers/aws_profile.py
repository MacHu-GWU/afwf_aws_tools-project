# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import workflow
import typing
from pathlib_mate import Path
from ..cache import cache, CacheKeys
from ..icons import HotIcons
from ..credential import (
    PATH_DEFAULT_AWS_CONFIG_FILE,
    PATH_DEFAULT_AWS_CREDENTIALS_FILE,
    read_all_section_name,
    replace_section,
    set_named_profile_as_default,
    mfa_auth,
)
from ..constants import (
    all_regions, FollowUpActionKey,
)
from ..settings import settings, SettingKeys
from fuzzywuzzy import process


class AWSProfileHandlers:
    aws_config_file = PATH_DEFAULT_AWS_CONFIG_FILE  # type: Path
    aws_credentials_file = PATH_DEFAULT_AWS_CREDENTIALS_FILE  # type: Path

    def _read_aws_profile_from_config(self):
        """
        :rtype: typing.List[str]
        """
        aws_profile_list_from_config = read_all_section_name(self.aws_config_file.abspath)
        aws_profile_list_from_config = [
            aws_profile[8:] if aws_profile.startswith("profile ") else aws_profile
            for aws_profile in aws_profile_list_from_config
        ]
        return aws_profile_list_from_config

    # ------- aws-set-default-profile keyword implementation ---
    def mh_set_default_aws_profile(self, wf, query_str):
        set_named_profile_as_default(aws_profile=query_str)
        return wf

    def ib_select_aws_profile_for_default(self, wf, list_of_profile):
        wf.setvar("action", FollowUpActionKey.run_script)
        for aws_profile in list_of_profile:
            wf.add_item(
                title=aws_profile,
                subtitle="set the default profile to: [{}]".format(aws_profile),
                autocomplete=aws_profile,
                arg="{} {}".format(
                    self.mh_set_default_aws_profile.__name__,
                    aws_profile,
                ),
                icon=HotIcons.iam,
                valid=True,
            )
        return wf

    def sh_show_all_aws_profile(self, wf, item_builder):
        """
        :type item_builder: callable
        """
        aws_profile_list_from_config = self._read_aws_profile_from_config()
        item_builder(wf, aws_profile_list_from_config)
        return wf

    def sh_show_filtered_aws_profile(self, wf, query_str, item_builder):
        """
        :type item_builder: callable
        """
        aws_profile_list_from_config = self._read_aws_profile_from_config()
        filtered_aws_profile_list = [
            tp[0]
            for tp in process.extract(query_str.strip(), aws_profile_list_from_config, limit=20)
        ]
        item_builder(wf, filtered_aws_profile_list)
        return wf

    def mh_select_aws_profile_to_set_as_default(self, wf, query_str):
        """
        Return list of available aws named profile to select.

        Return profile name as argument.

        :type wf: workflow.Workflow3
        :type args: list[str]
        """
        if bool(query_str) is False:
            self.sh_show_all_aws_profile(
                wf,
                item_builder=self.ib_select_aws_profile_for_default,
            )
        else:
            self.sh_show_filtered_aws_profile(
                wf,
                query_str,
                item_builder=self.ib_select_aws_profile_for_default,
            )
        return wf

    # ------- aws-mfa-auth keyword implementation ---
    def mh_execute_mfa_auth(self, wf, query_str):
        """
        Update the ~/.aws/credentials and ~/.aws/config file, create / update
        the new mfa profile

        :type wf: workflow.Workflow3
        :type query_str: str
        """
        args = query_str.split(" ")
        if len(args) == 2:
            profile_name, mfa_token = args
            mfa_auth(aws_profile=profile_name, mfa_code=mfa_token)
        else:
            raise ValueError()
        return wf

    def ib_select_aws_profile_for_mfa(self, wf, list_of_profile):
        wf.setvar("action", FollowUpActionKey.run_script)
        for aws_profile in list_of_profile:
            wf.add_item(
                title=aws_profile,
                subtitle="Use base profile [{}] for MFA auth".format(aws_profile),
                autocomplete="{} ".format(aws_profile),
                arg="{} {}".format(
                    self.mh_execute_mfa_auth.__name__,
                    aws_profile,
                ),
                icon=HotIcons.iam,
                valid=True,
            )
        return wf

    def mh_select_aws_profile_for_mfa_auth(self, wf, query_str):
        if bool(query_str) is False:
            self.sh_show_all_aws_profile(
                wf,
                item_builder=self.ib_select_aws_profile_for_mfa,
            )
            return wf

        args = query_str.split(" ")
        if len(args) == 1:
            self.sh_show_filtered_aws_profile(
                wf,
                query_str,
                item_builder=self.ib_select_aws_profile_for_mfa,
            )
        elif len(args) == 2:
            profile_name, mfa_token = args
            aws_profile_list_from_config = cache.fast_get(
                key=CacheKeys.aws_profile_list_from_config,
                callable=self._read_aws_profile_from_config,
                expire=10,
            )
            if profile_name not in aws_profile_list_from_config:  # example: "a_invalid_profile a_mfa_token"
                # display helper info
                wf.add_item(
                    title="'{}' is not a valid named profile!".format(profile_name),
                    subtitle="below is list of valid profile",
                    icon=workflow.ICON_ERROR,
                    valid=True,
                )
                for _profile_name in aws_profile_list_from_config:
                    wf.add_item(
                        title=_profile_name,
                        subtitle="hit 'Tab' to choose this profile",
                        autocomplete="{} ".format(_profile_name),
                        icon=HotIcons.iam,
                        valid=True
                    )
            elif bool(mfa_token) is False:  # example: "a_valid_profile "
                wf.setvar("action", FollowUpActionKey.open_url)
                wf.add_item(
                    title="Enter your six digits MFA Token",
                    subtitle="Doc https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/",
                    arg="https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/",
                    icon=HotIcons.iam,
                    valid=True,
                )
            else:
                if len(mfa_token) < 6:  # example: "a_valid_profile 123"
                    wf.setvar("action", FollowUpActionKey.open_url)
                    wf.add_item(
                        title="Enter your six digits MFA Token '{}'".format(mfa_token),
                        subtitle="Doc https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/",
                        arg="https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/",
                        icon=HotIcons.iam,
                        valid=True,
                    )
                elif len(mfa_token) > 6:  # example: "a_valid_profile 123456789"
                    wf.setvar("action", FollowUpActionKey.open_url)
                    wf.add_item(
                        title="MFA Token has to be 6 digits!".format(mfa_token),
                        subtitle="Doc https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/",
                        arg="https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/",
                        icon=HotIcons.error,
                        valid=True,
                    )
                elif not mfa_token.isdigit():  # example: "a_valid_profile abcdef"
                    wf.setvar("action", FollowUpActionKey.open_url)
                    wf.add_item(
                        title="MFA Token has to be 6 digits!".format(mfa_token),
                        subtitle="Doc https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/",
                        arg="https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/",
                        icon=HotIcons.error,
                        valid=True,
                    )
                else:  # example: "a_valid_profile 123456"
                    wf.setvar("action", FollowUpActionKey.run_script)
                    wf.add_item(
                        title="Do MFA auth using token '{}'".format(mfa_token),
                        subtitle="hit 'Enter' to execute MFA auth",
                        arg="{} {} {}".format(
                            self.mh_execute_mfa_auth.__name__,
                            profile_name,
                            mfa_token,
                        ),
                        icon=HotIcons.iam,
                        valid=True,
                    )
        else:
            wf.add_item(
                title="Invalid arg: '{}'".format(query_str),
                subtitle="valid arg: '{aws_profile_name} {six_digit_mfa_token}'",
                icon=workflow.ICON_ERROR,
                valid=True,
            )
        return wf


aws_profile_handlers = AWSProfileHandlers()


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


def aws_set_default_profile(wf, query=None):
    """
    Update the ~/.aws/credentials and ~/.aws/config file, set default profile
    to one of named profile

    :type wf: workflow.Workflow3
    :type args: list[str]
    """
    if query is None:
        query = wf.args[1]

    if len(query) == 0:  #
        select_profile(wf)

    if len(args) == 1:
        profile_name = args[0]
        if profile_name != "default":
            replace_section(
                config_file=PATH_DEFAULT_AWS_CREDENTIALS_FILE.abspath,
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
