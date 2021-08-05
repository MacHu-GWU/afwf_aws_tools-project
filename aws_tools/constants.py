# -*- coding: utf-8 -*-

from __future__ import unicode_literals

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


class FollowUpActionKey:
    open_file = "open-file"
    open_url = "open-url"
    run_script = "run-script"
