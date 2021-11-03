# -*- coding: utf-8 -*-

"""
All workflow handlers for ``aws`` trigger.
"""

from __future__ import unicode_literals, print_function
from workflow.workflow3 import Workflow3
from ..alfred import ItemArgs
from ..icons import HotIcons, find_svc_icon
from ..search.aws_res import reg
from ..search.aws_resources import AwsResourceSearcher
from ..search.aws_urls import main_service_searcher, sub_service_searcher
from ..settings import SettingValues
from ..paths import DIR_AWS_TOOL_USER_DATA


def main_svc_doc_to_item(doc):
    """
    Convert a MainServiceSchema whoosh document (dict) to
    an alfred :class:`ItemArgs` object.

    :type doc: dict
    :param doc: MainServiceSchema document

    :rtype: ItemArgs
    """
    title = doc["id"]
    subtitle = "{emoji}{name}{shortname}{description}".format(
        emoji="📂" if doc["has_sub_svc"] else "",
        name=doc["name"],
        shortname=" ({})".format(doc.get("short_name")) if doc.get("short_name") else "",
        description=" - {}".format(doc.get("description")) if doc.get("description") else "",
    )
    autocomplete = title + "-" if doc["has_sub_svc"] else title
    console_url = "https://console.aws.amazon.com" + doc["url"].format(region=SettingValues.aws_region)
    arg = console_url
    item_arg = ItemArgs(
        title=title,
        subtitle=subtitle,
        autocomplete=autocomplete,
        arg=arg,
        icon=find_svc_icon(doc["id"]),
        valid=True,
    )
    item_arg.open_browser(console_url)
    return item_arg


def sub_svc_doc_to_item(doc, main_svc_id):
    """
    Convert sub service whoosh document (dict) to
    an alfred :class:`ItemArgs` item object.

    :type doc: dict
    :param doc: SubServiceSchema document

    :type main_svc_id: str

    :rtype: ItemArgs
    """
    sub_svc_id = doc["id"]
    title = "{}-{}".format(main_svc_id, sub_svc_id)
    aws_res_searcher_id = title
    subtitle = "{emoji}{name}{shortname}{description}".format(
        emoji="🔍" if reg.has(aws_res_searcher_id) else "",
        name=doc["name"],
        shortname=" ({})".format(doc.get("short_name")) if doc.get("short_name") else "",
        description=" - {}".format(doc.get("description")) if doc.get("description") else "",
    )
    autocomplete = title + " " if reg.has(aws_res_searcher_id) else title
    console_url = "https://console.aws.amazon.com" + doc["url"].format(region=SettingValues.aws_region)
    arg = console_url
    item_arg = ItemArgs(
        title=title,
        subtitle=subtitle,
        autocomplete=autocomplete,
        arg=arg,
        icon=find_svc_icon(title),
        valid=True,
    )
    item_arg.open_browser(console_url)
    return item_arg


def update_wf_for_main_svc_doc(
        wf,
        doc_list,
):
    """
    :type wf: Workflow3
    :type doc_list: list[dict]
    """
    for doc in doc_list:
        item_arg = main_svc_doc_to_item(doc)
        item_arg.add_to_wf(wf)


def update_wf_for_sub_svc_doc(
        wf,
        doc_list,
):
    """
    :type wf: Workflow3
    :type doc_list: list[dict]
    """
    for doc in doc_list:
        item_arg = sub_svc_doc_to_item(doc, main_svc_id=doc["main_svc_id"])
        item_arg.add_to_wf(wf)


class AwsHandlers(object):
    """
    All workflow handlers for ``aws`` trigger.
    """

    def sh_help_info(self, wf):
        """
        :type wf: Workflow3
        """
        yaml_url = "https://github.com/MacHu-GWU/afwf_aws_tools-project/blob/main/devtools/console-urls.yml"
        item_arg = ItemArgs(
            title="Search for an AWS Service",
            subtitle="example: ec2, vpc, s3, iam ...",
        )
        item_arg.open_browser(yaml_url)
        item_arg.add_to_wf(wf)
        return wf

    def sh_top20_main_service(self, wf):
        """
        :type wf: Workflow3
        """
        doc_list = main_service_searcher.top_20()
        update_wf_for_main_svc_doc(wf, doc_list)
        if len(doc_list) == 0:
            item_arg = ItemArgs(
                title="First you need to build index for AWS console url search",
                subtitle="hit 'Enter' to build the index",
                icon=HotIcons.info,
                valid=True,
            )
            cmd = "/usr/bin/python main.py '{} {}'".format("mh_rebuild_index", "do-build-index")
            item_arg.run_script(cmd)
            item_arg.open_file(path=DIR_AWS_TOOL_USER_DATA.abspath)
            item_arg.notify(title="AWS Console url index is rebuilt!")
            item_arg.add_to_wf(wf)
        return wf

    def sh_query_too_short(self, wf):
        """
        :type wf: Workflow3
        """
        item_arg = ItemArgs(
            title="Query is too Short!",
            subtitle="please enter at least two character to search for service, e.g. 's3'",
            icon=HotIcons.error,
            valid=True,
        )
        item_arg.add_to_wf(wf)
        return wf

    def sh_filter_main_service(self, wf, query_str):
        """
        :type wf: Workflow3
        :type query_str: str
        """
        doc_list = main_service_searcher.search(query_str=query_str, limit=20)
        update_wf_for_main_svc_doc(wf, doc_list)
        if len(doc_list) == 0:
            item_arg = ItemArgs(
                title="Found no service match '{}'".format(query_str),
                icon=HotIcons.info,
                valid=True,
            )
            item_arg.add_to_wf(wf)
        return wf

    def sh_get_one_main_service(self, wf, main_svc_id):
        """
        :type wf: Workflow3
        :type main_svc_id: str
        """
        doc = main_service_searcher.search_one(id=main_svc_id)
        if doc is None:
            item_arg = ItemArgs(
                title="Found no service match '{}'".format(main_svc_id),
                icon=HotIcons.info,
                valid=True,
            )
            item_arg.add_to_wf(wf)
        else:
            update_wf_for_main_svc_doc(wf, [doc, ])
        return wf

    def sh_top20_sub_service(self, wf, main_svc_id):
        """
        :type wf: Workflow3
        :type main_svc_id: str
        """
        doc_list = sub_service_searcher.top_20(main_svc_id)
        update_wf_for_sub_svc_doc(wf, doc_list)
        return wf

    def sh_filter_sub_service(self, wf, main_svc_id, query_str):
        """
        :type wf: Workflow3
        :type main_svc_id: str
        :type query_str: str
        """
        doc_list = sub_service_searcher.search(
            main_svc_id=main_svc_id, query_str=query_str, limit=20)
        update_wf_for_sub_svc_doc(wf, doc_list)
        if len(doc_list) == 0:
            item_arg = ItemArgs(
                title="Found no service match '{}-{}'".format(main_svc_id, query_str),
                icon=HotIcons.info,
                valid=True,
            )
            item_arg.add_to_wf(wf)
        return wf

    def sh_get_one_sub_service(self, wf, main_svc_id, sub_svc_id):
        """
        :type wf: Workflow3
        :type main_svc_id: str
        :type sub_svc_id: str
        """
        doc = sub_service_searcher.search_one(main_svc_id, sub_svc_id)
        update_wf_for_sub_svc_doc(wf, [doc, ])
        return wf

    def sh_list_aws_resources(self, wf, searcher_id):
        """
        :type wf: Workflow3
        :type searcher_id: str
        """
        searcher = reg.get(searcher_id) # type: AwsResourceSearcher
        results = searcher.list_res()
        for data in results:
            item_arg = searcher.to_item(data)
            item_arg.add_to_wf(wf)
        return wf

    def sh_filter_aws_resources(self, wf, searcher_id, query_str):
        """
        Example input:

            searcher_id = "ec2-instances"
            query_str = "dev jumpbox"

        :type wf: Workflow3
        :type searcher_id: str
        :type query_str: str
        """
        if reg.has(searcher_id):
            searcher = reg.get(searcher_id) # type: AwsResourceSearcher
            results = searcher.filter_res(query_str)

            # Some service console has built-in restful search url
            # For example, ec2-instances, vpc-subnets
            # The default hit 'Enter' behavior is to open the exact url
            # point to one specific resource. But in this case, user may want
            # to use the search box to filter the results in console as well
            if searcher.has_search_box:
                console_url = searcher.to_search_url(query_str=query_str)
                item_args = ItemArgs(
                    title="Search '{query_str}' in {svc_id} console".format(
                        query_str=query_str,
                        svc_id=searcher.id,
                    ),
                    subtitle="hit 'Enter' jump to console",
                    arg=console_url,
                    icon=searcher.icon,
                    valid=True,
                )
                item_args.open_browser(url=console_url)
                item_args.add_to_wf(wf)
            for data in results:
                item_args = searcher.to_item(data)
                item_args.add_to_wf(wf)
            if len(results) == 0:
                item_args = ItemArgs(
                    title="Found nothing",
                    subtitle="query has to be sub string of the name or id",
                    icon=HotIcons.info,
                    valid=True,
                )
                item_args.add_to_wf(wf)
        else:
            item_args = ItemArgs(
                title="It is not a valid service id '{}'".format(searcher_id),
                icon=HotIcons.info,
                valid=True,
            )
            item_args.add_to_wf(wf)
        return wf

    def mh_aws(self, wf, query_str):
        """
        :type wf: Workflow3
        :type query_str: str
        """
        args = [arg for arg in query_str.split(" ") if arg.strip()]
        if len(args) == 0:  # query = " " or ""
            self.sh_help_info(wf)
            self.sh_top20_main_service(wf)
        elif len(args) == 1:
            svc_id = args[0]
            if len(svc_id) == 1:  # query = "e"
                self.sh_query_too_short(wf)
            elif query_str.endswith(" "):
                if reg.has(svc_id):  # query = "ec2-instances "
                    self.sh_list_aws_resources(wf, svc_id)
                else:  # query = "ec2-limits "
                    return self.mh_aws(wf=wf, query_str=query_str.rstrip())
            elif "-" not in svc_id:  # query = "ec2":
                self.sh_filter_main_service(wf, svc_id)
            elif "-" in svc_id:
                if svc_id.endswith("-"):  # query = "ec2-"
                    main_svc_id = svc_id[:-1]
                    self.sh_top20_sub_service(wf, main_svc_id)
                else:
                    main_svc_id, query_str = svc_id.split("-", 1)
                    if len(query_str) == 1:  # query = "ec2-i"
                        self.sh_get_one_main_service(wf, main_svc_id)
                        self.sh_query_too_short(wf)
                    else:  # query = "ec2-ins"
                        self.sh_filter_sub_service(wf, main_svc_id, query_str)
            else:
                raise ValueError
        elif len(args) == 2:
            searcher_id, res_query = args
            self.sh_filter_aws_resources(wf, searcher_id, res_query)
        else:
            searcher_id = args[0]
            res_query = " ".join(args[1:])
            self.sh_filter_aws_resources(wf, searcher_id, res_query)

        return wf


aws_handlers = AwsHandlers()
