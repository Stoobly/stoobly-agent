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
source_env=set -a; [ -f .env ] && source .env; set +a

docker_compose_file_path=$(data_dir)/docker/mock-ui/exec/.docker-compose.exec.yml
stoobly_exec_args=--profile $(WORKFLOW_NAME) -p $(WORKFLOW_NAME) up --build --remove-orphans
stoobly_exec_env=export CONTEXT_DIR=$(context_dir) && export USER_ID=$$UID
stoobly_exec=$(stoobly_exec_env) && $(source_env) && $(docker_compose_command) -f "$(docker_compose_file_path)" $(stoobly_exec_args)
stoobly_exec_run_env=export USER_ID=$$UID
# Because scaffold is stored in the APP_DIR, when running a scaffold command from within a container,
# it needs access to APP_DIR rather than CONTEXT_DIR
stoobly_exec_run=$(stoobly_exec_run_env) && $(source_env) && CONTEXT_DIR=$(app_dir) $(docker_compose_command) -f "$(docker_compose_file_path)" $(stoobly_exec_args)

run_script=$(data_dir)/tmp/run.sh
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
	export EXEC_ARGS="$(services) mock" && \
	$(stoobly_exec) && \
	$(workflow_run)
mock/stop:
	export EXEC_COMMAND=bin/.stop && \
	export EXEC_ARGS="$(services) mock" && \
	$(stoobly_exec) && \
	$(workflow_run)
record:
	export EXEC_COMMAND=bin/.run && \
	export EXEC_ARGS="$(services) record" && \
	$(stoobly_exec) && \
	$(workflow_run)
record/stop:
	export EXEC_COMMAND=bin/.stop && \
	export EXEC_ARGS="$(services) record" && \
	$(stoobly_exec) && \
	$(workflow_run)
scenario/create:
# Create a scenario
	export EXEC_COMMAND=bin/.create && \
	export EXEC_ARGS=$(name) && \
	$(stoobly_exec)
scenario/delete:
# Delete a scenario
	export EXEC_COMMAND=bin/.delete && \
	export EXEC_ARGS=$(key) && \
	$(stoobly_exec)
scenario/reset:
# Resets a scenario to its last snapshot
	export EXEC_COMMAND=bin/.reset && \
	export EXEC_ARGS=$(key) && \
	$(stoobly_exec)
scenario/snapshot:
# Create committable files for a scenario
	export EXEC_COMMAND=bin/.snapshot && \
	export EXEC_ARGS=$(key) && \
	$(stoobly_exec)