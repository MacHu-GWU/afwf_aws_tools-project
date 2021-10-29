#!/bin/bash
#
# Install dependency for your python virtualenv

dir_here="$( cd "$(dirname "$0")" ; pwd -P )"
dir_project_root="$(dirname "${dir_here}")"
dir_venv="${dir_project_root}/venv"
bin_pytest="${dir_venv}/bin/pytest"
dir_tests="${dir_project_root}/tests"
dir_coverage_annotate="${dir_project_root}/coverage.annotate"

${bin_pytest} ${dir_tests} -s --cov=aws_tools --cov-report term-missing --cov-report annotate:${dir_coverage_annotate}
