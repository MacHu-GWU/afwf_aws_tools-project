# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pprint import pprint
from aws_tools.handlers.aws_fts import main_service_searcher, sub_service_searcher

# main_service_searcher.build_index(force_rebuild=True)
# sub_service_searcher.build_index(force_rebuild=True)

# pprint(main_service_searcher.top_20())
# pprint(main_service_searcher.search("ec"))
# pprint(main_service_searcher.search_one("ec2"))

# pprint(sub_service_searcher.top_20("ec2"))
# pprint(sub_service_searcher.search_one("ec2", "securitygroups"))
pprint(sub_service_searcher.search("ec2", "sg"))



# from whoosh import qparser, query
# idx = main_service_searcher.get_index()
# with idx.searcher() as searcher:
#     q = query.And([query.Term("globally", True), query.Term("weight", 9)])
#     for hit in searcher.search(q, limit=5, sortedby="weight", reverse=True):
#         print(hit.fields())

# parser = qparser.QueryParser(
#     "id",
#     schema=main_service_searcher.schema,
# )
# # parser.remove_plugin_class(qparser.WildcardPlugin)
# # parser.add_plugin(qparser.PrefixPlugin())
# # query = parser.parse("ec*")
#
# q = query.Prefix("id", "ec")
#
# with idx.searcher() as searcher:
#     result = [
#         hit.fields()
#         for hit in searcher.search(q, limit=20)
#     ]
#     pprint(result)