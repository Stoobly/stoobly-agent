# Overridable Environment Variables
#
# STOOBLY_APP_DIR: path to the application source code directory
# STOOBLY_CA_CERTS_DIR: path to folder where ca certs are stored
# STOOBLY_CERTS_DIR: path to a folder to store certs
# STOOBLY_CONTEXT_DIR: path to the folder containing the .stoobly folder
# STOOBLY_WORKFLOW_SERVICE_OPTIONS: extra --service options to pass  'stoobly-agent scaffold workflow' commands

# Overridable Options
#
# workflow_down_extra_options: e.g. $(eval workflow_down_extra_options=<OPTIONS>)
# workflow_log_extra_options: e.g. $(eval workflow_log_extra_options=<OPTIONS>)
# workflow_up_extra_options: e.g. $(eval workflow_up_extra_options=<OPTIONS>)

# Constants
DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
EXEC_WORKFLOW_NAME := exec
PULL_OPTION := $(if $(STOOBLY_IMAGE_USE_LOCAL),,--pull)
USER_ID := $(shell id -u)

CONTEXT_DIR_DEFAULT := $(realpath $(DIR)/../..)

# Configuration
app_dir=$$(realpath "$${STOOBLY_APP_DIR:-$(CONTEXT_DIR_DEFAULT)}")
ca_certs_dir=$$(realpath "$${STOOBLY_CA_CERTS_DIR:-$(app_data_dir)/ca_certs}")
certs_dir=$$(realpath "$${STOOBLY_CERTS_DIR:-$(app_data_dir)/certs}")
context_dir=$$(realpath "$${STOOBLY_CONTEXT_DIR:-$(CONTEXT_DIR_DEFAULT)}")
workflow=record
workflow_service_options=$(shell echo $$STOOBLY_WORKFLOW_SERVICE_OPTIONS)

app_data_dir=$(app_dir)/.stoobly
app_namespace_dir=$(app_data_dir)/docker
app_tmp_dir=$(app_data_dir)/tmp
dockerfile_path=$(app_namespace_dir)/.Dockerfile.context
exec_docker_compose_file_path=$(app_namespace_dir)/stoobly-ui/exec/.docker-compose.exec.yml
exec_namespace=$(shell echo "$(workflow_namespace).$(context_dir)" | (md5 2>/dev/null || md5sum 2>/dev/null || shasum 2>/dev/null) | awk '{print $$1}')
workflow_namespace=$(if $(namespace),$(namespace),$(workflow))
workflow_script=.stoobly/tmp/$(workflow_namespace)/run.sh

# Options
certs_dir_options=--ca-certs-dir-path $(ca_certs_dir) --certs-dir-path $(certs_dir)
stoobly_exec_options=--profile $(EXEC_WORKFLOW_NAME) -p $(exec_namespace)
working_dir_options=--app-dir-path $(app_dir) --context-dir-path $(context_dir)

workflow_down_options=--user-id $(USER_ID) $(workflow_down_extra_options)
workflow_log_options=$(workflow_log_extra_options)
workflow_run_options=--namespace $(workflow_namespace) --script-path $(workflow_script) $(workflow_service_options)
workflow_up_options=$(working_dir_options) $(certs_dir_options) --user-id $(USER_ID) $(workflow_up_extra_options)

# Commands
docker_command=docker
docker_compose_command=$(docker_command) compose
exec_down=$(docker_compose_command) -f "$(exec_docker_compose_file_path)" $(stoobly_exec_options) down
exec_env=APP_DIR="$(app_dir)" CA_CERTS_DIR="$(ca_certs_dir)" USER_ID="$(USER_ID)"
exec_up=$(docker_compose_command) -f "$(exec_docker_compose_file_path)" $(stoobly_exec_options) up --abort-on-container-exit --remove-orphans
source_env=(set -a; [ -f .env ] && source .env; set +a)

# Build base image
stoobly_exec_build=$(docker_command) build $(stoobly_exec_build_args) $(app_namespace_dir)
stoobly_exec_build_args=-f "$(dockerfile_path)" -t stoobly.$(USER_ID) --build-arg USER_ID=$(USER_ID) $(PULL_OPTION) --quiet

# Exec any
stoobly_exec=$(stoobly_exec_build) && $(stoobly_exec_env) $(exec_up)
stoobly_exec_env=$(source_env) && $(exec_env) CONTEXT_DIR="$(context_dir)" 

# Exec workflow run
# Scaffold is stored in the application source code directory, 
# when running a scaffold command from within a container, it needs access to $(app_dir) rather than $(context_dir)
stoobly_exec_run=$(stoobly_exec_build) && $(stoobly_exec_run_env) $(exec_up)
stoobly_exec_run_env=$(source_env) && $(exec_env) CONTEXT_DIR="$(app_dir)"

# Workflow run
workflow_run=$(source_env) && bash "$(app_dir)/$(workflow_script)"

action/install:
	$(eval action=install)
action/uninstall:
	$(eval action=uninstall)
ca-cert/install: stoobly/install
	@if [ -z "$$(ls $(ca_certs_dir) 2> /dev/null)" ]; then \
		read -p "Installing CA certificate is required for $(workflow)ing requests, continue? (y/N) " confirm && \
		if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
			echo "Running stoobly-agent ca-cert install..."; \
			stoobly-agent ca-cert install --ca-certs-dir-path $(ca_certs_dir); \
		else \
			echo "You can install the CA certificate later by running: stoobly-agent ca-cert install"; \
		fi \
	fi
certs:
	@export EXEC_COMMAND=.mkcert && \
	$(stoobly_exec)
exec/down:
	@$(stoobly_exec_env) EXEC_COMMAND=- EXEC_ARGS=- EXEC_OPTIONS=- $(exec_down)
nameservers: tmpdir
	@if [ -f /etc/resolv.conf ]; then \
		nameserver=$$(grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' /etc/resolv.conf) && \
		if [ "$$nameserver" = "127.0.0.53" ]; then \
			echo "Nameserver is 127.0.0.53. Checking resolvectl status..."; \
			nameserver=$$(resolvectl status | sed -n '/DNS Servers:/s/.*DNS Servers:\s*\([^ ]*\).*/\1/p' | head -n 1); \
		fi; \
		echo "$$nameserver" > $(app_tmp_dir)/.nameservers; \
	else \
		echo "/etc/resolv.conf not found." >&2; \
	fi
intercept/disable:
	@export EXEC_COMMAND=.disable && \
	$(stoobly_exec)
intercept/enable:
	@export EXEC_COMMAND=.enable && \
	export EXEC_ARGS=$(scenario_key) && \
	$(stoobly_exec)
mock: workflow/mock ca-cert/install workflow/hostname/install nameservers workflow/up
mock/services: workflow/mock workflow/services
mock/logs: workflow/mock workflow/logs
mock/down: workflow/mock workflow/down workflow/hostname/uninstall exec/down
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
record: workflow/record ca-cert/install workflow/hostname/install nameservers workflow/up
record/down: workflow/record workflow/down workflow/hostname/uninstall exec/down
record/services: workflow/record workflow/services
record/logs: workflow/record workflow/logs
scenario/create:
# Create a scenario
	@export EXEC_COMMAND=.create && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(name)" && \
	$(stoobly_exec)
scenario/delete:
# Delete a scenario
	@export EXEC_COMMAND=.delete && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
scenario/list:
# List scenarios
	@export EXEC_COMMAND=.list && \
	export EXEC_OPTIONS="$(options)" && \
	$(stoobly_exec)
scenario/overwrite:
# Overwrite a scenario
	@export EXEC_COMMAND=.overwrite && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
scenario/reset:
# Resets a scenario to its last snapshot
	@export EXEC_COMMAND=.reset && \:
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
scenario/snapshot:
# Create committable files for a scenario
	@export EXEC_COMMAND=.snapshot && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
stoobly/install: python/validate pipx/install 
	@if ! pipx list 2> /dev/null | grep -q 'stoobly-agent'; then \
		echo "stoobly-agent not found. Installing..."; \
		pipx install stoobly-agent || { echo "Failed to install stoobly-agent"; exit 1; }; \
	fi
test: workflow/test workflow/up
test/services: workflow/test workflow/services
test/logs: workflow/test workflow/logs
test/down: workflow/test workflow/down exec/down
tmpdir:
	@mkdir -p $(app_tmp_dir)
workflow/down:
	@export EXEC_COMMAND=.down && \
	export EXEC_OPTIONS="$(workflow_down_options) $(workflow_run_options) $(options)" && \
	export EXEC_ARGS="$(workflow)" && \
	$(stoobly_exec_run) && \
	$(workflow_run)
workflow/hostname: stoobly/install
	@read -p "Do you want to $(action) hostname(s) in /etc/hosts? (y/N) " confirm && \
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
	@export EXEC_COMMAND=.logs && \
	export EXEC_OPTIONS="$(workflow_log_options) $(workflow_run_options) $(options)" && \
	export EXEC_ARGS="$(workflow)" && \
	$(stoobly_exec_run) && \
	$(workflow_run)
workflow/mock:
	$(eval workflow=mock)
workflow/record:
	$(eval workflow=record)
workflow/services:
	@export EXEC_COMMAND=.services && \
	export EXEC_OPTIONS="$(workflow_service_options) $(options)" && \
	export EXEC_ARGS="$(workflow)" && \
	$(stoobly_exec_run)
workflow/test:
	$(eval workflow=test) $(eval workflow_up_extra_options=$(workflow_up_extra_options) --no-publish)
workflow/up:
	@export EXEC_COMMAND=.up && \
	export EXEC_OPTIONS="$(workflow_up_options) $(workflow_run_options) $(options)" && \
	export EXEC_ARGS="$(workflow)" && \
	$(stoobly_exec_run) && \
	$(workflow_run)
