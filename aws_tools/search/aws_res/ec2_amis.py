# -*- coding: utf-8 -*-

"""
Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images
"""

from __future__ import unicode_literals
import attr
from ..aws_resources import ResData, AwsResourceSearcher, ItemArgs
from ...icons import find_svc_icon
from ...settings import SettingValues
from ...cache import cache
from ...helpers import union, intersect, tokenize


@attr.s(hash=True)
class Image(ResData):
    id = attr.ib()
    name = attr.ib()
    description = attr.ib()
    platform = attr.ib()
    arch = attr.ib()
    state = attr.ib()
    create_date = attr.ib()

    @property
    def short_id(self):
        return self.id[:8] + "..." + self.id[-4:]

    def to_console_url(self):
        return "https://console.aws.amazon.com/ec2/home?region={region}#Images:visibility=owned-by-me;search={ami_id};sort=name".format(
            ami_id=self.id,
            region=SettingValues.aws_region,
        )

    def to_largetext(self):
        return "\n".join([
            "id = {}".format(self.id),
            "name = {}".format(self.name),
            "description = {}".format(self.description),
            "platform = {}".format(self.platform),
            "arch = {}".format(self.arch),
            "state = {}".format(self.state),
            "create_date = {}".format(self.create_date),
        ])


class Ec2AmiSearcher(AwsResourceSearcher):
    id = "ec2-amis"

    def simplify_response(self, res):
        """
        :type res: dict
        :param res: the return of ec2_client.describe_images

        :rtype: list[SecurityGroup]
        """
        image_list = list()
        for image_dict in res["Images"]:
            image = Image(
                id=image_dict["ImageId"],
                name=image_dict["Name"],
                description=len(image_dict["Description"]),
                platform=image_dict["PlatformDetails"],
                arch=image_dict["Architecture"],
                state=image_dict["State"],
                create_date=len(image_dict["CreationDate"]),
            )
            image_list.append(image)
        image_list = list(sorted(image_list, key=lambda i: i.create_date, reverse=True))
        return image_list

    @cache.memoize(expire=SettingValues.expire)
    def list_res(self):
        """
        :rtype: list[Image]
        """
        res = self.sdk.ec2_client.describe_images(Owners=["self", ])
        return self.simplify_response(res)

    @cache.memoize(expire=SettingValues.expire)
    def filter_res(self, query_str):
        """
        :type query_str: str
        :rtype: list[Image]
        """
        args = tokenize(query_str)
        if len(args) == 1:
            filter_ = dict(Name="name", Values=["*{}*".format(args[0])])
            res = self.sdk.ec2_client.describe_images(
                Owners=["self", "amazon"],
                Filters=[filter_, ],
            )
            image_list_by_name = self.simplify_response(res)

            filter_ = dict(Name="image-id", Values=["*{}*".format(args[0])])
            res = self.sdk.ec2_client.describe_images(
                Owners=["self", "amazon"],
                Filters=[filter_, ],
            )
            image_list_by_id = self.simplify_response(res)

            image_list = union(image_list_by_name, image_list_by_id)
            return image_list
        elif len(args) > 1:
            image_list_list = [self.filter_res(query_str=arg) for arg in args]
            image_list = intersect(*image_list_list)
            return image_list
        else:
            raise Exception

    def to_item(self, image):
        """
        :type image: Image
        :rtype: ItemArgs
        """
        console_url = image.to_console_url()
        largetext = image.to_largetext()
        item_arg = ItemArgs(
            title="{image_id} {platform}".format(
                image_id=image.short_id,
                platform=image.platform,
            ),
            subtitle="{image_name}".format(
                image_name=image.name,
            ),
            autocomplete="{} {}".format(self.resource_id, image.id),
            arg=console_url,
            largetext=largetext,
            icon=find_svc_icon(self.id),
            valid=True,
        )
        item_arg.open_browser(console_url)
        return item_arg

ec2_amis_searcher = Ec2AmiSearcher()
