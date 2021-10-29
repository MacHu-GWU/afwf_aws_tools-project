# -*- coding: utf-8 -*-
#
# This file is generated by cookiecutter-pygitrepo 0.0.5: https://github.com/MacHu-GWU/cookiecutter-pygitrepo/tree/0.0.5

help: ## ** Show this help message
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'


up: ## Set Up the Virtual Environment
	bash ./bin/venv-up.sh


remove: ## Remove Virtual Environment
	bash ./bin/venv-remove.sh


pip-dev-install: ## Install This Package in Editable Mode
	bash ./bin/pip-dev-install.sh


req-test: ## Install Test Dependencies
	bash ./bin/req-test.sh

cov: ## ** Run Code Coverage test
	bash ./bin/test-cov.sh


build-wf: ## Build Alfred Workflow
	bash ./bin/build-wf.sh


refresh-code: ## Refresh Source Code
	bash ./bin/refresh-code.sh


info: ## Show information about python, pip in this environment
	bash ./bin/info.sh
