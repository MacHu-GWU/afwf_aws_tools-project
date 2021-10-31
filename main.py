# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import sys
import json
from workflow import Workflow3

here = os.path.dirname(os.path.abspath(__file__))
wf_input_file = os.path.join(here, "wf-input.json")
wf_output_file = os.path.join(here, "wf-output.json")


def json_dump(file, data):
    with open(file, "wb") as f:
        f.write(json.dumps(data, indent=4).encode("utf-8"))


def main(wf):
    """
    .. note::

        注意, 所有的第三方库的导入都要放在 main 函数内, 因为直到创建 Workflow 实例时,
        lib 目录才会被添加到系统路径中去. 在这之前所有的第三方库都无法被找到.

    :type wf: Workflow3
    """
    from aws_tools.handlers import handler

    # 将 Python 收到的 args 以及返回的 items 保存为 json 文件, 用于调试
    # if "user.workflow" not in here: # don't dump if in alfred preference folder
    json_dump(wf_input_file, wf.args)
    # json_dump(wf_input_file, sys.argv)
    json_dump(wf_output_file, wf.obj)
    # json_dump(wf_output_file, wf.args)

    # from aws_tools.alfred import ActionEnum
    # item = wf.add_item(title="test", subtitle="my_sub", arg="touch \"/Users/sanhehu/airflow/my folder/good.txt\"", valid=True)
    # item.setvar("action", "run-script")
    # # item.setvar("open_file_path", "/Users/sanhehu/airflow")
    # item.setvar("cmd", "touch /Users/sanhehu/airflow/good.txt")

    # item.setvar("action", ActionEnum.copy)
    # item.add_modifier(
    #     key="cmd", subtitle="v1", arg="v2", valid=None,
    # )

    wf = handler(wf)
    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(libraries=["lib", ])
    sys.exit(wf.run(main))
