# -*- coding: utf-8 -*-

import boto3
from .settings import settings, Keys

def create_boto_ses():
    return boto3.session.Session(
        profile_name=settings[Keys.aws_profile],
        region_name=settings[Keys.aws_region],
    )
