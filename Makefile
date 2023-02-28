default: help
SHELL := /bin/bash

-include .env
-include Makefile.configure
-include Makefile.specific
-include .github/workflows/Makefile.cicd

BRANCH ?= master
DOMAIN ?= github.com
CODECOV_TOKEN ?=
PART ?= #PATCH #MINOR MAJOR
EXTRAS ?= dev
GH_PACKAGE=$(shell tr '[:upper:]' '[:lower:]' <<< "ghcr.io/$(_USER)/$(_PROJECT):")
SERVICE_NAME=$(shell tr '[:upper:]' '[:lower:]' <<< "$(_PROJECT)-dev")
BOILERPLATE_REPO_PATH = git@github.com:Filip-231/Boilerplate.git
BOILERPLATE_REPO_SSH = git@$(DOMAIN):$(BOILERPLATE_REPO_PATH)
PYTHON ?= python3.9
_VENV=.venv
_VENV_ACTIVATE = $(_VENV)/bin/activate
_CURRENT_DIR_NAME=$(shell cd -P -- '$(shell dirname -- "$0")' && pwd -P)

_BOLD := $(shell tput -T ansi bold)
_COLS := $(shell tput -T ansi cols)
_DEFAULT := $(shell tput -T ansi sgr0)
_ITALICS := $(shell tput -T ansi sitm)
_BLUE := $(shell tput -T ansi setaf 4)
_CYAN := $(shell tput -T ansi setaf 6)
_GREEN := $(shell tput -T ansi setaf 2)
_MAGENTA := $(shell tput -T ansi setaf 5)
_RED := $(shell tput -T ansi setaf 1)
_YELLOW := $(shell tput -T ansi setaf 3)


.PHONY: bump
bump: venv ## (PART= ) bump the release version - deduced automatically from commit messages unless PART is provided
	. $(_VENV_ACTIVATE) && \
		cz bump --files-only --yes $(if $(PART),--increment=$(PART))


.PHONY: all
all: ## commit and push all changes
	git add .
	git commit -m "feat: auto-commit" --no-verify
	git push
	git status


.PHONY: commit
commit: venv ## make interactive conventional commit
	. $(_VENV_ACTIVATE) && \
		cz commit


.PHONY: help
help: ## display this help message
	$(info Please use $(_BOLD)make $(_DEFAULT)$(_ITALICS)$(_CYAN)target$(_DEFAULT) where \
	$(_ITALICS)$(_CYAN)target$(_DEFAULT) is one of:)
	@grep --no-filename "^[a-zA-Z]" $(MAKEFILE_LIST) | \
		sort | \
		awk -F ":.*?## " 'NF==2 {printf "$(_CYAN)%-20s$(_DEFAULT)%s\n", $$1, $$2}'


.PHONY: changelog
changelog: venv ## (UNRELEASED= current version) update the changelog incrementally.
	@. $(_VENV_ACTIVATE) && \
		cz changelog --incremental --unreleased-version=$(UNRELEASED)
		#make changelog UNRELEASED=$(make get-version)


.PHONY: get-version
get-version: ## output the current version
	@. $(_VENV_ACTIVATE) && \
		cz version --project


.PHONY: check-commit
check-commit: venv ## check the commit message is valid
	. $(_VENV_ACTIVATE) && \
		cz check --commit-msg-file=./.git/COMMIT_EDITMSG


.PHONY: test
test:: venv ## (ALLURE=True BROWSE=True) run tests
	echo "Executing pytest"
	@. "$(_VENV_ACTIVATE)" && python -m pytest -p no:allure_pytest_bdd  --cov --cov-report=term-missing \
			--cov-report=xml:public/coverage.xml \
			$(if $(ALLURE),--alluredir=public/allure-results,-p no:allure_pytest) \
			$(if $(CODECOV_TOKEN),--codecov --codecov-token="$(CODECOV_TOKEN)",-p no:codecov) \
			$(if $(DEBUG),--pdb )tests/ $(if $(ALLURE),&& \
				allure generate --clean --report-dir public/allure-report public/allure-results)
	$(if $(ALLURE), \
		$(if $(BROWSE), \
		echo "Opening Allure report" && \
			allure open public/allure-report \
		) \
	)


.PHONY: format
format:: venv ## format code
	. "$(_VENV_ACTIVATE)" && \
		isort . && black .


.PHONY: lint
lint:: venv ## run static code checkers
	. "$(_VENV_ACTIVATE)" && \
		prospector


.PHONY: docs
docs:: venv ## render documentation
	. "$(_VENV_ACTIVATE)" && \
		sphinx-build -a -b html -E docs/source public


.PHONY: clean
clean:: ## clean up temp and trash files
	find . -type f -name "*.py[cdo]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage .mypy_cache .pytest_cache *.egg-info build dist public
	sudo docker-compose down --remove-orphans
	yes | sudo docker system prune --volumes


.PHONY: install
install:: pre-install ## install the requirements
	$(info Installing requirements.)
	. "$(_VENV_ACTIVATE)" && \
		pip install -r requirements.txt


.PHONY: pre-install
pre-install: venv ## install pre-requirements
	. $(_VENV_ACTIVATE) && \
		pip install $(if $(UPGRADE),--upgrade )commitizen cruft pre-commit pip-tools && \
			if [ -n "$(SKIP_PRE_COMMIT)" ]; then \
			echo "SKIP_PRE_COMMIT detected; ignoring pre-commit setup..."; \
			else \
				if [ -n "$(UPGRADE)" ]; then \
				pre-commit autoupdate --config=.pre-commit-config.yml; \
				fi; \
				pre-commit install --allow-missing-config --config=.pre-commit-config.yml --hook-type=pre-commit \
					--hook-type=commit-msg; \
			fi


.PHONY: venv
venv: $(_VENV_ACTIVATE) ## install virtual environment


$(_VENV_ACTIVATE):
	python3 -m venv --clear "$(_VENV)" && \
		. $@ && \
		pip install --upgrade pip
	touch $@
