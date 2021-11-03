# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from workflow import Workflow3
from loggerFactory import FileRotatingLogger
from pathlib_mate import Path
from .paths import PATH_LOG


def add_logger(wf):
    """
    :type wf: Workflow3
    """
    if not hasattr(wf, "log"):
        logger = FileRotatingLogger(
            name="aws_tools",
            path=PATH_LOG.abspath,
            max_bytes=1000000,  # 1MB
            backup_count=5,
        )
        wf.log = logger


def clear_log():
    to_remove_list = list()
    to_remove_list.append(PATH_LOG)
    for i in range(1, 10):
        p = Path(PATH_LOG.abspath + ".{}".format(str(i)))
        to_remove_list.append(p)

    for p in to_remove_list:
        if p.exists():
            p.remove()
