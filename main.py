# -*- coding: utf-8 -*-

"""
**How to debug**:

Note: you have to copy the ``info.plist`` file to the repo root directory
to simulate a Alfred Workflow runtime.

1. Figure out the arguments: suppose your input in Alfred UI is
    "aws ec2-instances my server", the trigger keyword is ``aws``,
    in Alfred Workflow preference, you should see the script filter ``aws``.
    The script should be ``/usr/bin/python main.py 'mh_aws {query}'``
2. Scroll to the end of this file, comment out the line ``sys.exit(wf.run(main))``.
    uncomment the line ``wf.run(main)``
3. Scroll to the ``def main(wf, args=None):``, manually define
    ``args=["mh_aws ec2-instances my server",]``. This is the corresponding
    python code.
"""

from __future__ import unicode_literals
import os
import sys
import json
import traceback
from workflow import Workflow3, ICON_ERROR

DIR_HERE = os.path.dirname(os.path.abspath(__file__))
DIR_HOME = os.path.expanduser("~")
DIR_USER_DATA = os.path.join(DIR_HOME, ".alfred-aws-tools")

PATH_LOG = os.path.join(DIR_USER_DATA, "log.txt")
PATH_ERROR = os.path.join(DIR_USER_DATA, "error.txt")

PATH_WF_INPUT = os.path.join(DIR_HERE, "wf-input.json")
PATH_WF_OUTPUT = os.path.join(DIR_HERE, "wf-output.json")


def json_dump(file, data):
    with open(file, "wb") as f:
        f.write(json.dumps(data, indent=4).encode("utf-8"))


def write_text(file, text):
    with open(file, "wb") as f:
        f.write(text.encode("utf-8"))


def main(wf, args=None):  # set args here for manual debug
    """
    .. note::

        注意, 所有的第三方库的导入都要放在 main 函数内, 因为直到创建 Workflow 实例时,
        lib 目录才会被添加到系统路径中去. 在这之前所有的第三方库都无法被找到.

    :type wf: Workflow3
    :type args: list[str]
    """
    from loggerFactory import FileRotatingLogger

    logger = FileRotatingLogger(
        name="aws_tools",
        path=os.path.join(DIR_USER_DATA, "log.txt"),
        max_bytes=1000000,  # 1MB
        backup_count=5,
    )
    wf.log = logger

    try:
        from aws_tools.handlers import handler
        wf = handler(wf, args=args)
    except:
        traceback_msg = traceback.format_exc()
        write_text(PATH_ERROR, traceback_msg)

        item = wf.add_item(
            title="ERROR! hit 'Enter' to open error traceback log",
            subtitle=PATH_ERROR,
            icon=ICON_ERROR,
            valid=True
        )
        item.setvar("open_file", "y")
        item.setvar("open_file_path", PATH_ERROR)

    wf.send_feedback()
    return wf


if __name__ == "__main__":
    wf = Workflow3(libraries=["lib", ])

    # Production Mode
    sys.exit(wf.run(main))  # comment this out for debug

    # Debug Mode
    # wf.run(main)  # uncomment this for debug
