# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.list_environments
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.describe_environments
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Environment(ResData):
    id = attr.ib()
    name = attr.ib()
    description = attr.ib()
    arn = attr.ib()
    owner_arn = attr.ib()
    status = attr.ib()

    def to_console_url(self):
        return "https://{domain}/cloud9/home/environments/{id}".format(
            domain=SettingValues.get_console_domain(),
            id=self.id,
        )

# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.describe_environments
env_state_emoji_mapper = {
    "CREATING": "🟡",
    "CREATED": "🟢",
    "CREATE_FAILED": "🔴️",
    "DELETING": "🟠",
    "DELETE_FAILED": "🔴️",
    "UNKNOWN": "🟤",
}


class Cloud9EnvironmentsSearcher(AwsResourceSearcher):
    id = "cloud9-environments"
    limit_arg_name = "maxResults"
    paginator_arg_name = "nextToken"

    def boto3_call(self, **kwargs):
        page_size = 25
        limit = 1000

        max_results = page_size if limit > page_size else limit
        paginator = None
        env_id_list = list()
        while 1:
            if kwargs is None:
                kwargs = dict()
            if self.limit_arg_name:
                kwargs[self.limit_arg_name] = max_results
            if paginator:
                kwargs[self.paginator_arg_name] = paginator

            response = self.sdk.c9_client.list_environments(**kwargs)
            env_id_list.extend(response.get("environmentIds", list()))
            paginator = self.get_paginator(response)

            n_res = len(env_id_list)
            if n_res >= limit:  # already got enough items
                break
            else:
                max_results = (limit - n_res) if (limit - n_res) < page_size else page_size

            if not paginator:  # no more items
                break

        return self.sdk.c9_client.describe_environments(environmentIds=env_id_list)

    def get_paginator(self, res):
        return res.get("nextToken")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of lambda_client.list_envtions

        :rtype: list[Environment]
        """
        env_list = list()
        for env_dict in res["environments"]:
            env = Environment(
                id=env_dict["id"],
                name=env_dict["name"],
                description=env_dict.get("description"),
                arn=env_dict.get("arn"),
                owner_arn=env_dict.get("ownerArn"),
                status=env_dict.get("lifecycle", dict()).get("status", "UNKNOWN"),
            )
            env_list.append(env)
        return env_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Environment]
        """
        env_list = self.recur_list_res(limit=limit)
        env_list = list(sorted(
            env_list, key=lambda env: env.name))
        return env_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Environment]
        """
        env_list = self.list_res(limit=1000)
        keys = [env.name for env in env_list]
        mapper = {env.name: env for env in env_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_env_list = fz_sr.match(query_str, limit=20)
        return matched_env_list

    def to_item(self, env):
        """
        :type env: Environment
        :rtype: ItemArgs
        """
        console_url = env.to_console_url()
        item_arg = ItemArgs(
            title="{env_name} Id({env_id})".format(
                env_name=env.name,
                env_id=env.id,
            ),
            subtitle="{state} {description}".format(
                state=env_state_emoji_mapper.get(env.status, "❓"),
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


cloud9_environments_searcher = Cloud9EnvironmentsSearcher()
