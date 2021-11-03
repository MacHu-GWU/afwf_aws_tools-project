# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from workflow.workflow3 import Workflow3
from pathlib_mate import Path
from ..icons import HotIcons
from ..credential import (
    PATH_DEFAULT_AWS_CONFIG_FILE,
    PATH_DEFAULT_AWS_CREDENTIALS_FILE,
    set_named_profile_as_default,
    mfa_auth,
)
from ..alfred import ItemArgs
from ..settings import settings, SettingKeys
from .item_builder import item_builders
from .item_filter import item_filters


class AWSProfileHandlers(object):
    aws_config_file = PATH_DEFAULT_AWS_CONFIG_FILE  # type: Path
    aws_credentials_file = PATH_DEFAULT_AWS_CREDENTIALS_FILE  # type: Path

    # ------- aws-set-default-profile keyword implementation ---
    def mh_set_default_aws_profile(self, wf, query_str):
        """
        :type wf: Workflow3
        :type query_str: str
        """
        set_named_profile_as_default(
            aws_profile=query_str,
            aws_config_file=self.aws_config_file.abspath,
            aws_credentials_file=self.aws_credentials_file.abspath,
        )
        return wf

    def mh_select_aws_profile_to_set_as_default(self, wf, query_str):
        """
        Return list of available aws named profile to select.

        Return profile name as argument.

        :type wf: Workflow3
        :type query_str: str
        """
        aws_profile_list = item_filters.aws_profile(
            query_str=query_str,
            aws_config_file=self.aws_config_file.abspath,
        )
        item_builders.select_aws_profile_as_default(
            wf=wf,
            aws_profile_list=aws_profile_list,
            set_default_aws_profile_handler_id=self.mh_set_default_aws_profile.__name__,
        )
        return wf

    # ------- aws-mfa-auth keyword implementation ---
    def mh_execute_mfa_auth(self, wf, query_str):
        """
        Update the ~/.aws/credentials and ~/.aws/config file, create / update
        the new mfa profile

        :type wf: Workflow3
        :type query_str: str
        """
        args = query_str.split(" ")
        if len(args) == 2:
            profile_name, mfa_token = args
            mfa_auth(
                aws_profile=profile_name,
                mfa_code=mfa_token,
                aws_config_file=self.aws_config_file.abspath,
                aws_credentials_file=self.aws_credentials_file.abspath,
            )
        else:
            raise ValueError()
        return wf

    def mh_select_aws_profile_for_mfa_auth(self, wf, query_str):
        """
        :type wf: Workflow3
        :type query_str: str
        """
        args = query_str.split(" ")
        help_url = "https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/"
        if len(args) == 1:
            aws_profile_list = item_filters.aws_profile(
                query_str=query_str,
                aws_config_file=self.aws_config_file.abspath,
            )
            item_builders.select_aws_profile_for_mfa(
                wf=wf,
                aws_profile_list=aws_profile_list,
                execute_mfa_auth_handler_id=self.mh_set_default_aws_profile.__name__,
            )

        elif len(args) == 2:
            profile_name, mfa_token = args
            aws_profile_list = item_filters.aws_profile(
                query_str=query_str,
                aws_config_file=self.aws_config_file.abspath,
            )
            if profile_name not in aws_profile_list:  # example: "a_invalid_profile a_mfa_token"
                # display helper info
                wf.add_item(
                    title="'{}' is not a valid named profile!".format(profile_name),
                    subtitle="below is list of valid profile",
                    icon=HotIcons.error,
                    valid=True,
                )
                for _profile_name in aws_profile_list:
                    wf.add_item(
                        title=_profile_name,
                        subtitle="hit 'Tab' to choose this profile",
                        autocomplete="{} ".format(_profile_name),
                        icon=HotIcons.iam,
                        valid=True
                    )
            elif bool(mfa_token) is False:  # example: "a_valid_profile "
                item_arg = ItemArgs(
                    title="Enter your six digits MFA Token",
                    subtitle="Doc: {}".format(help_url),
                    icon=HotIcons.iam,
                    valid=True,
                )
                item_arg.open_browser(help_url)
                item_arg.add_to_wf(wf)
            else:
                if len(mfa_token) < 6:  # example: "a_valid_profile 123"
                    item_arg = ItemArgs(
                        title="Enter your six digits MFA Token '{}'".format(mfa_token),
                        subtitle="Doc: {}".format(help_url),
                        icon=HotIcons.iam,
                        valid=True,
                    )
                    item_arg.open_browser(help_url)
                    item_arg.add_to_wf(wf)
                elif len(mfa_token) > 6:  # example: "a_valid_profile 123456789"
                    item_arg = ItemArgs(
                        title="MFA Token has to be 6 digits!".format(mfa_token),
                        subtitle="Doc: {}".format(help_url),
                        icon=HotIcons.error,
                        valid=True,
                    )
                    item_arg.open_browser(help_url)
                    item_arg.add_to_wf(wf)
                elif not mfa_token.isdigit():  # example: "a_valid_profile abcdef"
                    item_arg = ItemArgs(
                        title="MFA Token has to be 6 digits!".format(mfa_token),
                        subtitle="Doc: {}".format(help_url),
                        icon=HotIcons.error,
                        valid=True,
                    )
                    item_arg.open_browser(help_url)
                    item_arg.add_to_wf(wf)
                else:  # example: "a_valid_profile 123456"
                    cmd = "{} {} {}".format(
                        self.mh_execute_mfa_auth.__name__,
                        profile_name,
                        mfa_token,
                    )
                    item_arg = ItemArgs(
                        title="Do MFA auth using token '{}'".format(mfa_token),
                        subtitle="hit 'Enter' to execute MFA auth",
                        icon=HotIcons.run,
                        valid=True,
                    )
                    item_arg.run_script(cmd)
                    item_arg.notify(title="create/update mfa profile", subtitle="{}_mfa".format(profile_name))
                    item_arg.add_to_wf(wf)
        else:
            item_arg = ItemArgs(
                title="Invalid arg: '{}'".format(query_str),
                subtitle="valid arg: '{aws_profile_name} {six_digit_mfa_token}'",
                icon=HotIcons.error,
                valid=True,
            )
            item_arg.add_to_wf(wf)
        return wf

    # ------ aws-tool-set-profile script filter implementation ------
    def mh_set_aws_profile_as_aws_tools_default(self, wf, query_str):
        """
        :type wf: Workflow3
        :type query_str: str
        """
        settings[SettingKeys.aws_profile] = query_str

    def mh_select_aws_profile_to_set_as_aws_tools_default(self, wf, query_str):
        """
        :type wf: Workflow3
        :type query_str: str
        """
        aws_profile_list = item_filters.aws_profile(
            query_str=query_str,
            aws_config_file=self.aws_config_file.abspath,
        )
        item_builders.set_aws_profile_as_aws_tools_default(
            wf=wf,
            aws_profile_list=aws_profile_list,
            set_aws_profile_as_aws_tools_default_handler_id=self.mh_set_aws_profile_as_aws_tools_default.__name__,
        )
        return wf

    # ------ aws-tool-set-region script filter implementation ------
    def mh_set_aws_region_as_aws_tools_default(self, wf, query_str):
        """
        :type wf: Workflow3
        :type query_str: str
        """
        settings[SettingKeys.aws_region] = query_str

    def mh_select_aws_region_to_set_as_aws_tools_default(self, wf, query_str):
        """
        :type wf: Workflow3
        :type query_str: str
        """
        all_regions = item_filters.aws_region(
            query_str=query_str,
        )
        item_builders.set_aws_region_as_aws_tools_default(
            wf=wf,
            all_regions=all_regions,
            set_aws_region_as_aws_tools_default_handler_id=self.mh_set_aws_region_as_aws_tools_default.__name__,
        )
        return wf

aws_profile_handlers = AWSProfileHandlers()
