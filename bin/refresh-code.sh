#!/bin/bash

dir_bin="$( cd "$(dirname "$0")" ; pwd -P )"
dir_project_root="$(dirname "${dir_bin}")"
dir_venv="${dir_project_root}/venv"
bin_pip="${dir_venv}/bin/pip"

source ${dir_bin}/settings.sh

rm -r ${dir_workflow}/lib/${package_name}
rm -r ${dir_workflow}/lib/${package_name}-${package_version}.dist-info
rm ${dir_workflow}/main.py

#cp -r ${dir_project_root}/${package_name} ${dir_workflow}/lib/${package_name}
${bin_pip} install ${dir_project_root} --no-dependencies --target=${dir_workflow}/lib
cp ${dir_project_root}/main.py ${dir_workflow}/main.py
