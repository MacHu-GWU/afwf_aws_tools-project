# -*- coding: utf-8 -*-

from workflow.workflow3 import Workflow3
from aws_tools.handlers.aws import aws_handlers
from sfm.timer import TimeTimer

with TimeTimer():
    wf = Workflow3()
    aws_handlers.mh_aws(wf, query_str="vpc-vp")
