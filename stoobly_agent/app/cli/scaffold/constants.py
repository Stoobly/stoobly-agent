import os

from typing import Literal

from stoobly_agent.config.data_dir import CERTS_DIR_NAME, DATA_DIR_NAME

APP_DIR_ENV = 'APP_DIR'
APP_NETWORK_ENV = 'APP_NETWORK'
APP_NAME_ENV = 'APP_NAME'
BIN_FOLDER_NAME = 'bin'
CA_CERTS_DIR_ENV = 'CA_CERTS_DIR'
CERTS_DIR_ENV = 'CERTS_DIR'
COMPOSE_TEMPLATE = '.docker-compose.{workflow}.yml'
CONFIG_FILE = '.config.yml'
CONTEXT_DIR_ENV = 'CONTEXT_DIR'
DOCKER_NAMESPACE = 'docker'
ENV_FILE = '.env'
NAMESERVERS_FILE = '.nameservers'
PUBLIC_FOLDER_NAME = 'public'
SERVICE_DETACHED = '${SERVICE_DETACHED}'
SERVICE_DETACHED_ENV = 'SERVICE_DETACHED'
SERVICE_HOSTNAME = '${SERVICE_HOSTNAME}'
SERVICE_HOSTNAME_ENV = 'SERVICE_HOSTNAME'
SERVICE_DNS = '${SERVICE_DNS}'
SERVICE_DNS_ENV = 'SERVICE_DNS'
SERVICE_NAME = '${SERVICE_NAME}'
SERVICE_NAME_ENV = 'SERVICE_NAME'
SERVICE_PROXY_MODE = '${SERVICE_PROXY_MODE}'
SERVICE_PROXY_MODE_ENV = 'SERVICE_PROXY_MODE'
SERVICE_SCHEME = '${SERVICE_SCHEME}'
SERVICE_SCHEME_ENV = 'SERVICE_SCHEME'
SERVICE_PORT = '${SERVICE_PORT}'
SERVICE_PORT_ENV = 'SERVICE_PORT'
SERVICE_PRIORITY_ENV = 'SERVICE_PRIORITY'
SERVICE_SCRIPTS = '${SERVICE_SCRIPTS}'
SERVICE_SCRIPTS_DIR = '/usr/local/bin/services'
SERVICE_SCRIPTS_ENV = 'SERVICE_SCRIPTS'
STOOBLY_HOME_DIR = '/home/stoobly'
STOOBLY_DATA_DIR = os.path.join(STOOBLY_HOME_DIR, DATA_DIR_NAME)
STOOBLY_CERTS_DIR = os.path.join(STOOBLY_DATA_DIR, CERTS_DIR_NAME)
USER_ID_ENV = 'USER_ID'
VIRTUAL_HOST_ENV = 'VIRTUAL_HOST'
VIRTUAL_PORT_ENV = 'VIRTUAL_PORT'
VIRTUAL_PROTO_ENV = 'VIRTUAL_PROTO'
WORKFLOW_CONTAINER_CONFIGURE = 'configure'
WORKFLOW_CONTAINER_INIT = 'init'
WORKFLOW_CONTAINER_PROXY = 'proxy'
WORKFLOW_CONTAINER_TEMPLATE = '{service_name}.{container}'
WORKFLOW_CONTAINER_CONFIGURE_TEMPLATE = '{service_name}.' + WORKFLOW_CONTAINER_CONFIGURE
WORKFLOW_CONTAINER_INIT_TEMPLATE = '{service_name}.' + WORKFLOW_CONTAINER_INIT
WORKFLOW_CONTAINER_PROXY_TEMPLATE = '{service_name}.' + WORKFLOW_CONTAINER_PROXY
WORKFLOW_EXEC_TYPE = 'exec'
WORKFLOW_MOCK_TYPE = 'mock'
WORKFLOW_NAME = '${WORKFLOW_NAME}'
WORKFLOW_NAME_ENV = 'WORKFLOW_NAME'
WORKFLOW_NAMESPACE_ENV = 'WORKFLOW_NAMESPACE'
WORKFLOW_RECORD_TYPE = 'record'
WORKFLOW_SCRIPTS = '${WORKFLOW_SCRIPTS}'
WORKFLOW_SCRIPTS_DIR = '/usr/local/bin/workflows'
WORKFLOW_SCRIPTS_ENV = 'WORKFLOW_SCRIPTS'
WORKFLOW_TEMPLATE = '${WORKFLOW_TEMPLATE}'
WORKFLOW_TEMPLATE_ENV = 'WORKFLOW_TEMPLATE'
WORKFLOW_TEST_TYPE = 'test'

WORKFLOW_TEMPLATE_OPTION = Literal[WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]
