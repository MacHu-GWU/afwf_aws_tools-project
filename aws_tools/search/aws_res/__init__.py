# -*- coding: utf-8 -*-

from ...register import Registry
from ..aws_resources import AwsResourceSearcher


class AwsResourceSearcherRegistry(Registry):
    def get_key(self, obj):
        """
        :type obj: AwsResourceSearcher
        :rtype: str
        """
        return obj.id


aws_res_sr_registry = AwsResourceSearcherRegistry()
reg = aws_res_sr_registry

# --- Register your AWS Resource Searcher here ---
from .ec2_instances import ec2_instances_searcher
from .ec2_securitygroups import ec2_securitygroups_searcher
from .ec2_amis import ec2_amis_searcher
from .ec2_volumes import ec2_volumns_searcher
from .vpc_vpcs import vpc_vpcs_searcher
from .vpc_subnets import vpc_subnets_searcher
from .iam_roles import iam_roles_searcher
from .iam_policies import iam_policies_searcher
from .iam_users import iam_users_searcher
from .glue_databases import glue_databases_searcher
from .glue_tables import glue_tables_searcher
from .glue_jobs import glue_job_searcher
from .glue_awsgluestudio import glue_studiojob_searcher
from .s3_buckets import s3_bucket_searcher
from .lambda_functions import lambda_functions_searcher
from .lambda_layers import lambda_layers_searcher
from .lakeformation_databases import lakeformation_databases_searcher
from .lakeformation_tables import lakeformation_tables_searcher
from .cloudformation_stacks import cloudformation_stacks_searcher
from .dynamodb_tables import dynamodb_tables_searcher
from .dynamodb_items import dynamodb_items_searcher
from .rds_databases import rds_databases_searcher
from .sqs_queues import sqs_queues_searcher
from .kms_awsmanagedkeys import kms_awsmanagedkeys_searcher
from .kms_customermanagedkeys import kms_customermanagedkeys_searcher

reg.check_in(ec2_instances_searcher)
reg.check_in(ec2_securitygroups_searcher)
reg.check_in(ec2_amis_searcher)
reg.check_in(ec2_volumns_searcher)
reg.check_in(vpc_vpcs_searcher)
reg.check_in(vpc_subnets_searcher)
reg.check_in(iam_roles_searcher)
reg.check_in(iam_policies_searcher)
reg.check_in(iam_users_searcher)
reg.check_in(glue_databases_searcher)
reg.check_in(glue_tables_searcher)
reg.check_in(glue_job_searcher)
reg.check_in(glue_studiojob_searcher)
reg.check_in(s3_bucket_searcher)
reg.check_in(lambda_functions_searcher)
reg.check_in(lambda_layers_searcher)
reg.check_in(lakeformation_databases_searcher)
reg.check_in(lakeformation_tables_searcher)
reg.check_in(cloudformation_stacks_searcher)
reg.check_in(dynamodb_tables_searcher)
reg.check_in(dynamodb_items_searcher)
reg.check_in(rds_databases_searcher)
reg.check_in(sqs_queues_searcher)
reg.check_in(kms_awsmanagedkeys_searcher)
reg.check_in(kms_customermanagedkeys_searcher)
