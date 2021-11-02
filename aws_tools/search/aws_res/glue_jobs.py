# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_jobs
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import Base, AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch
from .glue_databases import Database, glue_databases_searcher


@attr.s(hash=True)
class Job(Base):
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
        return "https://console.aws.amazon.com/glue/home?region={region}#etl:tab=jobs".format(
            region=SettingValues.aws_region,
        )

    def to_largetext(self):
        return "\n".join([
            "name = {}".format(self.name),
            "description = {}".format(self.description),
            "create_on = {}".format(self.create_on),
            "last_modified_on = {}".format(self.last_modified_on),
            "worker_type = {}".format(self.worker_type),
            "glue_version = {}".format(self.glue_version),
        ])


class GlueJobSearcher(AwsResourceSearcher):
    id = "glue-jobs"

    limit_arg_name = "MaxResults"
    paginator_arg_name = "NextToken"
    lister = AwsResourceSearcher.sdk.glue_client.get_jobs

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

    @cache.memoize(expire=SettingValues.expire)
    def list_res(self, limit=SettingValues.limit):
        """
        :rtype: list[Job]
        """
        job_list = self.recur_list_res(limit=limit)
        job_list = list(sorted(
            job_list, key=lambda j: j.last_modified_on, reverse=True,
        ))
        return job_list

    @cache.memoize(expire=SettingValues.expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[typing.Union[Database, Table]]
        """
        role_list = self.list_res(limit=1000)
        keys = [role.name for role in role_list]
        mapper = {role.name: role for role in role_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_role_list = fz_sr.match(query_str, limit=20)
        return matched_role_list

    def to_item(self, job):
        """
        :type job: Job
        :rtype: ItemArgs
        """
        console_url = job.to_console_url()
        largetext = job.to_largetext()
        item_arg = ItemArgs(
            title=job.name,
            subtitle="{description}".format(
                description=job.description
            ),
            autocomplete="{} {}".format(self.resource_id, job.name),
            arg=console_url,
            largetext=largetext,
            icon=find_svc_icon(self.id),
            valid=True,
        )
        item_arg.open_browser(console_url)
        return item_arg

glue_job_searcher = GlueJobSearcher()
