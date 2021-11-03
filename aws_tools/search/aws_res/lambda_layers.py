# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_layers
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...cache import cache
from ...settings import SettingValues
from ...search.fuzzy import FuzzyObjectSearch


@attr.s(hash=True)
class Layer(ResData):
    name = attr.ib()
    arn = attr.ib()

    @property
    def id(self):
        return self.name

    def to_console_url(self):
        return "https://console.aws.amazon.com/lambda/home?region={region}#/layers/{layer_name}".format(
            layer_name=self.name,
            region=SettingValues.aws_region,
        )


class LambdaLayersSearcher(AwsResourceSearcher):
    id = "lambda-layers"
    limit_arg_name = "MaxItems"
    paginator_arg_name = "Marker"
    lister = AwsResourceSearcher.sdk.lambda_client.list_layers

    def get_paginator(self, res):
        return res.get("NextMarker")

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of lambda_client.list_layers

        :rtype: list[Layer]
        """
        layer_list = list()
        for layer_dict in res["Layers"]:
            layer = Layer(
                name=layer_dict["LayerName"],
                arn=layer_dict["LayerArn"],
            )
            layer_list.append(layer)
        return layer_list

    @cache.memoize(expire=SettingValues.expire)
    def list_res(self, limit=SettingValues.limit):
        """
        :rtype: list[Layer]
        """
        layer_list = self.recur_list_res(page_size=50, limit=limit)
        layer_list = list(sorted(
            layer_list, key=lambda r: r.name, reverse=True))
        return layer_list

    @cache.memoize(expire=SettingValues.expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Layer]
        """
        layer_list = self.list_res(limit=1000)
        keys = [layer.name for layer in layer_list]
        mapper = {layer.name: layer for layer in layer_list}
        fz_sr = FuzzyObjectSearch(keys, mapper)
        matched_layer_list = fz_sr.match(query_str, limit=20)
        return matched_layer_list

    def to_item(self, layer):
        """
        :type layer: Layer
        :rtype: ItemArgs
        """
        console_url = layer.to_console_url()
        item_arg = ItemArgs(
            title="{layer_name}".format(
                layer_name=layer.name,
            ),
            subtitle="{description}".format(
                description=layer.arn
            ),
            autocomplete="{} {}".format(self.resource_id, layer.name),
            arg=console_url,
            largetext=layer.to_large_text(),
            icon=self.icon,
            valid=True,
        )
        item_arg.open_browser(console_url)
        item_arg.copy_arn(layer.arn)
        return item_arg


lambda_layers_searcher = LambdaLayersSearcher()
