# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import attr
from ..aws_resources import AwsResourceSearcher, ItemArgs
from ...icons import Icons


@attr.s
class Image(object):
    id = attr.ib()
    name = attr.ib()
    description = attr.ib()
    platform = attr.ib()
    state = attr.ib()
    create_date = attr.ib()

    @property
    def short_id(self):
        return self.id[:8] + "..." + self.id[-4:]

    def to_console_url(self):
        return "https://console.aws.amazon.com/ec2/home#Images:visibility=owned-by-me;search={};sort=name".format(
            self.id)

    def to_largetext(self):
        return "\n".join([
            "id = {}".format(self.id),
            "name = {}".format(self.name),
            "description = {}".format(self.description),
            "platform = {}".format(self.platform),
            "state = {}".format(self.state),
            "create_date = {}".format(self.create_date),
        ])


def simplify_describe_images_response(res):
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
            state=image_dict["State"],
            create_date=len(image_dict["CreationDate"]),
        )
        image_list.append(image)
    return image_list


class Ec2AmiSearcher(AwsResourceSearcher):
    id = "ec2-amis"

    def list_res(self):
        """
        :rtype: list[Image]
        """
        res = self.sdk.ec2_client.describe_images(Owners=["self", ])
        return simplify_describe_images_response(res)

    def filter_res(self, query_str):
        """
        Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images

        :type query_str: str
        :rtype: list[Image]
        """
        filter_ = dict(Name="name", Values=["*{}*".format(query_str)])
        res_by_name = self.sdk.ec2_client.describe_images(
            Owners=["self", "amazon"],
            Filters=[filter_, ],
        )
        filter_ = dict(Name="image-id", Values=["*{}*".format(query_str)])
        res_by_id = self.sdk.ec2_client.describe_images(
            Owners=["self", "amazon"],
            Filters=[filter_, ],
        )

        # de-duplicate and sort
        image_list = simplify_describe_images_response(res_by_name) \
                     + simplify_describe_images_response(res_by_id)
        image_mapper = {
            image.id: image
            for image in image_list
        }
        image_list = list(sorted(image_mapper.values(), key=lambda x: x.name))
        return image_list

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
            icon=Icons.abspath(Icons.Res_Amazon_EC2_AMI),
            valid=True,
        )
        item_arg.open_browser(console_url)
        return item_arg
