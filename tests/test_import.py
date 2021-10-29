# -*- coding: utf-8 -*-

import pytest


class TestImport:
    def test(self):
        import aws_tools.handlers as _


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
