# -*- coding: utf-8 -*-

import pytest
from pathlib_mate import Path
from aws_tools import paths

def test():
    pass



if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
