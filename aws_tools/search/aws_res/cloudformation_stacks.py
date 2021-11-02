# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.list_stacks
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Stack(ResData):
    id = attr.ib()
    name = attr.ib()
    create_time = attr.ib()
    update_time = attr.ib()
    delete_time = attr.ib()
    status = attr.ib()
    parent_id = attr.ib()
    root_id = attr.ib()

    def to_console_url(self):
        return "https://console.aws.amazon.com/cloudformation/home?region={region}#/stacks/stackinfo?filteringStatus=active&filteringText=&viewNested=true&hideStacks=false&stackId={stack_id}".format(
            stack_id=self.id,
            region=SettingValues.aws_region,
        )

stack_state_emoji_mapper = {
    "CREATE_IN_PROGRESS": "🟡",
    "CREATE_FAILED": "🔴",
    "CREATE_COMPLETE": "🟢",
    "ROLLBACK_IN_PROGRESS": "🟡",
    "ROLLBACK_FAILED": "🔴",
    "ROLLBACK_COMPLETE": "🟢",
    "DELETE_IN_PROGRESS": "🟡",
    "DELETE_FAILED": "🔴",
    "DELETE_COMPLETE": "🟢",
    "UPDATE_IN_PROGRESS": "🟡",
    "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS": "🟡",
    "UPDATE_COMPLETE": "🟢",
    "UPDATE_FAILED": "🔴",
    "UPDATE_ROLLBACK_IN_PROGRESS": "🟡",
    "UPDATE_ROLLBACK_FAILED": "🔴",
    "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS": "🟡",
    "UPDATE_ROLLBACK_COMPLETE": "🟢",
    "REVIEW_IN_PROGRESS": "🟡",
    "IMPORT_IN_PROGRESS": "🟡",
    "IMPORT_COMPLETE": "🟢",
    "IMPORT_ROLLBACK_IN_PROGRESS": "abcd",
    "IMPORT_ROLLBACK_FAILED": "🔴",
    "IMPORT_ROLLBACK_COMPLETE'": "🟢",
}


class CloudFormationStacksSearcher(AwsResourceSearcher):
    id = "cloudformation-stacks"
    limit_arg_name = None
    paginator_arg_name = "NextToken"
    lister = AwsResourceSearcher.sdk.cft_client.list_stacks

    def get_paginator(self, res):
        return res.get("NextToken")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of iam_client.list_stacks

        :rtype: list[Stack]
        """
        stack_list = list()
        for stack_dict in res["StackSummaries"]:
            stack = Stack(
                id=stack_dict["StackId"],
                name=stack_dict["StackName"],
                create_time=str(stack_dict["CreationTime"]),
                update_time=str(stack_dict.get("LastUpdatedTime", "")),
                delete_time=str(stack_dict.get("DeletionTime", "")),
                status=stack_dict["StackStatus"],
                parent_id=stack_dict.get("ParentId"),
                root_id=stack_dict.get("RootId"),
            )
            stack_list.append(stack)
        return stack_list

    @cache.memoize(expire=SettingValues.expire)
    def list_res(self, limit=SettingValues.limit):
        """
        :rtype: list[Stack]
        """
        stack_list = self.recur_list_res()
        stack_list = list(sorted(
            stack_list, key=lambda r: r.update_time, reverse=True))
        return stack_list

    @cache.memoize(expire=SettingValues.expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Stack]
        """
        stack_list = self.list_res(limit=1000)
        keys = [stack.name for stack in stack_list]
        mapper = {stack.name: stack for stack in stack_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_stack_list = fz_sr.match(query_str, limit=20)
        return matched_stack_list

    def to_item(self, stack):
        """
        :type stack: Stack
        :rtype: ItemArgs
        """
        console_url = stack.to_console_url()
        largetext = stack.to_large_text()
        item_arg = ItemArgs(
            title="{stack_name}".format(
                stack_name=stack.name,
            ),
            subtitle="{status_emojii} {status}".format(
                status_emojii=stack_state_emoji_mapper.get(stack.status, "❓"),
                status=stack.status
            ),
            autocomplete="{} {}".format(self.resource_id, stack.name),
            arg=console_url,
            largetext=largetext,
            icon=find_svc_icon(self.id),
            valid=True,
        )
        item_arg.open_browser(console_url)
        return item_arg

cloudformation_stacks_searcher = CloudFormationStacksSearcher()
