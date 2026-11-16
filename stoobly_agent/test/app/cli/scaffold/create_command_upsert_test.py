import os

import yaml

from stoobly_agent.app.cli.scaffold.constants import CORE_WORKFLOWS
from stoobly_agent.app.cli.scaffold.create_command import (
  remove_scaffold_create_command,
  save_scaffold_command,
  scaffold_command_identity,
  update_scaffold_create_command,
)


class TestScaffoldCommandIdentity:
  def test_create_by_name(self):
    assert scaffold_command_identity({
      'resource': 'service',
      'action': 'create',
      'options': {'service_name': 'api'},
    }) == ('service', 'create', 'api')

  def test_create_missing_name_returns_none(self):
    assert scaffold_command_identity({
      'resource': 'app',
      'action': 'create',
      'options': {},
    }) is None

  def test_service_update_has_no_identity(self):
    # Update is not recorded as its own step; it merges into create.
    assert scaffold_command_identity({
      'resource': 'service',
      'action': 'update',
      'options': {'service_name': 'api'},
    }) is None

  def test_filter_by_pattern_and_methods(self):
    identity = scaffold_command_identity({
      'resource': 'setting',
      'action': 'filter set',
      'options': {'pattern': '.*', 'method': ['POST', 'GET']},
    })
    assert identity == ('setting', 'filter set', '.*', frozenset(['GET', 'POST']))

  def test_rewrite_includes_type_and_name(self):
    identity = scaffold_command_identity({
      'resource': 'setting',
      'action': 'rewrite set',
      'options': {
        'pattern': '.*',
        'method': ['GET'],
        'type': 'Header',
        'name': 'authorization',
      },
    })
    assert identity == (
      'setting', 'rewrite set', '.*', frozenset(['GET']), 'Header', 'authorization',
    )

  def test_rewrite_url_only_uses_absent_type_name(self):
    identity = scaffold_command_identity({
      'resource': 'setting',
      'action': 'rewrite set',
      'options': {'pattern': '.*', 'method': ['GET'], 'hostname': 'example.com'},
    })
    assert identity == ('setting', 'rewrite set', '.*', frozenset(['GET']), None, None)

  def test_intercept_omitted_workflow_means_all(self):
    assert scaffold_command_identity({
      'resource': 'intercept',
      'action': 'enable',
      'options': {},
    }) == ('intercept', 'enable', None)

  def test_intercept_core_workflows_means_all(self):
    assert scaffold_command_identity({
      'resource': 'intercept',
      'action': 'enable',
      'options': {'workflow': list(CORE_WORKFLOWS)},
    }) == ('intercept', 'enable', None)

  def test_intercept_explicit_workflow_set(self):
    assert scaffold_command_identity({
      'resource': 'intercept',
      'action': 'enable',
      'options': {'workflow': ['mock', 'record']},
    }) == ('intercept', 'enable', frozenset(['mock', 'record']))


class TestSaveScaffoldCommandUpsert:
  def test_upserts_matching_create_in_place(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'service', 'create', {
      'service_name': 'api',
      'hostname': 'api.example.com',
    })
    save_scaffold_command(path, 'app', 'create', {'app_name': 'app'})
    save_scaffold_command(path, 'service', 'create', {
      'service_name': 'api',
      'hostname': 'api.updated.com',
      'port': 443,
    })

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 2
    assert data['commands'][0]['options']['hostname'] == 'api.updated.com'
    assert data['commands'][0]['options']['port'] == 443
    assert data['commands'][1]['resource'] == 'app'

  def test_appends_different_create_names(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'service', 'create', {'service_name': 'api'})
    save_scaffold_command(path, 'service', 'create', {'service_name': 'web'})

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert [c['options']['service_name'] for c in data['commands']] == ['api', 'web']

  def test_upserts_filter_same_pattern_and_methods(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'setting', 'filter set', {
      'pattern': '.*',
      'method': ['GET'],
      'action': 'exclude',
      'mode': ['record'],
    })
    save_scaffold_command(path, 'setting', 'filter set', {
      'pattern': '.*',
      'method': ['GET'],
      'action': 'include',
      'mode': ['mock'],
    })

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 1
    assert data['commands'][0]['options']['action'] == 'include'
    assert data['commands'][0]['options']['mode'] == ['mock']

  def test_appends_filter_different_methods(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'setting', 'filter set', {
      'pattern': '.*',
      'method': ['GET'],
      'action': 'exclude',
    })
    save_scaffold_command(path, 'setting', 'filter set', {
      'pattern': '.*',
      'method': ['POST'],
      'action': 'exclude',
    })

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 2

  def test_rewrite_same_pattern_different_names_append(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    methods = ['GET', 'POST']
    save_scaffold_command(path, 'setting', 'rewrite set', {
      'pattern': '.*',
      'method': methods,
      'type': 'Header',
      'name': 'authorization',
      'value': '',
    })
    save_scaffold_command(path, 'setting', 'rewrite set', {
      'pattern': '.*',
      'method': methods,
      'type': 'Header',
      'name': 'cookie',
      'value': '',
    })

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert [c['options']['name'] for c in data['commands']] == ['authorization', 'cookie']

  def test_intercept_set_and_enable_coexist(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'intercept', 'set', {
      'mode': 'mock',
      'workflow': ['mock'],
    })
    save_scaffold_command(path, 'intercept', 'enable', {
      'workflow': ['mock'],
    })

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert [c['action'] for c in data['commands']] == ['set', 'enable']

  def test_intercept_omitted_workflow_upserts(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'intercept', 'enable', {})
    save_scaffold_command(path, 'intercept', 'enable', {'quiet': True})

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 1
    assert data['commands'][0]['options']['quiet'] is True

  def test_intercept_omitted_does_not_match_explicit_workflow(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'intercept', 'enable', {})
    save_scaffold_command(path, 'intercept', 'enable', {'workflow': ['mock']})

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 2

  def test_intercept_omitted_upserts_core_workflows(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'intercept', 'enable', {
      'workflow': list(CORE_WORKFLOWS),
    })
    save_scaffold_command(path, 'intercept', 'enable', {})

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 1
    assert 'workflow' not in data['commands'][0].get('options', {})

  def test_intercept_upsert_collapses_core_and_omitted_duplicates(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    with open(path, 'w') as fp:
      yaml.safe_dump({
        'version': 1,
        'commands': [
          {
            'resource': 'intercept',
            'action': 'enable',
            'options': {'workflow': list(CORE_WORKFLOWS)},
          },
          {
            'resource': 'service',
            'action': 'create',
            'options': {'service_name': 'google', 'port': 123},
          },
          {'resource': 'intercept', 'action': 'enable'},
          {
            'resource': 'intercept',
            'action': 'set',
            'options': {'mode': 'mock'},
          },
        ],
      }, fp, default_flow_style=False, sort_keys=False)

    save_scaffold_command(path, 'intercept', 'enable', {})

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert [c['action'] for c in data['commands']] == ['enable', 'create', 'set']
    assert data['commands'][0]['resource'] == 'intercept'
    assert 'workflow' not in data['commands'][0].get('options', {})
    assert data['commands'][1]['options']['service_name'] == 'google'
    assert data['commands'][2]['options']['mode'] == 'mock'


class TestUpdateScaffoldCreateCommand:
  def test_merges_into_matching_create(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'service', 'create', {
      'service_name': 'api',
      'hostname': 'api.example.com',
      'scheme': 'https',
      'port': 443,
    })
    save_scaffold_command(path, 'app', 'create', {'app_name': 'app'})

    update_scaffold_create_command(path, 'service', {
      'service_name': 'api',
      'port': 8443,
      'local': True,
    })

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 2
    step = data['commands'][0]
    assert step['action'] == 'create'
    assert step['options']['hostname'] == 'api.example.com'
    assert step['options']['port'] == 8443
    assert step['options']['local'] is True
    assert data['commands'][1]['resource'] == 'app'

  def test_false_bool_clears_create_flag(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'service', 'create', {
      'service_name': 'api',
      'local': True,
      'hostname': 'api.example.com',
    })

    update_scaffold_create_command(path, 'service', {
      'service_name': 'api',
      'local': False,
    })

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert 'local' not in data['commands'][0]['options']
    assert data['commands'][0]['options']['hostname'] == 'api.example.com'

  def test_rename_updates_service_name(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'service', 'create', {
      'service_name': 'api',
      'hostname': 'api.example.com',
    })

    update_scaffold_create_command(path, 'service', {
      'service_name': 'api',
      'name': 'api-v2',
      'port': 8443,
    })

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 1
    assert data['commands'][0]['options']['service_name'] == 'api-v2'
    assert data['commands'][0]['options']['port'] == 8443
    assert 'name' not in data['commands'][0]['options']

  def test_missing_create_appends_create(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')

    update_scaffold_create_command(path, 'service', {
      'service_name': 'api',
      'port': 8443,
      'name': 'api-v2',
    })

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 1
    assert data['commands'][0]['action'] == 'create'
    assert data['commands'][0]['options']['service_name'] == 'api-v2'
    assert data['commands'][0]['options']['port'] == 8443
    assert 'name' not in data['commands'][0]['options']


class TestRemoveScaffoldCreateCommand:
  def test_removes_matching_create(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'service', 'create', {
      'service_name': 'api',
      'hostname': 'api.example.com',
    })
    save_scaffold_command(path, 'app', 'create', {'app_name': 'app'})
    save_scaffold_command(path, 'service', 'create', {
      'service_name': 'web',
      'hostname': 'web.example.com',
    })

    remove_scaffold_create_command(path, 'service', {'service_name': 'api'})

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 2
    assert data['commands'][0]['resource'] == 'app'
    assert data['commands'][1]['options']['service_name'] == 'web'

  def test_missing_create_leaves_file_unchanged(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')
    save_scaffold_command(path, 'app', 'create', {'app_name': 'app'})

    remove_scaffold_create_command(path, 'service', {'service_name': 'api'})

    with open(path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 1
    assert data['commands'][0]['resource'] == 'app'

  def test_missing_file_does_not_create_empty(self, tmp_path):
    path = os.path.join(str(tmp_path), 'scaffold.yml')

    remove_scaffold_create_command(path, 'service', {'service_name': 'api'})

    assert not os.path.exists(path)
