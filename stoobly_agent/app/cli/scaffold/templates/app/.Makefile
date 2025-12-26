# Overridable Environment Variables
#
# STOOBLY_APP_DIR: path to the application source code directory, defaults to $(pwd)
# STOOBLY_CA_CERTS_DIR: path to folder where ca certs are stored, defaults to $(pwd)/.stoobly/ca_certs
# STOOBLY_CA_CERTS_INSTALL_CONFIRM: confirm answer to CA certificate installation prompt
# STOOBLY_CERTS_DIR: path to a folder to store certs, defaults to $(pwd)/.stoobly/certs
# STOOBLY_CONTEXT_DIR: path to the folder containing the .stoobly folder, defaults to $(pwd)
# STOOBLY_DOTENV_FILE: path to dotenv file, defaults to $(pwd)/.env
# STOOBLY_HOSTNAME_INSTALL_CONFIRM: confirm answer to hostname installation prompt
# STOOBLY_WORKFLOW_SERVICE_OPTIONS: extra --service options to pass 'stoobly-agent scaffold workflow' commands

# Overridable Options
#
# workflow_down_extra_options e.g. $(eval workflow_down_extra_options=<OPTIONS>)
# workflow_log_extra_options e.g. $(eval workflow_log_extra_options=<OPTIONS>)
# workflow_up_extra_options e.g. $(eval workflow_up_extra_options=<OPTIONS>)
# 
# For full list, see targets with EXEC_OPTIONS

# Constants
DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
DOCKER_BIN := docker
PULL_OPTION := $(if $(STOOBLY_IMAGE_USE_LOCAL),,--pull)
USER_ID := $(shell id -u)

CONTEXT_DIR_DEFAULT := $(realpath $(DIR)/../..)

# Configuration
app_dir=$$(realpath "$${STOOBLY_APP_DIR:-$(CONTEXT_DIR_DEFAULT)}")
ca_certs_dir=$$(realpath "$${STOOBLY_CA_CERTS_DIR:-$(app_data_dir)/ca_certs}")
certs_dir=$$(realpath "$${STOOBLY_CERTS_DIR:-$(app_data_dir)/certs}")
context_dir=$$(realpath "$${STOOBLY_CONTEXT_DIR:-$(CONTEXT_DIR_DEFAULT)}")
dotenv_file=$$(realpath "$${STOOBLY_DOTENV_FILE:-.env}" 2> /dev/null || echo '')
workflow=record
workflow_service_options=$(shell echo $$STOOBLY_WORKFLOW_SERVICE_OPTIONS)

app_data_dir=$(app_dir)/.stoobly
app_namespace_dir=$(app_data_dir)/services
app_tmp_dir=$(app_data_dir)/tmp
dockerfile_path=$(app_namespace_dir)/.Dockerfile.context
exec_docker_compose_file_path=$(app_namespace_dir)/stoobly-ui/exec/.docker-compose.yml
workflow_namespace=$(if $(namespace),$(namespace),$(workflow))
workflow_namespace_dir=$(app_tmp_dir)/$(workflow_namespace)
workflow_script=.stoobly/tmp/$(workflow_namespace)/run.sh

# Options
certs_dir_options=--ca-certs-dir-path $(ca_certs_dir) --certs-dir-path $(certs_dir)
working_dir_options=--app-dir-path $(app_dir) --context-dir-path $(context_dir)

workflow_down_options=$(working_dir_options) --user-id $(USER_ID) $(workflow_down_extra_options)
workflow_log_options=$(workflow_log_extra_options)
workflow_run_options=--namespace $(workflow_namespace) --script-path $(workflow_script) $(workflow_service_options)
workflow_up_options=$(working_dir_options) $(certs_dir_options) --user-id $(USER_ID) $(workflow_up_extra_options)
 
# Commands
exec_env=APP_DIR="$(app_dir)" CA_CERTS_DIR="$(ca_certs_dir)" USER_ID="$(USER_ID)"
exec_up=$(DOCKER_BIN) compose -f "$(exec_docker_compose_file_path)" run --rm stoobly_ui.command

# Build base image
stoobly_exec_build=$(DOCKER_BIN) build $(stoobly_exec_build_args) $(app_namespace_dir) > /dev/null
stoobly_exec_build_args=-f "$(dockerfile_path)" -t stoobly.$(USER_ID) --build-arg USER_ID=$(USER_ID) $(PULL_OPTION) --quiet

# Exec any
stoobly_exec=$(stoobly_exec_build) && $(stoobly_exec_env) $(exec_up)
stoobly_exec_env=$(exec_env) CONTEXT_DIR="$(context_dir)" 

# Exec workflow run
# Scaffold is stored in the application source code directory. 
# When running a scaffold command from within a container, it needs access to $(app_dir) rather than $(context_dir)
stoobly_exec_run=$(stoobly_exec_build) && $(stoobly_exec_run_env) $(exec_up)
stoobly_exec_run_env=$(exec_env) CONTEXT_DIR="$(app_dir)"

action/install:
	$(eval action=install)
action/uninstall:
	$(eval action=uninstall)
ca-cert/install: stoobly/install
	@if [ -z "$$(ls $(ca_certs_dir) 2> /dev/null)" ]; then \
		if [ -n "$$STOOBLY_CA_CERTS_INSTALL_CONFIRM" ]; then \
			confirm="$$STOOBLY_CA_CERTS_INSTALL_CONFIRM"; \
		else \
			read -p "Installing CA certificate is required for $(workflow)ing requests, continue? (y/N) " confirm; \
		fi && \
		if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
			echo "Running stoobly-agent ca-cert install..."; \
			stoobly-agent ca-cert install --ca-certs-dir-path $(ca_certs_dir); \
		else \
			echo "You can install the CA certificate later by running: stoobly-agent ca-cert install"; \
		fi \
	fi
certs:
	@export EXEC_COMMAND=scaffold/.mkcert EXEC_OPTIONS="" EXEC_ARGS="" && \
	$(stoobly_exec)
dotenv: workflow/namespace
	@if [ -f "$(dotenv_file)" ]; then cp "$(dotenv_file)" $(workflow_namespace_dir)/.env; fi
nameservers: workflow/namespace
	@if [ -f /etc/resolv.conf ]; then \
		nameserver=$$(grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' /etc/resolv.conf) && \
		if [ "$$nameserver" = "127.0.0.53" ]; then \
			echo "Nameserver is 127.0.0.53. Checking resolvectl status..."; \
			nameserver=$$(resolvectl status | sed -n '/DNS Servers:/s/.*DNS Servers:\s*\([^ ]*\).*/\1/p' | head -n 1); \
		fi; \
		echo "$$nameserver" > $(workflow_namespace_dir)/.nameservers; \
	else \
		echo "/etc/resolv.conf not found." >&2; \
	fi
intercept/disable:
	@export EXEC_COMMAND=intercept/.disable EXEC_OPTIONS="" EXEC_ARGS="" && \
	$(stoobly_exec)
intercept/enable:
	@export EXEC_COMMAND=intercept/.enable EXEC_OPTIONS="" EXEC_ARGS=$(scenario_key) && \
	$(stoobly_exec)
mock: workflow/mock workflow/up nameservers workflow/hostname/install workflow/up/run
mock/down: workflow/mock workflow/down workflow/down/run workflow/hostname/uninstall
mock/logs: workflow/mock workflow/logs workflow/logs/run
mock/report: workflow/mock workflow/report
mock/services: workflow/mock workflow/services
pipx/install:
	@if ! command -v pipx >/dev/null 2>&1; then \
		echo "pipx is not installed. Installing pipx..."; \
		python3 -m pip install --user pipx && python3 -m pipx ensurepath; \
	fi
python/validate:
	@if ! python3 --version | grep -Eq 'Python 3\.(10|11|12)'; then \
		echo "Error: Python 3.10, 3.11, or 3.12 is required."; \
		exit 1; \
	fi
record: workflow/record ca-cert/install workflow/up nameservers workflow/hostname/install workflow/up/run
record/down: workflow/record workflow/down workflow/down/run workflow/hostname/uninstall
record/logs: workflow/record workflow/logs workflow/logs/run
record/report: workflow/record workflow/report
record/services: workflow/record workflow/services
scenario/create:
# Create a scenario
	@export EXEC_COMMAND=scenario/.create EXEC_OPTIONS="$(options)" EXEC_ARGS="$(name)" && \
	$(stoobly_exec)
scenario/delete:
# Delete a scenario
	@export EXEC_COMMAND=scenario/.delete EXEC_OPTIONS="$(options)" EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
scenario/list:
# List scenarios
	@export EXEC_COMMAND=scenario/.list EXEC_OPTIONS="$(options)" EXEC_ARGS="" && \
	$(stoobly_exec)
scenario/overwrite:
# Overwrite a scenario
	@export EXEC_COMMAND=scenario/.overwrite EXEC_OPTIONS="$(options)" EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
scenario/reset:
# Resets a scenario to its last snapshot
	@export EXEC_COMMAND=scenario/.reset EXEC_OPTIONS="$(options)" EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
scenario/snapshot:
# Create committable files for a scenario
	@export EXEC_COMMAND=scenario/.snapshot EXEC_OPTIONS="$(options)" EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
stoobly/install: python/validate pipx/install 
	@if ! pipx list 2> /dev/null | grep -q 'stoobly-agent'; then \
		echo "stoobly-agent not found. Installing..."; \
		pipx install stoobly-agent || { echo "Failed to install stoobly-agent"; exit 1; }; \
	fi
test: workflow/test workflow/up workflow/up/run
test/down: workflow/test workflow/down workflow/down/run
test/logs: workflow/test workflow/logs workflow/logs/run
test/report: workflow/test workflow/report
test/services: workflow/test workflow/services
tmpdir:
	@mkdir -p $(app_tmp_dir)
workflow/down: dotenv
	@export EXEC_COMMAND=scaffold/.down EXEC_OPTIONS="$(workflow_down_options) $(workflow_run_options) $(options)" EXEC_ARGS="$(workflow)" && \
	$(stoobly_exec_run)
workflow/down/run:
	@bash "$(app_dir)/$(workflow_script)"
workflow/hostname: stoobly/install
	@if [ -n "$$STOOBLY_HOSTNAME_INSTALL_CONFIRM" ]; then \
		confirm="$$STOOBLY_HOSTNAME_INSTALL_CONFIRM"; \
	else \
		read -p "Do you want to $(action) hostname(s) in /etc/hosts? (y/N) " confirm; \
	fi && \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		CURRENT_VERSION=$$(stoobly-agent --version); \
		REQUIRED_VERSION="1.4.0"; \
		if [ "$$(printf '%s\n' "$$REQUIRED_VERSION" "$$CURRENT_VERSION" | sort -V | head -n 1)" != "$$REQUIRED_VERSION" ]; then \
			echo "stoobly-agent version $$REQUIRED_VERSION required. Please run: pipx upgrade stoobly-agent"; \
			exit 1; \
		fi; \
		echo "Running stoobly-agent scaffold hostname $(action) $(workflow_service_options)"; \
		stoobly-agent scaffold hostname $(action) --app-dir-path $(app_dir) --workflow $(workflow) $(workflow_service_options); \
	fi
workflow/hostname/install: action/install workflow/hostname
workflow/hostname/uninstall: action/uninstall workflow/hostname  
workflow/logs:
	@export EXEC_COMMAND=scaffold/.logs EXEC_OPTIONS="$(workflow_log_options) $(workflow_run_options) $(options)" EXEC_ARGS="$(workflow)" && \
	$(stoobly_exec_run)
workflow/logs/run:
	@bash "$(app_dir)/$(workflow_script)"
workflow/mock:
	$(eval workflow=mock)
workflow/namespace: tmpdir
	@mkdir -p $(workflow_namespace_dir)
workflow/record:
	$(eval workflow=record)
workflow/report:
	@export EXEC_COMMAND=request/log/.list EXEC_OPTIONS="$(options)" EXEC_ARGS="" && \
	$(stoobly_exec)
workflow/services:
	@export EXEC_COMMAND=scaffold/.services EXEC_OPTIONS="$(workflow_service_options) $(options)" EXEC_ARGS="$(workflow)" && \
	$(stoobly_exec_run)
workflow/test:
	$(eval workflow=test) $(eval workflow_up_extra_options=$(workflow_up_extra_options) --no-publish)
workflow/up: dotenv
	@export EXEC_COMMAND=scaffold/.up EXEC_OPTIONS="$(workflow_up_options) $(workflow_run_options) $(options)" EXEC_ARGS="$(workflow)" && \
	$(stoobly_exec_run)
workflow/up/run:
	@bash "$(app_dir)/$(workflow_script)"
