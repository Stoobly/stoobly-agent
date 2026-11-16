import os

import yaml

from stoobly_agent.app.cli.scaffold.create_command import (
  save_scaffold_command,
  scaffold_command_identity,
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
