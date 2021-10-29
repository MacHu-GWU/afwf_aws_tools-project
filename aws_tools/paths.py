# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pathlib_mate import Path

# DIR_AWS_TOOLS = Path(__file__).parent
DIR_AWS_TOOLS = Path("/Users/sanhehu/Google Drive/Alfred Setting/Alfred.alfredpreferences/workflows/user.workflow.9137626C-55D8-41FA-BC5C-BD03048E1979/lib/aws_tools")
DIR_PROJECT_ROOT = DIR_AWS_TOOLS.parent

DIR_WORKFLOW_ROOT = DIR_AWS_TOOLS.parent.parent
PATH_CONSOLE_URLS_YAML = Path(DIR_WORKFLOW_ROOT, "console-urls.yml")

DIR_HOME = Path().home()
DIR_AWS_TOOL_USER_DATA = Path(DIR_HOME, ".alfred-aws-tools")
DIR_MAIN_SERVICE_INDEX = Path(DIR_AWS_TOOL_USER_DATA, "main-service-whoosh_index")
DIR_SUB_SERVICE_INDEX = Path(DIR_AWS_TOOL_USER_DATA, "sub-service-whoosh_index")

if not DIR_AWS_TOOL_USER_DATA.exists():
    DIR_AWS_TOOL_USER_DATA.mkdir()
