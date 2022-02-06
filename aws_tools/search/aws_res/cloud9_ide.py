# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.list_environments
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.describe_environments
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ItemArgs
from . import cloud9_environments


@attr.s(hash=True)
class Environment(cloud9_environments.Environment):
    def to_console_url(self):
        return "https://{domain}/cloud9/ide/{id}".format(
            domain=SettingValues.get_console_domain(),
            id=self.id,
        )


class Cloud9IdeSearcher(cloud9_environments.Cloud9EnvironmentsSearcher):
    id = "cloud9-ide"

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of lambda_client.list_envtions

        :rtype: list[Environment]
        """
        env_list = super(Cloud9IdeSearcher, self).simplify_response(res)
        return [
            Environment(**env.to_dict())
            for env in env_list
        ]

    def to_item(self, env):
        """
        :type env: Environment
        :rtype: ItemArgs
        """
        console_url = env.to_console_url()
        item_arg = ItemArgs(
            title="Open IDE for {env_name} Id({env_id})".format(
                env_name=env.name,
                env_id=env.id,
            ),
            subtitle="{state} {description}".format(
                state=cloud9_environments.env_state_emoji_mapper.get(env.status, "❓"),
                description=env.description
            ),
            autocomplete="{} {}".format(self.resource_id, env.id),
            arg=console_url,
            largetext=env.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(env.arn)
        item_arg.copy_id(env.id)
        return item_arg


cloud9_ide_searcher = Cloud9IdeSearcher()
