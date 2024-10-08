# Overridable Environment Variables
#
# CONTEXT_DIR
# APP_DIR
# CERTS_DIR

# Constants
WORKFLOW_NAME := exec
DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
DATA_DIR_DEFAULT := $(realpath $(DIR)/..)
CONTEXT_DIR_DEFAULT := $(realpath $(DIR)/../..)

# Configuration
context_dir=$$(realpath "$${CONTEXT_DIR:-$(CONTEXT_DIR_DEFAULT)}")
data_dir=$(context_dir)/.stoobly
app_dir=$$(realpath "$${APP_DIR:-$(context_dir)}")
certs_dir=$$(realpath "$${CERTS_DIR:-$(data_dir)/certs}")

# Commands
docker_compose_command=docker compose
docker_compose_file_path=$(data_dir)/docker/mock-ui/exec/.docker-compose.exec.yml
docker_compose_args=--profile $(WORKFLOW_NAME) -p $(WORKFLOW_NAME) up --build
docker_compose_stoobly_exec=export CONTEXT_DIR=$(context_dir) && $(docker_compose_command) -f "$(docker_compose_file_path) $(docker_compose_args)"

run_script=$(data_dir)/tmp/run.sh
env_exports=export APP_DIR="$(app_dir)" && export CERTS_DIR="$(certs_dir)" && export CONTEXT_DIR="$(context_dir)" && source .env 2> /dev/null
docker_compose_stoobly_exec_run=$(env_exports) && bash "$(run_script)"

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
mock:
	export EXEC_COMMAND=bin/run && \
	export EXEC_ARGS="$(services) mock" && \
	$(docker_compose_stoobly_exec_run)
mock/apply:
# Build local mock scenarios from snapshots
	export EXEC_COMMAND=bin/apply && \
	$(docker_compose_stoobly_exec)
mock/create:
# Creates a scenario to group mocked requests
	export EXEC_COMMAND=bin/create && \
	export EXEC_ARGS=$(key) && \
	$(docker_compose_stoobly_exec)
mock/delete:
# Deletes a mock scenario
	export EXEC_COMMAND=bin/delete && \
	export EXEC_ARGS=$(key) && \
	$(docker_compose_stoobly_exec)
mock/stop:
	export EXEC_COMMAND=bin/stop && \
	export EXEC_ARGS="$(services) mock" && \
	$(docker_compose_stoobly_exec_run)
mock/reset:
# Resets a mock scenario to last snapshot
	export EXEC_COMMAND=bin/reset && \
	export EXEC_ARGS=$(key) && \
	$(docker_compose_stoobly_exec)
mock/snapshot:
# Converts mocks to committable files
	export EXEC_COMMAND=bin/snapshot && \
	export EXEC_ARGS=$(key) && \
	$(docker_compose_stoobly_exec)
record:
	export EXEC_COMMAND=bin/run && \
	export EXEC_ARGS="$(services) record" && \
	$(docker_compose_stoobly_exec_run)
record/stop:
	export EXEC_COMMAND=bin/stop && \
	export EXEC_ARGS="$(services) record" && \
	$(docker_compose_stoobly_exec_run)
test:
	export CONTEXT_DIR="$${CONTEXT_DIR:-$(CONTEXT_DIR_DEFAULT)}" && \
	export APP_DIR="$${APP_DIR:-$(app_dir)}" && \
	echo $$CONTEXT_DIR && \
	echo $$APP_DIR
test2:
	export CONTEXT_DIR=/tmp && \
	echo $(context_dir) && \
	echo $(certs_dir)