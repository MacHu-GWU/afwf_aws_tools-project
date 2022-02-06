# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.list_queues
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Queue(ResData):
    url = attr.ib()

    @property
    def id(self):
        return self.url

    @property
    def name(self):
        return self.url.split("/")[-1]

    @property
    def arn(self):
        chunks = self.url.split("/")
        endpoint = chunks[2]
        account_id = chunks[3]
        name = chunks[4]
        region = endpoint.split(".")[1]
        return "arn:aws:sqs:{region}:{account_id}:{name}".format(
            account_id=account_id,
            region=region,
            name=name,
        )

    def to_console_url(self):
        return "https://{domain}/sqs/v2/home?region={region}#/queues/{q_url}".format(
            domain=SettingValues.get_console_domain(),
            region=SettingValues.aws_region,
            q_url=self.url,
        )


class SqsQueuesSearcher(AwsResourceSearcher):
    id = "sqs-queues"
    limit_arg_name = "MaxResults"
    paginator_arg_name = "NextToken"

    def boto3_call(self, **kwargs):
        return self.sdk.sqs_client.list_queues(**kwargs)

    def get_paginator(self, res):
        return res.get("NextToken")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of sqs_client.list_queues

        :rtype: list[Queue]
        """
        queue_list = list()
        for queue_url in res["QueueUrls"]:
            queue = Queue(
                url=queue_url,
            )
            queue_list.append(queue)
        return queue_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Queue]
        """
        queue_list = self.recur_list_res(page_size=1000, limit=limit)
        return queue_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Queue]
        """
        queue_list = self.list_res(limit=1000)
        keys = [queue.name for queue in queue_list]
        mapper = {queue.name: queue for queue in queue_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_queue_list = fz_sr.match(query_str, limit=20)
        return matched_queue_list

    def to_item(self, queue):
        """
        :type queue: Queue
        :rtype: ItemArgs
        """
        console_url = queue.to_console_url()
        item_arg = ItemArgs(
            title=queue.name,
            autocomplete="{} {}".format(self.resource_id, queue.name),
            arg=console_url,
            largetext=queue.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(queue.arn)
        item_arg.copy_id(queue.name)
        return item_arg


sqs_queues_searcher = SqsQueuesSearcher()
