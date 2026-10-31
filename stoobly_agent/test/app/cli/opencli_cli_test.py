import json

import pytest
from click.testing import CliRunner

from stoobly_agent.cli import main


@pytest.fixture
def runner():
  return CliRunner()


LISTABLE_GROUPS = [
  'endpoint',
  'intercept',
  'request',
  'scaffold',
  'scenario',
  'setting',
  'snapshot',
]

ALL_GROUPS = ['main'] + LISTABLE_GROUPS


class TestOpencliList:
  def test_lists_expected_groups_as_table(self, runner: CliRunner):
    result = runner.invoke(main, ['opencli', 'list'])

    assert result.exit_code == 0
    assert 'name' in result.output
    assert 'summary' in result.output
    for group in LISTABLE_GROUPS:
      assert group in result.output
    assert 'main' not in result.output.splitlines()[0]  # header is name/summary
    # No data row for main
    assert not any(
      line.split()[:1] == ['main']
      for line in result.output.splitlines()
      if line.strip() and not line.startswith('name')
    )

  def test_lists_json(self, runner: CliRunner):
    result = runner.invoke(main, ['opencli', 'list', '--format', 'json'])

    assert result.exit_code == 0
    rows = json.loads(result.output)
    assert isinstance(rows, list)
    names = [row['name'] for row in rows]
    assert 'main' not in names
    assert set(names) >= set(LISTABLE_GROUPS)
    assert 'summary' in rows[0]


class TestOpencliShow:
  @pytest.mark.parametrize('group', ALL_GROUPS)
  def test_shows_group(self, runner: CliRunner, group: str):
    result = runner.invoke(main, ['opencli', 'show', group])

    assert result.exit_code == 0
    expected_name = 'stoobly-agent' if group == 'main' else group
    assert f'name: {expected_name}' in result.output
    assert 'opencli:' in result.output

  def test_defaults_to_main(self, runner: CliRunner):
    result = runner.invoke(main, ['opencli', 'show'])

    assert result.exit_code == 0
    assert 'name: stoobly-agent' in result.output
    assert 'opencli:' in result.output

  def test_unknown_group_fails(self, runner: CliRunner):
    result = runner.invoke(main, ['opencli', 'show', 'nope'])

    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert "Unknown OpenCLI group 'nope'" in combined
    assert 'main' in combined
