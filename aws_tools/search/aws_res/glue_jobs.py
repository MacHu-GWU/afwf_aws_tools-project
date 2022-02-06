# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_jobs
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Job(ResData):
    name = attr.ib()
    description = attr.ib()
    create_on = attr.ib()
    last_modified_on = attr.ib()
    worker_type = attr.ib()
    glue_version = attr.ib()

    @property
    def id(self):
        return self.name

    def to_console_url(self):
        return "https://{domain}/glue/home?region={region}#etl:tab=jobs".format(
            domain=SettingValues.get_console_domain(),
            region=SettingValues.aws_region,
        )


class GlueJobSearcher(AwsResourceSearcher):
    id = "glue-jobs"

    limit_arg_name = "MaxResults"
    paginator_arg_name = "NextToken"

    def boto3_call(self, **kwargs):
        return self.sdk.glue_client.get_jobs(**kwargs)

    def get_paginator(self, res):
        return res.get("NextToken")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of glue_client.get_tables

        :rtype: list[Job]
        """
        job_list = list()
        for job_dict in res["Jobs"]:
            tb = Job(
                name=job_dict["Name"],
                description=job_dict.get("Description"),
                create_on=str(job_dict["CreatedOn"]),
                last_modified_on=str(job_dict["LastModifiedOn"]),
                worker_type=job_dict["WorkerType"],
                glue_version=job_dict["GlueVersion"],
            )
            job_list.append(tb)
        return job_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self, limit=SettingValues.search_limit):
        """
        :rtype: list[Job]
        """
        job_list = self.recur_list_res(limit=limit)
        job_list = list(sorted(
            job_list, key=lambda j: j.last_modified_on, reverse=True,
        ))
        return job_list

    @cache.memoize(expire=SettingValues.cache_expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[typing.Union[Database, Table]]
        """
        job_list = self.list_res(limit=1000)
        keys = [job.name for job in job_list]
        mapper = {job.name: job for job in job_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_job_list = fz_sr.match(query_str, limit=20)
        return matched_job_list

    def to_item(self, job):
        """
        :type job: Job
        :rtype: ItemArgs
        """
        console_url = job.to_console_url()
        item_arg = ItemArgs(
            title=job.name,
            subtitle="{description}".format(
                description=job.description
            ),
            autocomplete="{} {}".format(self.resource_id, job.name),
            arg=console_url,
            largetext=job.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_id(job.id)
        return item_arg


glue_job_searcher = GlueJobSearcher()
