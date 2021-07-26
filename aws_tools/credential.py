# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import attr
from pathlib_mate import Path
import ConfigParser


# @attr.s
# class AWSProfile(object):
#     name = attr.ib()  # type: str
#     aws_access_key_id = attr.ib()  # type: str
#     aws_secret_access_key = attr.ib()  # type: str
#     region = attr.ib()  # type: str
#     output = attr.ib()  # type: str
#     aws_session_token = attr.ib(default=None)  # type: str


def read_all_aws_profile():
    """
    :rtype: list[AWSProfile]

    :return:
    """

    HOME = Path.home()

    aws_credential_file = Path(HOME, ".aws", "credentials")
    # aws_config_file = Path(HOME, ".aws", "config")

    aws_credential = ConfigParser.ConfigParser()
    aws_credential.readfp(open(aws_credential_file.abspath))

    # aws_config = ConfigParser.ConfigParser()  # type:
    # aws_config.readfp(open(aws_config_file.abspath))

    aws_profile_list = list()  # type: list[str]

    aws_credential_sections = aws_credential.sections()
    # aws_config_sections = aws_config.sections()

    for cred_section_name in aws_credential_sections:
        credential_data = dict(aws_credential.items(cred_section_name))
        # config_section_name = "profile {}".format(cred_section_name)
        # if config_section_name not in aws_config_sections:
        #     print("[{}] not found in ~/.aws/config file".format(config_section_name))
        #     continue
        # config_data = dict(aws_config.items(config_section_name))
        # aws_profile = AWSProfile(
        #     name=cred_section_name,
        #     aws_access_key_id=credential_data.get("aws_access_key_id"),
        #     aws_secret_access_key=credential_data.get("aws_secret_access_key"),
        #     region=config_data.get("region"),
        #     output=config_data.get("output"),
        #     aws_session_token=credential_data.get("aws_session_token"),
        # )
        aws_profile = cred_section_name
        aws_profile_list.append(aws_profile)

    return aws_profile_list

# Go https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html#Concepts.RegionsAndAvailabilityZones.Regions
# Copy the data
# Go https://www.tablesgenerator.com/markdown_tables
# File -> Paste Table data, delete other columns, keep only first two columns
all_regions = [
    ("US East (Ohio)", "us-east-2"),
    ("US East (N. Virginia)", "us-east-1"),
    ("US West (N. California)", "us-west-1"),
    ("US West (Oregon)", "us-west-2"),
    ("Africa (Cape Town)", "af-south-1"),
    ("Asia Pacific (Hong Kong)", "ap-east-1"),
    ("Asia Pacific (Mumbai)", "ap-south-1"),
    ("Asia Pacific (Osaka)", "ap-northeast-3"),
    ("Asia Pacific (Seoul)", "ap-northeast-2"),
    ("Asia Pacific (Singapore)", "ap-southeast-1"),
    ("Asia Pacific (Sydney)", "ap-southeast-2"),
    ("Asia Pacific (Tokyo)", "ap-northeast-1"),
    ("Canada (Central)", "ca-central-1"),
    ("Europe (Frankfurt)", "eu-central-1"),
    ("Europe (Ireland)", "eu-west-1"),
    ("Europe (London)", "eu-west-2"),
    ("Europe (Milan)", "eu-south-1"),
    ("Europe (Paris)", "eu-west-3"),
    ("Europe (Stockholm)", "eu-north-1"),
    ("Middle East (Bahrain)", "me-south-1"),
    ("South America (São Paulo)", "sa-east-1"),
    ("AWS GovCloud (US-East)", "us-gov-east-1"),
    ("AWS GovCloud (US-West)", "us-gov-west-1"),
]