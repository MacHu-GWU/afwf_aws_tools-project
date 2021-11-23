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
        self._account_id = None

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

    @property
    def account_id(self):
        if self._account_id is None:
            res = self.sts_client.get_caller_identity()
            self._account_id = res["Account"]
        return self._account_id

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
    def rds_client(self):
        return self._get_client("rds")

    @property
    def lambda_client(self):
        return self._get_client("lambda")

    @property
    def iam_client(self):
        return self._get_client("iam")

    @property
    def glue_client(self):
        return self._get_client("glue")

    @property
    def cft_client(self):
        return self._get_client("cloudformation")

    @property
    def dynamodb_client(self):
        return self._get_client("dynamodb")

    @property
    def sts_client(self):
        return self._get_client("sts")

    @property
    def sqs_client(self):
        return self._get_client("sqs")

    @property
    def sns_client(self):
        return self._get_client("sns")

    @property
    def ses_client(self):
        return self._get_client("ses")

    @property
    def kms_client(self):
        return self._get_client("kms")

    @property
    def sm_client(self):
        return self._get_client("secretsmanager")

    @property
    def c9_client(self):
        return self._get_client("cloud9")


sdk = SDK()
