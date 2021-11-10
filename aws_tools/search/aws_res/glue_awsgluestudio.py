# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_jobs
"""

from __future__ import unicode_literals
from ..aws_resources import ItemArgs
from ...settings import SettingValues
from .glue_jobs import Job, GlueJobSearcher


def to_console_url(job):
    """
    :type job: Job
    """
    return "https://console.aws.amazon.com/gluestudio/home?region={region}#/editor/job/{job_name}/script".format(
        job_name=job.name,
        region=SettingValues.aws_region,
    )


class GlueStudioJobSearcher(GlueJobSearcher):
    id = "glue-awsgluestudio"

    def to_item(self, job):
        """
        :type job: Job
        :rtype: ItemArgs
        """
        item_arg = super(GlueStudioJobSearcher, self).to_item(job)
        console_url = to_console_url(job)
        item_arg.title = "GlueJob({})".format(job.name)
        item_arg.arg = console_url
        item_arg.open_browser(console_url)
        item_arg.copy_id(job.id)
        return item_arg


glue_studiojob_searcher = GlueStudioJobSearcher()
