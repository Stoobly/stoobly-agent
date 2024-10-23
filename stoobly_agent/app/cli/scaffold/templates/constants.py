import os

CORE_BUILD_SERVICE_NAME = 'build'
CORE_ENABLE_INTERCEPT_NAME = 'enable-intercept'
CORE_MOCK_UI_SERVICE_NAME = 'mock-ui'
CORE_GATEWAY_SERVICE_NAME = 'gateway'
CORE_TEST_SERVICE_NAME = 'tests'
CORE_SERVICES = [
  CORE_BUILD_SERVICE_NAME, CORE_ENABLE_INTERCEPT_NAME, CORE_MOCK_UI_SERVICE_NAME, CORE_GATEWAY_SERVICE_NAME, CORE_TEST_SERVICE_NAME
]

CORE_MOCK_WORKFLOW = 'mock'
CORE_RECORD_WORKFLOW = 'record'

CUSTOM_CONFIGURE = os.path.join('bin', 'configure')
CUSTOM_INIT = os.path.join('bin', 'init')
MAINTAINED_CONFIGURE = os.path.join('bin', '.configure')
MAINTAINED_INIT = os.path.join('bin', '.init')

MOCK_WORKFLOW_MAINTAINED_FILES = [
  MAINTAINED_CONFIGURE,
  MAINTAINED_INIT
]

MOCK_WORKFLOW_CUSTOM_FILES = [
  os.path.join('bin', 'build'),
  os.path.join('bin', 'init'),
  CUSTOM_CONFIGURE,
  os.path.join('.keep'),
  os.path.join('lifecycle_hooks.py'),
]

RECORD_WORKFLOW_MAINTAINED_FILES = [
  MAINTAINED_CONFIGURE,
  MAINTAINED_INIT
]

RECORD_WORKFLOW_CUSTOM_FILES = [
  os.path.join('bin', 'build'),
  os.path.join('bin', 'init'),
  CUSTOM_CONFIGURE,
  os.path.join('.keep'),
  os.path.join('lifecycle_hooks.py'),
]

TEST_WORKFLOW_MAINTAINED_FILES = [
  MAINTAINED_CONFIGURE,
  MAINTAINED_INIT
]

TEST_WORKFLOW_CUSTOM_FILES = [
  os.path.join('bin', 'build'),
  os.path.join('bin', 'init'),
  CUSTOM_CONFIGURE,
  os.path.join('.keep'),
  os.path.join('lifecycle_hooks.py'),
]

SERVICE_HOSTNAME_BUILD_ARG = 'SERVICE_HOSTNAME'