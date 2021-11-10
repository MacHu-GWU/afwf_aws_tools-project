# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...settings import SettingValues
from ...cache import cache
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Bucket(ResData):
    name = attr.ib()
    create_date = attr.ib()

    @property
    def id(self):
        return self.name

    def to_console_url(self):
        return "https://s3.console.aws.amazon.com/s3/buckets/{name}?region={region}&tab=objects".format(
            name=self.name,
            region=SettingValues.aws_region,
        )

    @property
    def arn(self):
        return "arn:aws:s3:::{}".format(self.name)


class S3BucketsSearcher(AwsResourceSearcher):
    id = "s3-buckets"

    def simplify_response(self, res):
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

    @cache.memoize(expire=SettingValues.cache_expire)
    def list_res(self):
        """
        :rtype: list[Bucket]
        """
        res = self.sdk.s3_client.list_buckets()
        bucket_list = self.simplify_response(res)
        bucket_list = list(sorted(
            bucket_list, key=lambda b: b.name
        ))
        return bucket_list

    @cache.memoize(expire=SettingValues.cache_expire)
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
        item_arg = ItemArgs(
            title=bucket.name,
            subtitle="Create at {create_date}".format(
                create_date=bucket.create_date
            ),
            autocomplete="{} {}".format(self.resource_id, bucket.name),
            arg=console_url,
            largetext=bucket.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(bucket.arn)
        item_arg.copy_id(bucket.id)
        return item_arg


s3_bucket_searcher = S3BucketsSearcher()
