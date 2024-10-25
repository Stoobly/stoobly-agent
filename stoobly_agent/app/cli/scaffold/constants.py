from typing import Literal

APP_NETWORK_ENV = 'APP_NETWORK'
CERTS_DIR_ENV = 'CERTS_DIR'
COMPOSE_TEMPLATE = '.docker-compose.{workflow}.yml'
CONFIG_FILE = '.config.yml'
CONTEXT_DIR_ENV = 'CONTEXT_DIR'
CORE_SERVICES = ['build', 'gateway', 'mock-ui']
DIST_FOLDER_NAME = 'dist'
DOCKER_NAMESPACE = 'docker'
ENV_FILE = '.env'
FIXTURES_FOLDER_NAME = 'fixtures'
SERVICE_DETACHED = '${SERVICE_DETACHED}'
SERVICE_DETACHED_ENV = 'SERVICE_DETACHED'
SERVICE_DOCKER_COMPOSE_PATH = '${SERVICE_DOCKER_COMPOSE_PATH}'
SERVICE_DOCKER_COMPOSE_PATH_ENV = 'SERVICE_DOCKER_COMPOSE_PATH'
SERVICE_HOSTNAME = '${SERVICE_HOSTNAME}'
SERVICE_HOSTNAME_ENV = 'SERVICE_HOSTNAME'
SERVICE_DNS = '${SERVICE_DNS}'
SERVICE_DNS_ENV = 'SERVICE_DNS'
SERVICE_NAME_ENV = 'SERVICE_NAME'
SERVICE_PROXY_MODE = '${SERVICE_PROXY_MODE}'
SERVICE_PROXY_MODE_ENV = 'SERVICE_PROXY_MODE'
SERVICE_SCHEME = '${SERVICE_SCHEME}'
SERVICE_SCHEME_ENV = 'SERVICE_SCHEME'
SERVICE_PORT = '${SERVICE_PORT}'
SERVICE_PORT_ENV = 'SERVICE_PORT'
SERVICE_PRIORITY_ENV = 'SERVICE_PRIORITY'
STOOBLY_HOME_DIR = '/home/stoobly'
USER_ID_ENV = 'USER_ID'
WORKFLOW_CUSTOM_FILTER = 'custom'
WORKFLOW_MOCK_TYPE = 'mock'
WORKFLOW_NAME_ENV = 'WORKFLOW_NAME'
WORKFLOW_RECORD_TYPE = 'record'
WORKFLOW_TEST_TYPE = 'test'
WORKFLOW_TEMPLATE = Literal[WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]

