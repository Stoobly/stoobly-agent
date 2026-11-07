import os
from unittest.mock import MagicMock

import stoobly_agent.app.cli.scaffold.templates as templates_pkg
from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_RECORD_TYPE
from stoobly_agent.app.cli.scaffold.templates.constants import (
  CUSTOM_FIXTURES,
  CUSTOM_PUBLIC_GITIGNORE,
)
from stoobly_agent.app.cli.scaffold.templates.factory import custom_files


class TestRecordCustomFiles:
  def test_includes_fixtures_and_public_when_hostname_present(self):
    workflow_builder = MagicMock()
    workflow_builder.config.hostname = 'example.com'

    files = custom_files(WORKFLOW_RECORD_TYPE, workflow_builder)

    assert CUSTOM_FIXTURES in files
    assert CUSTOM_PUBLIC_GITIGNORE in files

  def test_omits_public_when_no_hostname(self):
    workflow_builder = MagicMock()
    workflow_builder.config.hostname = None

    files = custom_files(WORKFLOW_RECORD_TYPE, workflow_builder)

    assert CUSTOM_FIXTURES in files
    assert CUSTOM_PUBLIC_GITIGNORE not in files

  def test_record_workflow_templates_exist(self):
    templates_dir = os.path.join(os.path.dirname(templates_pkg.__file__), 'workflow', 'record')

    assert os.path.isfile(os.path.join(templates_dir, 'fixtures.yml'))
    assert os.path.isfile(os.path.join(templates_dir, 'public', '.gitignore'))
