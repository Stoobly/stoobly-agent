import pytest
import yaml

from stoobly_agent.app.cli.helpers.opencli_resolve import (
  MAIN_GROUP,
  OpencliResolveError,
  list_group_rows,
  list_groups,
  read_document,
  registered_groups,
  resolve_path,
)

LISTABLE_GROUPS = [
  'endpoint',
  'intercept',
  'request',
  'scaffold',
  'scenario',
  'setting',
  'snapshot',
]

ALL_GROUPS = [MAIN_GROUP] + LISTABLE_GROUPS


class TestListGroups:
  def test_excludes_main(self):
    assert MAIN_GROUP not in list_groups()

  def test_includes_listable_groups(self):
    assert set(LISTABLE_GROUPS) <= set(list_groups())

  def test_returns_sorted(self):
    groups = list_groups()
    assert groups == sorted(groups)


class TestRegisteredGroups:
  def test_includes_main_first(self):
    groups = registered_groups()
    assert groups[0] == MAIN_GROUP
    assert set(ALL_GROUPS) <= set(groups)


class TestResolvePath:
  @pytest.mark.parametrize('group', ALL_GROUPS)
  def test_group_path_is_file(self, group: str):
    path = resolve_path(group)
    assert path.is_file()
    assert path.name == f'{group}.opencli.yaml'

  def test_unknown_group_raises(self):
    with pytest.raises(OpencliResolveError) as exc_info:
      resolve_path('nope')

    message = str(exc_info.value)
    assert "Unknown OpenCLI group 'nope'" in message
    assert 'main' in message


class TestReadDocument:
  @pytest.mark.parametrize('group', ALL_GROUPS)
  def test_group_is_valid_opencli(self, group: str):
    data = yaml.safe_load(read_document(group))

    assert data.get('opencli') == '0.1'
    expected_name = 'stoobly-agent' if group == MAIN_GROUP else group
    assert data['command']['name'] == expected_name

  def test_defaults_to_main(self):
    data = yaml.safe_load(read_document())
    assert data['command']['name'] == 'stoobly-agent'


class TestListGroupRows:
  def test_rows_exclude_main(self):
    rows = list_group_rows()
    names = [row['name'] for row in rows]
    assert MAIN_GROUP not in names
    assert set(LISTABLE_GROUPS) <= set(names)
    assert all(row.get('summary') for row in rows)
