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
from .ec2_instances import Ec2InstancesSearcher
from .ec2_securitygroups import Ec2SecurityGroupsSearcher
from .ec2_amis import Ec2AmiSearcher
from .ec2_volumes import Ec2VolumesSearcher
from .iam_roles import IamRolesSearcher
from .iam_policies import IamPolicysSearcher
from .iam_users import IamUsersSearcher
from .glue_databases import glue_databases_searcher
from .glue_tables import glue_tables_searcher
from .glue_jobs import glue_job_searcher
from .glue_awsgluestudio import glue_studiojob_searcher
from .s3_buckets import s3_bucket_searcher
from .lambda_functions import lambda_functions_searcher
from .lambda_layers import lambda_layers_searcher
from .lakeformation_databases import lakeformation_databases_searcher
from .lakeformation_tables import lakeformation_tables_searcher

reg.check_in(Ec2InstancesSearcher())
reg.check_in(Ec2SecurityGroupsSearcher())
reg.check_in(Ec2AmiSearcher())
reg.check_in(Ec2VolumesSearcher())
reg.check_in(IamRolesSearcher())
reg.check_in(IamPolicysSearcher())
reg.check_in(IamUsersSearcher())
reg.check_in(glue_databases_searcher)
reg.check_in(glue_tables_searcher)
reg.check_in(glue_job_searcher)
reg.check_in(glue_studiojob_searcher)
reg.check_in(s3_bucket_searcher)
reg.check_in(lambda_functions_searcher)
reg.check_in(lambda_layers_searcher)
reg.check_in(lakeformation_databases_searcher)
reg.check_in(lakeformation_tables_searcher)
