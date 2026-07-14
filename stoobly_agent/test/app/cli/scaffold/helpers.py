import os

from stoobly_agent.app.cli.scaffold.constants import CORE_WORKFLOWS, SERVICES_NAMESPACE
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
