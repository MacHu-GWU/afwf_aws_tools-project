# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from aws_tools.search.aws_urls import main_service_searcher, sub_service_searcher


class TestMainServiceSearcher(object):
    def test_build_index(self):
        main_service_searcher.build_index(force_rebuild=True)

    def test_search_one(self):
        doc = main_service_searcher.search_one(id="ec2")
        assert doc["id"] == "ec2"

        doc = main_service_searcher.search_one(id="not-valid-id")
        assert doc is None

    def test_top_20(self):
        ids = [doc["id"] for doc in main_service_searcher.top_20()]
        assert ids[:5] == ["ec2", "iam", "s3", "vpc", "sns"]

    def test_search(self):
        ids = [doc["id"] for doc in main_service_searcher.search("ec", limit=5)]
        assert ids[:3] == ["ec2", "ecr", "ecs"]


class TestSubServiceSearcher(object):
    def test_build_index(self):
        sub_service_searcher.build_index(force_rebuild=True)

    def test_search_one(self):
        doc = sub_service_searcher.search_one(main_svc_id="ec2", sub_svc_id="instances")
        assert doc["id"] == "instances"

        doc = sub_service_searcher.search_one(main_svc_id="ec2", sub_svc_id="not-valid-id")
        assert doc is None

    def test_top_20(self):
        ids = [doc["id"] for doc in sub_service_searcher.top_20(main_svc_id="ec2")]
        assert ids[:3] == ["instances", "securitygroups", "amis"]

    def test_search(self):
        ids = [doc["id"] for doc in sub_service_searcher.search(
            main_svc_id="ec2", query_str="ins", limit=5)]
        assert ids[:3] == ["instances", "instancetypes", "reservedinstances"]


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
