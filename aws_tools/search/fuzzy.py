# -*- coding: utf-8 -*-

from fuzzywuzzy import process


class FuzzyObjectSearch(object):
    """
    :type keys: list[str]
    :type mapper: dict
    """

    def __init__(self, keys, mapper):
        self.keys = keys
        self.mapper = mapper

    def match(self, query, limit=20):
        """
        :rtype: list
        """
        return [
            self.mapper[key]
            for key, score in process.extract(query, self.keys, limit=limit)
        ]
