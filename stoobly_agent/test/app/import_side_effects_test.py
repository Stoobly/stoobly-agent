import os
import subprocess
import sys

import pytest

# Importing these modules must not create the default data dir (~/.stoobly)
MODULES = [
  'stoobly_agent.app.cli.helpers.certificate_authority',
  'stoobly_agent.app.proxy.intercept_handler',
  'stoobly_agent.app.cli.request_cli',
]


@pytest.mark.parametrize('module', MODULES)
def test_import_does_not_create_home_data_dir(module, tmp_path):
  home = tmp_path / 'home'
  cwd = tmp_path / 'cwd'
  home.mkdir()
  cwd.mkdir()

  env = {key: value for key, value in os.environ.items() if not key.startswith('STOOBLY')}
  env['HOME'] = str(home)

  result = subprocess.run(
    [sys.executable, '-c', f'import {module}'],
    cwd=cwd,
    env=env,
    capture_output=True,
    text=True,
  )

  assert result.returncode == 0, result.stderr
  assert sorted(os.listdir(home)) == [], f'importing {module} created {os.listdir(home)}'
