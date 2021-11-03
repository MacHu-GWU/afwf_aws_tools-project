#!/bin/bash
#
# Build Alfred Workflow release from source code.
# Basically it creates:
#
# - ${dir_workflow}/main.py
# - ${dir_workflow}/lib
# - ${dir_workflow}/workflow

dir_here="$( cd "$(dirname "$0")" ; pwd -P )"
dir_project_root="$(dirname "${dir_here}")"
dir_venv="${dir_project_root}/venv"
bin_pip="${dir_venv}/bin/pip"

source "${dir_here}/settings.sh"

rm -r "${dir_workflow}/workflow"
rm -r "${dir_workflow}/lib"
rm -r "${dir_workflow}/icons"
rm "${dir_workflow}/main.py"
rm "${dir_workflow}/version"
rm "${dir_workflow}/console-urls.yml"
rm "${dir_project_root}/info.plist"

${bin_pip} install -r "${dir_project_root}/requirements-alfred-workflow.txt" --target="${dir_workflow}"
${bin_pip} install "${dir_project_root}" --target="${dir_workflow}/lib"
cp -R "${dir_project_root}/icons" "${dir_workflow}/icons"
cp "${dir_project_root}/main.py" "${dir_workflow}/main.py"
cp "${dir_project_root}/version" "${dir_workflow}/version"
cp "${dir_project_root}/devtools/console-urls.yml" "${dir_workflow}/console-urls.yml"
cp "${dir_workflow}/info.plist" "${dir_project_root}/info.plist"
