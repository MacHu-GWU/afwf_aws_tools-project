#!/bin/bash
# -*- coding: utf-8 -*-
#
# activate your virtualenv quickly if not using pyenv-virtualenv
#
# usage:
#
# - activate: ``$ source ./bin/py/activate.sh``
# - deactivate: ``$ deactivate``

if [ -n "${BASH_SOURCE}" ]
then
    dir_bin="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
else
    dir_bin="$( cd "$(dirname "$0")" ; pwd -P )"
fi
dir_project_root="$(dirname "${dir_bin}")"
source "${dir_project_root}/venv/bin/activate"
