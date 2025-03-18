import os

CORE_BUILD_SERVICE_NAME = 'build'
CORE_ENTRYPOINT_SERVICE_NAME = 'entrypoint'
CORE_GATEWAY_SERVICE_NAME = 'gateway'
CORE_MOCK_UI_SERVICE_NAME = 'stoobly-ui'
CORE_SERVICES = [
  CORE_BUILD_SERVICE_NAME, CORE_ENTRYPOINT_SERVICE_NAME, CORE_MOCK_UI_SERVICE_NAME, CORE_GATEWAY_SERVICE_NAME 
]

CORE_MOCK_WORKFLOW = 'mock'
CORE_RECORD_WORKFLOW = 'record'

CUSTOM_BUILD = os.path.join('bin', 'build')
CUSTOM_CONFIGURE = os.path.join('bin', 'configure')
CUSTOM_INIT = os.path.join('bin', 'init')
CUSTOM_FIXTURES = 'fixtures.yml'
CUSTOM_LIFECYCLE_HOOKS = os.path.join('lifecycle_hooks.py')
MAINTAINED_CONFIGURE = os.path.join('bin', '.configure')
MAINTAINED_INIT = os.path.join('bin', '.init')
MAINTAINED_PUBLIC = os.path.join('public', '.gitignore')

MOCK_WORKFLOW_MAINTAINED_FILES = [
  MAINTAINED_CONFIGURE,
  MAINTAINED_INIT,
  MAINTAINED_PUBLIC
]

MOCK_WORKFLOW_CUSTOM_FILES = [
  CUSTOM_BUILD,
  CUSTOM_CONFIGURE,
  CUSTOM_FIXTURES,
  CUSTOM_INIT,
  CUSTOM_LIFECYCLE_HOOKS,
]

RECORD_WORKFLOW_MAINTAINED_FILES = [
  MAINTAINED_CONFIGURE,
  MAINTAINED_INIT
]

RECORD_WORKFLOW_CUSTOM_FILES = [
  CUSTOM_BUILD,
  CUSTOM_CONFIGURE,
  CUSTOM_INIT,
  CUSTOM_LIFECYCLE_HOOKS
]

TEST_WORKFLOW_MAINTAINED_FILES = [
  MAINTAINED_CONFIGURE,
  MAINTAINED_INIT,
  MAINTAINED_PUBLIC
]

TEST_WORKFLOW_CUSTOM_FILES = [
  CUSTOM_BUILD,
  CUSTOM_CONFIGURE,
  CUSTOM_FIXTURES,
  CUSTOM_INIT,
  CUSTOM_LIFECYCLE_HOOKS
]

SERVICE_HOSTNAME_BUILD_ARG = 'SERVICE_HOSTNAME'
