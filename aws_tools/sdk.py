# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import boto3
from .settings import settings, SettingKeys

class SDK(object):
    """
    AWS boto3 SDK helper class. Simplify boto session, service client creation
    and reuse.
    """

    def __init__(self):
        self._boto_ses = None
        self._client_cache = dict()

    @property
    def boto_ses(self):
        """
        Create the boto3 session for Alfred Workflow handler.

        :rtype: boto3.session.Session
        """

        if self._boto_ses is None:
            self._boto_ses = boto3.session.Session(
                profile_name=settings.get(SettingKeys.aws_profile),
                region_name=settings.get(SettingKeys.aws_region),
            )
        return self._boto_ses

    def _get_client(self, service_name):
        if self._client_cache.get(service_name) is None:
            self._client_cache[service_name] = self.boto_ses.client(service_name)
        return self._client_cache[service_name]

    @property
    def s3_client(self):
        return self._get_client("s3")

    @property
    def ec2_client(self):
        return self._get_client("ec2")

    @property
    def lambda_client(self):
        return self._get_client("lambda")

    @property
    def iam_client(self):
        return self._get_client("iam")

    @property
    def glue_client(self):
        return self._get_client("glue")


sdk = SDK()
