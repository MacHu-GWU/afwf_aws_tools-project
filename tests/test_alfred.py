# -*- coding: utf-8 -*-

import pytest
from workflow.workflow3 import Workflow3, Item3
from aws_tools.alfred import ItemArgs, VarKeyEnum, VarValueEnum


class TestItemArgs(object):
    def test(self):
        wf = Workflow3()

        item_args = ItemArgs("")
        item = item_args.add_to_wf(wf)
        assert isinstance(item, Item3)

        item_args.open_browser("google.com")
        item = item_args.add_to_wf(wf)
        assert item.variables[VarKeyEnum.open_browser] == VarValueEnum.y
        assert item.variables[VarKeyEnum.open_browser_url] == "google.com"

        item_args.open_file("/tmp")
        item_args.run_script("echo Hello")
        item_args.copy_text("hello world")
        item_args.notify("the title", "the subtitle")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
