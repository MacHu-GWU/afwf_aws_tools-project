# -*- coding: utf-8 -*-

from pathlib_mate import Path
from whoosh.fields import SchemaClass
from whoosh.index import Index, open_dir, create_in


class FtsSearcher(object):
    """
    A whoosh full text search utility class.

    :type schema: SchemaClass
    :type index_dir: Path
    """

    def __init__(self,
                 schema,
                 index_dir):
        self.schema = schema
        self.index_dir = Path(index_dir)  # ensure it is Path object

    def get_index(self):
        """
        :rtype: Index
        """
        if self.index_dir.exists():
            idx = open_dir(self.index_dir.abspath)
        else:
            self.index_dir.mkdir()
            idx = create_in(dirname=self.index_dir.abspath, schema=self.schema)
        return idx

    def build_index(self):
        """
        Abstract method that build the whoosh index
        """
        raise NotImplementedError
