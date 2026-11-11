import os

from stoobly_agent.app.cli.scaffold.constants import CORE_WORKFLOWS, SERVICES_NAMESPACE, WORKFLOW_TEST_TYPE
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_BUILD_SERVICE_NAME, CUSTOM_INIT
from stoobly_agent.config.data_dir import DATA_DIR_NAME


def enable_intercept_in_build_init_scripts(app_dir_path: str):
  """Append intercept enable to each workflow's build init script after app create."""
  enable_lines = [
    '',
    'echo "Enabling intercept..."',
    'stoobly-agent intercept enable',
    '',
  ]
  for workflow_name in CORE_WORKFLOWS:
    init_path = os.path.join(
      app_dir_path, DATA_DIR_NAME, SERVICES_NAMESPACE, CORE_BUILD_SERVICE_NAME, workflow_name, CUSTOM_INIT
    )
    if not os.path.exists(init_path):
      continue

    with open(init_path, 'r') as fp:
      contents = fp.read()

    if 'stoobly-agent intercept enable' in contents:
      continue

    with open(init_path, 'a') as fp:
      if contents and not contents.endswith('\n'):
        fp.write('\n')
      fp.write('\n'.join(enable_lines))


def set_workflow_mode_and_policy(app_dir_path: str, workflow_name: str, mode: str, policy: str):
  """Append intercept mode/policy configure to a workflow's build init script."""
  init_path = os.path.join(
    app_dir_path, DATA_DIR_NAME, SERVICES_NAMESPACE, CORE_BUILD_SERVICE_NAME, workflow_name, CUSTOM_INIT
  )
  if not os.path.exists(init_path):
    raise FileNotFoundError(f"Missing {workflow_name} workflow build init: {init_path}")

  configure_cmd = f'stoobly-agent intercept configure --mode {mode} --policy {policy}'
  with open(init_path, 'r') as fp:
    contents = fp.read()

  if configure_cmd in contents:
    return

  lines = [
    '',
    f'echo "Setting {mode} policy to {policy}..."',
    configure_cmd,
    '',
  ]
  with open(init_path, 'a') as fp:
    if contents and not contents.endswith('\n'):
      fp.write('\n')
    fp.write('\n'.join(lines))


def set_test_workflow_policy_found(app_dir_path: str):
  """Override scaffold default test policy none so Test report rows are emitted."""
  set_workflow_mode_and_policy(app_dir_path, WORKFLOW_TEST_TYPE, 'test', 'found')
