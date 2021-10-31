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

reg.check_in(Ec2InstancesSearcher())
reg.check_in(Ec2SecurityGroupsSearcher())
