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
from .iam_roles import IamRolesSearcher
from .iam_policies import IamPolicysSearcher
from .glue_databases import GlueDatabasesSearcher
from .glue_tables import GlueTablesSearcher
from .s3_buckets import S3BucketsSearcher

reg.check_in(Ec2InstancesSearcher())
reg.check_in(Ec2SecurityGroupsSearcher())
reg.check_in(Ec2AmiSearcher())
reg.check_in(IamRolesSearcher())
reg.check_in(IamPolicysSearcher())
reg.check_in(GlueDatabasesSearcher())
reg.check_in(GlueTablesSearcher())
reg.check_in(S3BucketsSearcher())
