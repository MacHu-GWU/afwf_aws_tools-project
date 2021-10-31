# -*- coding: utf-8 -*-

from ..aws_resources import AwsResourceSearcher


class Register(object):
    """
    """

    def __init__(self):
        self.mapper = dict()

    def register_searcher(self, searcher):
        """
        :type searcher_class: AwsResourceSearcher
        """
        if searcher.id is None:
            raise ValueError
        if searcher.id in self.mapper:
            raise ValueError
        self.mapper[searcher.id] = searcher

    def get(self, id):
        """
        :rtype: AwsResourceSearcher
        """
        if id not in self.mapper:
            raise KeyError
        return self.mapper[id]

    def has_id(self, id):
        return id in self.mapper


register = Register()

# --- Register your AWS Resource Searcher here ---
from .ec2_instances import Ec2InstancesSearcher

register.register_searcher(Ec2InstancesSearcher())
