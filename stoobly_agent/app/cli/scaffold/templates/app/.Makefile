# Overridable Environment Variables
#
# STOOBLY_APP_DIR: path to the application source code directory
# STOOBLY_CA_CERTS_DIR: path to folder where ca certs are stored
# STOOBLY_CERTS_DIR: path to a folder to store certs
# STOOBLY_CONTEXT_DIR: path to the folder containing the .stoobly folder
# STOOBLY_WORKFLOW_SERVICE_OPTIONS: extra --service options to pass  'stoobly-agent scaffold workflow' commands

# Constants
DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
EXEC_WORKFLOW_NAME := exec
PULL_OPTION := $(if $(STOOBLY_IMAGE_USE_LOCAL),,--pull)
USER_ID := $(shell id -u)

CONTEXT_DIR_DEFAULT := $(realpath $(DIR)/../..)

# Configuration
app_dir=$$(realpath "$${STOOBLY_APP_DIR:-$(CONTEXT_DIR_DEFAULT)}")
ca_certs_dir=$$(realpath "$${STOOBLY_CA_CERTS_DIR:-$$(realpath ~)/.mitmproxy}")
certs_dir=$$(realpath "$${STOOBLY_CERTS_DIR:-$(app_data_dir)/certs}")
context_dir=$$(realpath "$${STOOBLY_CONTEXT_DIR:-$(CONTEXT_DIR_DEFAULT)}")

context_dir_option=--context-dir-path $(context_dir)
user_id_option=--user-id $(USER_ID)
stoobly_exec_options=--profile $(EXEC_WORKFLOW_NAME) -p $(EXEC_WORKFLOW_NAME)
workflow_down_options=$(user_id_option)
workflow_service_options=$(shell echo $$STOOBLY_WORKFLOW_SERVICE_OPTIONS)
workflow_up_options=$(context_dir_option) --ca-certs-dir-path $(ca_certs_dir) --certs-dir-path $(certs_dir) --from-make $(user_id_option)

app_data_dir=$(app_dir)/.stoobly
app_namespace_dir=$(app_data_dir)/docker
app_tmp_dir=$(app_data_dir)/tmp
data_dir=$(context_dir)/.stoobly
dockerfile_path=$(app_namespace_dir)/.Dockerfile.context
docker_compose_file_path=$(app_namespace_dir)/stoobly-ui/exec/.docker-compose.exec.yml
workflow_run_script=$(app_data_dir)/tmp/run.sh

# Commands
docker_command=docker
docker_compose_command=$(docker_command) compose
exec_env=export CA_CERTS_DIR="$(ca_certs_dir)" && export USER_ID=$(USER_ID)
exec_up=$(docker_compose_command) -f "$(docker_compose_file_path)" $(stoobly_exec_options) up --remove-orphans
source_env=set -a; [ -f .env ] && source .env; set +a

# Build base image
stoobly_exec_build=$(docker_command) build $(stoobly_exec_build_args) $(app_namespace_dir)
stoobly_exec_build_args=-f "$(dockerfile_path)" -t stoobly.$(USER_ID) --build-arg USER_ID=$(USER_ID) $(PULL_OPTION) --quiet

# Exec any
stoobly_exec=$(stoobly_exec_build) && $(stoobly_exec_env) && $(exec_up)
stoobly_exec_env=$(source_env) && $(exec_env) && export CONTEXT_DIR="$(context_dir)" 

# Exec workflow run
# Because scaffold is stored in the application source code directory, 
# when running a scaffold command from within a container,
# it needs access to $(app_dir) rather than $(context_dir)
stoobly_exec_run=$(stoobly_exec_build) && $(stoobly_exec_run_env) && $(exec_up)
stoobly_exec_run_env=$(source_env) && $(exec_env) && export CONTEXT_DIR="$(app_dir)"

# Workflow run
workflow_run=$(source_env) && bash "$(workflow_run_script)"

ca-cert/install: stoobly/install
	@if [ ! -d "$$HOME/.mitmproxy" ]; then \
		read -p "Installing CA certificate is required for $(WORKFLOW)ing requests, continue? (y/N) " confirm && \
		if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
			echo "Running stoobly-agent ca-cert install..."; \
			stoobly-agent ca-cert install; \
		else \
			echo "You can install the CA certificate later by running: stoobly-agent ca-cert install"; \
		fi \
	fi
certs:
	@export EXEC_COMMAND=bin/.mkcert && \
	$(stoobly_exec)
command/install:
	$(eval COMMAND=install)
command/uninstall:
	$(eval COMMAND=uninstall)
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
		exit 1; \
	fi
intercept/disable:
	@export EXEC_COMMAND=bin/.disable && \
	$(stoobly_exec)
intercept/enable:
	@export EXEC_COMMAND=bin/.enable && \
	export EXEC_ARGS=$(scenario_key) && \
	$(stoobly_exec)
mock: workflow/mock ca-cert/install workflow/hostname/install nameservers workflow/up
mock/services: workflow/mock workflow/services
mock/logs: workflow/mock workflow/logs
mock/down: workflow/mock workflow/down workflow/hostname/uninstall
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
record/down: workflow/record workflow/down workflow/hostname/uninstall
record/services: workflow/record workflow/services
record/logs: workflow/record workflow/logs
scenario/create:
# Create a scenario
	@export EXEC_COMMAND=bin/.create && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(name)" && \
	$(stoobly_exec)
scenario/delete:
# Delete a scenario
	@export EXEC_COMMAND=bin/.delete && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
scenario/list:
# List scenarios
	@export EXEC_COMMAND=bin/.list && \
	export EXEC_OPTIONS="$(options)" && \
	$(stoobly_exec)
scenario/reset:
# Resets a scenario to its last snapshot
	@export EXEC_COMMAND=bin/.reset && \:
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
scenario/snapshot:
# Create committable files for a scenario
	@export EXEC_COMMAND=bin/.snapshot && \
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
test/down: workflow/test workflow/down
tmpdir:
	@mkdir -p $(app_tmp_dir)
workflow/down:
	@export EXEC_COMMAND=bin/.down && \
	export EXEC_OPTIONS="$(workflow_down_options) $(workflow_service_options) $(options)" && \
	export EXEC_ARGS="$(WORKFLOW)" && \
	$(stoobly_exec_run) && \
	$(workflow_run)
workflow/hostname: stoobly/install
	@read -p "Do you want to $(COMMAND) hostname(s) in /etc/hosts? (y/N) " confirm && \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		CURRENT_VERSION=$$(stoobly-agent --version); \
		REQUIRED_VERSION="1.4.0"; \
		if [ "$$(printf '%s\n' "$$REQUIRED_VERSION" "$$CURRENT_VERSION" | sort -V | head -n 1)" != "$$REQUIRED_VERSION" ]; then \
			echo "stoobly-agent version $$REQUIRED_VERSION required. Please run: pipx upgrade stoobly-agent"; \
			exit 1; \
		fi; \
		echo "Running stoobly-agent scaffold hostname $(COMMAND) $(workflow_service_options)"; \
		stoobly-agent scaffold hostname $(COMMAND) --app-dir-path $(app_dir) --workflow $(WORKFLOW) $(workflow_service_options); \
	fi
workflow/hostname/install: command/install workflow/hostname
workflow/hostname/uninstall: command/uninstall workflow/hostname  
workflow/logs:
	@export EXEC_COMMAND=bin/.logs && \
	export EXEC_OPTIONS="$(workflow_service_options) $(options)" && \
	export EXEC_ARGS="$(WORKFLOW)" && \
	$(stoobly_exec_run) && \
	$(workflow_run)
workflow/mock:
	$(eval WORKFLOW=mock)
workflow/record:
	$(eval WORKFLOW=record)
workflow/services:
	@export EXEC_COMMAND=bin/.services && \
	export EXEC_OPTIONS="$(workflow_service_options) $(options)" && \
	export EXEC_ARGS="$(WORKFLOW)" && \
	$(stoobly_exec_run)
workflow/test:
	$(eval WORKFLOW=test)
workflow/up:
	@export EXEC_COMMAND=bin/.up && \
	export EXEC_OPTIONS="$(workflow_up_options) $(workflow_service_options) $(options)" && \
	export EXEC_ARGS="$(WORKFLOW)" && \
	$(stoobly_exec_run) && \
	$(workflow_run)