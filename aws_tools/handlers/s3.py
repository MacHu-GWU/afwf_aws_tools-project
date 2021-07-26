# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import workflow
from typing import List, Tuple, Dict
from datetime import datetime
from .. import icons
from ..credential import read_all_aws_profile
from ..boto_ses import create_boto_ses
from ..settings import settings, Keys
from ..helpers import tokenize


def _list_bucket(boto_ses):
    """
    :rtype: List[Tuple[str, str]]
    """
    s3_client = boto_ses.client("s3")
    res = s3_client.list_buckets()
    result = list()
    for bucket_dct in res["Buckets"]:
        bucket_name = bucket_dct["Name"]  # type: datetime
        creation_date = bucket_dct["CreationDate"]
        result.append((bucket_name, str(creation_date)))
    return result


def list_bucket(wf, args=None):
    """
    :type wf: workflow.Workflow3
    :type args: list[str]
    """
    boto_ses = create_boto_ses()

    if args is None:
        args = wf.args[1:]

    n_args = len(args)

    # No argument behavior
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets
    if n_args == 0:
        for bucket_name, creation_date in _list_bucket(boto_ses):
            title = bucket_name
            subtitle = "Open S3 Console in Browser for Bucket '{}'".format(bucket_name)
            autocomplete = bucket_name
            arg = bucket_name
            valid = True
            match = " ".join(tokenize(bucket_name))
            wf.add_item(
                title=title,
                subtitle=subtitle,
                autocomplete=autocomplete,
                arg=arg,
                valid=valid,
                match=match,
                icon=icons.ICON_S3,
            )

    return wf
