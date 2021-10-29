# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from .aws_fts import (
    main_service_searcher, sub_service_searcher,
    main_svc_doc_to_item, sub_svc_doc_to_item,
)
from workflow import ICON_ERROR
from .aws_resource_filters import filter_resources


def _aws_top20_main_service(wf):
    """
    Handler user input ``"aws"``
    """
    for doc in main_service_searcher.top_20():
        item = main_svc_doc_to_item(doc)
        wf.add_item(**item.obj)
    return wf


def _aws_search_main_service(wf, query_str):
    """
    """
    if len(query_str) == 1:
        wf.add_item(
            title="Query is too Short!",
            subtitle="please enter at least two character to search for service, eg. 's3'",
            icon=ICON_ERROR,
            valid=True,
        )
        _aws_top20_main_service(wf)
    else:
        for doc in main_service_searcher.search(query_str=query_str, limit=20):
            item = main_svc_doc_to_item(doc)
            wf.add_item(**item.obj)
    return wf


def _aws_top20_sub_service(wf, main_svc_id):
    """
    Given a query string like: "ec2-", return list of items.
    First item is the ec2 console url. Then list of ec2 sub service url ordered
    by weight.
    """
    doc = main_service_searcher.search_one(main_svc_id)
    item = main_svc_doc_to_item(doc)
    wf.add_item(**item.obj)
    for doc in sub_service_searcher.top_20(main_svc_id=main_svc_id):
        item = sub_svc_doc_to_item(doc, main_svc_id)
        wf.add_item(**item.obj)


def _aws_search_sub_service(wf, main_svc_id, query_str):
    if len(query_str) == 1:
        wf.add_item(
            title="Query is too Short!",
            subtitle="please enter at least two character to search for sub service, eg. 'in' (instances), 'sg' (security group)",
            icon=ICON_ERROR,
            valid=True,
        )
        _aws_top20_sub_service(wf, main_svc_id)
    else:
        for doc in sub_service_searcher.search(
                main_svc_id=main_svc_id,
                query_str=query_str,
                limit=20,
        ):
            item = sub_svc_doc_to_item(doc, main_svc_id)
            wf.add_item(**item.obj)
    return wf


def _aws_search_resources(wf, res_searcher_id, query_str):
    if "-" not in res_searcher_id:
        raise ValueError

    main_svc_id, sub_svc_id = res_searcher_id.split("-")
    doc = sub_service_searcher.search_one(main_svc_id=main_svc_id, id=sub_svc_id)
    item = sub_svc_doc_to_item(doc, main_svc_id)
    wf.add_item(**item.obj)

    item_list = filter_resources(res_searcher_id, query_str)
    wf.add_item(title=str(item_list))
    wf._items.extend(item_list)
    return wf


def aws(wf, args=None):
    """
    Update the ~/.aws/credentials and ~/.aws/config file, create / update
    the new mfa profile

    :type wf: workflow.Workflow3
    :param args: manually pass in args to simulate alfred input box.
        FOR TESTING ONLY!
    :type args: list[str]
    """
    if args is None:
        # for alfred input box, ["$key_word", "$query_str"]
        args = wf.args[1:]

    query_str = args[0]
    chunks = [chunk for chunk in query_str.split(" ") if chunk.strip()]
    if len(chunks) == 0:  # query = "" or " "
        _aws_top20_main_service(wf)
    elif len(chunks) == 1 and query_str[-1] != " ":
        if "-" not in chunks[0]:  # query = "ec2"
            _aws_search_main_service(wf, query_str=chunks[0])
        else:
            if chunks[0].endswith("-"):  # query = "ec2-"
                _aws_top20_sub_service(wf, main_svc_id=chunks[0][:-1])
            else:  # query = "ec2-ins"
                _aws_search_sub_service(
                    wf,
                    main_svc_id=chunks[0].split("-", 1)[0],
                    query_str=chunks[0].split("-", 1)[1],
                )
    elif len(chunks) == 1 and query_str[-1] == " ":  # query = "ec2-instances "
        _aws_search_resources(wf, res_searcher_id=chunks[0], query_str=None)
    elif len(chunks) == 2:  # query = "ec2-ins dev"
        _aws_search_resources(wf, res_searcher_id=chunks[0], query_str=chunks[1])
    else:
        raise ValueError("Not a valid input!")

    wf.add_item(title="✅" + str(args))
    return wf
