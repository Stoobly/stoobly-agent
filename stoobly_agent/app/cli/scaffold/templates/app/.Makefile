# Overridable Environment Variables
#
# STOOBLY_APP_DIR: path to the application source code directory
# STOOBLY_CONTEXT_DIR: path to the folder containing the .stoobly folder
# STOOBLY_CERTS_DIR: path to a folder to store certs
# STOOBLY_WORKFLOW_RUN_OPTIONS: extra options to pass to 'stoobly-agent scaffold workflow run' command

# Constants
DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
WORKFLOW_NAME := exec

CONTEXT_DIR_DEFAULT := $(realpath $(DIR)/../..)

# Configuration
app_dir=$$(realpath "$${STOOBLY_APP_DIR:-$(CONTEXT_DIR_DEFAULT)}")
certs_dir=$$(realpath "$${STOOBLY_CERTS_DIR:-$(app_data_dir)/certs}")
context_dir=$$(realpath "$${STOOBLY_CONTEXT_DIR:-$(CONTEXT_DIR_DEFAULT)}")
workflow_run_options=$${STOOBLY_WORKFLOW_RUN_OPTIONS:+$$STOOBLY_WORKFLOW_RUN_OPTIONS }

app_data_dir=$(app_dir)/.stoobly
data_dir=$(context_dir)/.stoobly

# Commands
docker_compose_command=docker compose
source_env=set -a; [ -f .env ] && source .env; set +a

docker_compose_file_path=$(app_data_dir)/docker/stoobly-ui/exec/.docker-compose.exec.yml
stoobly_exec_args=--profile $(WORKFLOW_NAME) -p $(WORKFLOW_NAME) up --build --remove-orphans
stoobly_exec_env=export CONTEXT_DIR=$(context_dir) && export USER_ID=$$UID
stoobly_exec=$(stoobly_exec_env) && $(source_env) && $(docker_compose_command) -f "$(docker_compose_file_path)" $(stoobly_exec_args)

# Because scaffold is stored in the APP_DIR, when running a scaffold command from within a container,
# it needs access to APP_DIR rather than CONTEXT_DIR
stoobly_exec_run_env=export USER_ID=$$UID
stoobly_exec_run=$(stoobly_exec_run_env) && $(source_env) && CONTEXT_DIR=$(app_dir) $(docker_compose_command) -f "$(docker_compose_file_path)" $(stoobly_exec_args)

run_script=$(app_data_dir)/tmp/run.sh
run_env=export APP_DIR="$(app_dir)" && export CERTS_DIR="$(certs_dir)" && export CONTEXT_DIR="$(context_dir)"
workflow_run=$(run_env) && $(source_env) && bash "$(run_script)"

cert:
	if [ -z "$$(which mkcert)" ]; then \
		echo "Error: missing mkcert command"; \
	else \
		mkdir -p "$(certs_dir)" && \
		cd "$(certs_dir)" && \
		mkcert --install && \
		mkcert $(hostname) && \
		cp $(hostname).pem $(hostname).crt && \
		cp $(hostname)-key.pem $(hostname).key; \
	fi
intercept/disable:
	export EXEC_COMMAND=bin/.disable && \
	$(stoobly_exec)
intercept/enable:
	export EXEC_COMMAND=bin/.enable && \
	export EXEC_ARGS=$(scenario_key) && \
	$(stoobly_exec)
mock:
	export EXEC_COMMAND=bin/.run && \
	export EXEC_OPTIONS="$(workflow_run_options)$(options)" && \
	export EXEC_ARGS="mock" && \
	$(stoobly_exec_run) && \
	$(workflow_run)
mock/stop:
	export EXEC_COMMAND=bin/.stop && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="mock" && \
	$(stoobly_exec_run) && \
	$(workflow_run)
record:
	export EXEC_COMMAND=bin/.run && \
	export EXEC_OPTIONS="$(workflow_run_options)$(options)" && \
	export EXEC_ARGS="record" && \
	$(stoobly_exec_run) && \
	$(workflow_run)
record/stop:
	export EXEC_COMMAND=bin/.stop && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="record" && \
	$(stoobly_exec_run) && \
	$(workflow_run)
scenario/create:
# Create a scenario
	export EXEC_COMMAND=bin/.create && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(name)" && \
	$(stoobly_exec)
scenario/delete:
# Delete a scenario
	export EXEC_COMMAND=bin/.delete && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
scenario/reset:
# Resets a scenario to its last snapshot
	export EXEC_COMMAND=bin/.reset && \:
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
scenario/snapshot:
# Create committable files for a scenario
	export EXEC_COMMAND=bin/.snapshot && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="$(key)" && \
	$(stoobly_exec)
test:
	export EXEC_COMMAND=bin/.run && \
	export EXEC_OPTIONS="$(workflow_run_options)$(options)" && \
	export EXEC_ARGS="test" && \
	$(stoobly_exec_run) && \
	$(workflow_run)
test/stop:
	export EXEC_COMMAND=bin/.stop && \
	export EXEC_OPTIONS="$(options)" && \
	export EXEC_ARGS="test" && \
	$(stoobly_exec_run) && \
	$(workflow_run)