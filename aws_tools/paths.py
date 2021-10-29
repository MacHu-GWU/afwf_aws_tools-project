# -*- coding: utf-8 -*-

"""
Centralized path management. This module will not import other aws_tools module.
"""

from __future__ import unicode_literals
from pathlib_mate import Path

# the python package directory in alfred workflow,
# should ends
# DIR_AWS_TOOLS_AF = Path(__file__).parent # type: Path
DIR_AWS_TOOLS_AF = Path(
    "/Users/sanhehu/Documents/Alfred-Preferences/Alfred.alfredpreferences/workflows/user.workflow.E98A19AC-882C-47FF-AB13-6CB4C86DA93F/lib/aws_tools")  # type: Path
DIR_WORKFLOW_ROOT = DIR_AWS_TOOLS_AF.parent.parent  # type: Path
PATH_CONSOLE_URLS_YAML = Path(DIR_WORKFLOW_ROOT, "console-urls.yml")  # type: Path

# --- source code in github project directory ---
# the python package directory in github directory
DIR_AWS_TOOLS_GH = Path(__file__).parent  # type: Path
DIR_PROJECT_ROOT = DIR_AWS_TOOLS_GH.parent  # type: Path

# --- tests ---
DIR_TESTS = Path(DIR_PROJECT_ROOT, "tests")  # type: Path
P_TEST_BACKUP_CONFIG_FILE = Path(DIR_TESTS, "config-backup")  # type: Path
P_TEST_BACKUP_CREDENTIALS_FILE = Path(DIR_TESTS, "credentials-backup")  # type: Path
P_TEST_CONFIG_FILE = Path(DIR_TESTS, "config")  # type: Path
P_TEST_CREDENTIALS_FILE = Path(DIR_TESTS, "credentials")  # type: Path

# --- user data in ${HOME} directory ---
DIR_HOME = Path().home()  # type: Path
PATH_DEFAULT_AWS_CONFIG_FILE = Path(DIR_HOME, ".aws", "config")  # type: Path
PATH_DEFAULT_AWS_CREDENTIAL_FILE = Path(DIR_HOME, ".aws", "credentials")  # type: Path

DIR_AWS_TOOL_USER_DATA = Path(DIR_HOME, ".alfred-aws-tools")  # type: Path
DIR_MAIN_SERVICE_INDEX = Path(DIR_AWS_TOOL_USER_DATA, "main-service-whoosh_index")  # type: Path
DIR_SUB_SERVICE_INDEX = Path(DIR_AWS_TOOL_USER_DATA, "sub-service-whoosh_index")  # type: Path

if not DIR_AWS_TOOL_USER_DATA.exists():
    DIR_AWS_TOOL_USER_DATA.mkdir()
