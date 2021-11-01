# -*- coding: utf-8 -*-

"""
Centralized path management. This module will not import other aws_tools module.
"""

from __future__ import unicode_literals
from pathlib_mate import Path


class Env:
    local_dev = "local_dev"
    alfred = "alfred"


DIR_WORKFLOW_ROOT = Path(
    "/Users/sanhehu/Documents/Alfred-Preferences/Alfred.alfredpreferences/workflows/user.workflow.E98A19AC-882C-47FF-AB13-6CB4C86DA93F")

DIR_AWS_TOOLS = Path(__file__).parent

if DIR_AWS_TOOLS.parent.basename == "afwf_aws_tools-project":  # local dev env
    env = Env.local_dev
elif DIR_AWS_TOOLS.parent.basename == "lib":  # alfred 4 workflow env
    DIR_WORKFLOW_ROOT = DIR_AWS_TOOLS.parent.parent
    env = Env.alfred
else:
    raise EnvironmentError

if env == Env.local_dev:
    DIR_PROJECT_ROOT = DIR_AWS_TOOLS.parent  # type: Path
    PATH_CONSOLE_URLS_YAML = Path(DIR_WORKFLOW_ROOT, "console-urls.yml")  # type: Path
    PATH_CONSOLE_URLS_TEMP_YAML = Path(DIR_WORKFLOW_ROOT, "console-urls-tmp.yml")  # type: Path
    DIR_ICONS = Path(DIR_PROJECT_ROOT, "icons")  # type: Path

    # --- tests ---
    DIR_TESTS = Path(DIR_PROJECT_ROOT, "tests")  # type: Path
    PATH_TEST_BACKUP_CONFIG_FILE = Path(DIR_TESTS, "config-backup")  # type: Path
    PATH_TEST_BACKUP_CREDENTIALS_FILE = Path(DIR_TESTS, "credentials-backup")  # type: Path
    PATH_TEST_CONFIG_FILE = Path(DIR_TESTS, "config")  # type: Path
    PATH_TEST_CREDENTIALS_FILE = Path(DIR_TESTS, "credentials")  # type: Path

elif env == Env.alfred:
    PATH_CONSOLE_URLS_YAML = Path(DIR_WORKFLOW_ROOT, "console-urls.yml")  # type: Path
    DIR_ICONS = Path(DIR_WORKFLOW_ROOT, "icons")  # type: Path
    PATH_ERROR_TRACEBACK = Path(DIR_WORKFLOW_ROOT, "error.txt") # type: Path

# --- user data in ${HOME} directory ---
DIR_HOME = Path().home()  # type: Path
PATH_DEFAULT_AWS_CONFIG_FILE = Path(DIR_HOME, ".aws", "config")  # type: Path
PATH_DEFAULT_AWS_CREDENTIALS_FILE = Path(DIR_HOME, ".aws", "credentials")  # type: Path

DIR_AWS_TOOL_USER_DATA = Path(DIR_HOME, ".alfred-aws-tools")  # type: Path
DIR_MAIN_SERVICE_INDEX = Path(DIR_AWS_TOOL_USER_DATA, "main-service-whoosh_index")  # type: Path
DIR_SUB_SERVICE_INDEX = Path(DIR_AWS_TOOL_USER_DATA, "sub-service-whoosh_index")  # type: Path

if not DIR_AWS_TOOL_USER_DATA.exists():
    DIR_AWS_TOOL_USER_DATA.mkdir()
