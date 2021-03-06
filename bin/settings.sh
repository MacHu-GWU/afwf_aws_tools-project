#!/bin/bash
#
# Project specific settings value

if [ -n "${BASH_SOURCE}" ]
then
    dir_bin="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
else
    dir_bin="$( cd "$(dirname "$0")" ; pwd -P )"
fi
dir_project_root="$(dirname "${dir_bin}")"

package_name="aws_tools"

# Update this manually. Right click your workflow in Alfred Workflow view, then click open in finder.
dir_workflow="/Users/sanhehu/Documents/Alfred-Preferences/Alfred.alfredpreferences/workflows/user.workflow.E98A19AC-882C-47FF-AB13-6CB4C86DA93F"

package_version="$(python ${dir_project_root}/${package_name}/_version.py)"
