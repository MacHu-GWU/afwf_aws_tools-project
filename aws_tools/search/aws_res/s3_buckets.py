# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...settings import SettingValues
from ...cache import cache
from ...search.fuzzy import FuzzyObjectSearch


@attr.s
class Bucket(object):
    name = attr.ib()
    create_date = attr.ib()

    def to_console_url(self):
        return "https://s3.console.aws.amazon.com/s3/buckets/{name}?region={region}&tab=objects".format(
            name=self.name,
            region=SettingValues.aws_region,
        )

    @property
    def arn(self):
        return "arn:aws:s3:::{}".format(self.name)

    def to_largetext(self):
        return "\n".join([
            "name = {}".format(self.name),
            "create_date = {}".format(self.create_date),
            "arn = {}".format(self.arn),
        ])


def simplify_list_buckets_response(res):
    """
    :type res: dict
    :param res: the return of s3_client.list_buckets

    :rtype: list[Bucket]
    """
    bucket_list = list()
    for bucket_dict in res["Buckets"]:
        bucket = Bucket(
            name=bucket_dict["Name"],
            create_date=str(bucket_dict["CreationDate"]),
        )
        bucket_list.append(bucket)
    return bucket_list


class S3BucketsSearcher(AwsResourceSearcher):
    id = "s3-buckets"
    cache_key = "aws-res-s3-buckets"

    def list_bucket_dict(self):
        """
        :rtype list[dict]
        """
        res = self.sdk.s3_client.list_buckets()
        bucket_list = simplify_list_buckets_response(res)
        bucket_dict_list = [attr.asdict(bucket) for bucket in bucket_list]
        bucket_dict_list = list(sorted(
            bucket_dict_list, key=lambda d: d["create_date"], reverse=True
        ))
        return bucket_dict_list

    def list_res(self):
        """
        :rtype: list[Bucket]
        """
        bucket_dict_list = cache.fast_get(
            key=self.cache_key,
            callable=self.list_bucket_dict,
            expire=10,
        )
        bucket_list = [Bucket(**bucket_dict) for bucket_dict in bucket_dict_list]
        return bucket_list

    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Bucket]
        """
        bucket_list = self.list_res()
        keys = [bucket.name for bucket in bucket_list]
        mapper = {bucket.name: bucket for bucket in bucket_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_bucket_list = fz_sr.match(query_str, limit=20)
        return matched_bucket_list

    def to_item(self, bucket):
        """
        :type image: Bucket
        :rtype: ItemArgs
        """
        console_url = bucket.to_console_url()
        largetext = bucket.to_largetext()
        item_arg = ItemArgs(
            title=bucket.name,
            subtitle="Create at {create_date}".format(
                create_date=bucket.create_date
            ),
            autocomplete="{} {}".format(self.resource_id, bucket.name),
            arg=console_url,
            largetext=largetext,
            icon=find_svc_icon(self.id),
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(bucket.arn)
        return item_arg
