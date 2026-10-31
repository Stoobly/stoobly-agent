import json
import re

import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import filter_action
from stoobly_agent.app.settings.filter_rule import FilterRule
from stoobly_agent.app.settings.rewrite_rule import RewriteRule
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import reset


@pytest.fixture(scope='module')
def runner():
  return CliRunner()


@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()


def _minimal_har(url='https://example.com/api/pets', method='GET', status=200):
  return {
    'log': {
      'entries': [
        {
          '_resourceType': 'xhr',
          'request': {
            'method': method,
            'url': url,
            'headers': [{'name': 'Accept', 'value': 'application/json'}],
            'httpVersion': 'HTTP/1.1',
          },
          'response': {
            'status': status,
            'headers': [{'name': 'Content-Type', 'value': 'application/json'}],
            'content': {'text': '{"ok":true}', 'size': 10},
          },
          'time': 12,
        }
      ]
    }
  }


class TestScenarioImportHarCreate:

  def test_it_creates_scenario_and_request(self, runner: CliRunner, tmp_path):
    har_path = tmp_path / 'pets.har'
    har_path.write_text(json.dumps(_minimal_har()))

    result = runner.invoke(
      scenario,
      ['import', '--format', 'har', '--without-headers', '--select', 'name,requests_count', str(har_path)],
    )
    assert result.exit_code == 0, result.output

    created = Scenario.last()
    assert created is not None
    assert re.match(r'^pets-\d+$', created.name)
    assert created.requests.count() == 1

    req = Request.last()
    assert req.method == 'GET'
    assert req.host == 'example.com'
    assert req.path == '/api/pets'
    assert req.status == 200


class TestScenarioImportGorAppendAndOverwrite:

  @pytest.fixture(scope='class')
  def seed_request(self, runner: CliRunner):
    result = runner.invoke(request, ['create', 'https://example.com/seed'])
    assert result.exit_code == 0
    return Request.last()

  @pytest.fixture(scope='class')
  def gor_path(self, tmp_path_factory, seed_request):
    path = tmp_path_factory.mktemp('gor') / 'import.gor'
    path.write_bytes(JoinedRequestStringAdapter(seed_request).adapt())
    return path

  def test_it_appends_with_scenario_key(self, runner: CliRunner, gor_path):
    create_result = runner.invoke(scenario, ['create', '--without-headers', '--select', 'key', 'import-append'])
    assert create_result.exit_code == 0
    scenario_key = create_result.output.strip()

    # Seed one request into the scenario first
    seed = runner.invoke(request, ['create', 'https://example.com/existing', '--scenario-key', scenario_key])
    assert seed.exit_code == 0
    before = Scenario.find_by(uuid=ScenarioKey(scenario_key).id).requests.count()
    assert before == 1

    result = runner.invoke(
      scenario,
      ['import', '--format', 'gor', '--scenario-key', scenario_key, str(gor_path)],
    )
    assert result.exit_code == 0, result.output

    after = Scenario.find_by(uuid=ScenarioKey(scenario_key).id).requests.count()
    assert after == before + 1

  def test_it_overwrites_with_scenario_key(self, runner: CliRunner, gor_path):
    create_result = runner.invoke(scenario, ['create', '--without-headers', '--select', 'key', 'import-overwrite'])
    assert create_result.exit_code == 0
    scenario_key = create_result.output.strip()

    seed = runner.invoke(request, ['create', 'https://example.com/old-1', '--scenario-key', scenario_key])
    assert seed.exit_code == 0
    seed = runner.invoke(request, ['create', 'https://example.com/old-2', '--scenario-key', scenario_key])
    assert seed.exit_code == 0
    assert Scenario.find_by(uuid=ScenarioKey(scenario_key).id).requests.count() == 2

    result = runner.invoke(
      scenario,
      ['import', '--format', 'gor', '--scenario-key', scenario_key, '--overwrite', str(gor_path)],
    )
    assert result.exit_code == 0, result.output

    scenario_record = Scenario.find_by(uuid=ScenarioKey(scenario_key).id)
    assert scenario_record.requests.count() == 1
    assert scenario_record.requests.first().path == '/seed'


class TestScenarioImportInvalidHar:

  def test_it_rejects_invalid_json(self, runner: CliRunner, tmp_path):
    path = tmp_path / 'bad.har'
    path.write_text('not-json')

    result = runner.invoke(scenario, ['import', '--format', 'har', str(path)])
    assert result.exit_code != 0


class TestSharedCreateFirewallAndRewrite:

  def test_firewall_blocks_request_create(self, runner: CliRunner):
    settings = Settings.instance()
    settings.proxy.filter.set_filter_rules(str(LOCAL_PROJECT_ID), [
      FilterRule({
        'action': filter_action.EXCLUDE,
        'methods': ['GET'],
        'modes': [mode.RECORD],
        'pattern': 'https://blocked.example.com.*',
      })
    ])
    settings.commit()

    try:
      result = runner.invoke(request, ['create', 'https://blocked.example.com/secret'])
      assert result.exit_code != 0
      assert Request.where('host', 'blocked.example.com').count() == 0
    finally:
      settings.proxy.filter.set_filter_rules(str(LOCAL_PROJECT_ID), [])
      settings.commit()

  def test_rewrite_applies_on_request_create(self, runner: CliRunner):
    settings = Settings.instance()
    settings.proxy.rewrite.set_rewrite_rules(str(LOCAL_PROJECT_ID), [
      RewriteRule({
        'methods': ['GET'],
        'pattern': 'https://rewrite.example.com.*',
        'url_rules': [{'modes': [mode.RECORD], 'hostname': 'rewritten.example.com'}],
        'parameter_rules': [],
      })
    ])
    settings.commit()

    try:
      result = runner.invoke(request, ['create', 'https://rewrite.example.com/api'])
      assert result.exit_code == 0, result.output
      created = Request.last()
      assert created.host == 'rewritten.example.com'
    finally:
      settings.proxy.rewrite.set_rewrite_rules(str(LOCAL_PROJECT_ID), [])
      settings.commit()

  def test_har_import_skips_firewall_blocked_entries(self, runner: CliRunner, tmp_path):
    settings = Settings.instance()
    settings.proxy.filter.set_filter_rules(str(LOCAL_PROJECT_ID), [
      FilterRule({
        'action': filter_action.EXCLUDE,
        'methods': ['GET'],
        'modes': [mode.RECORD],
        'pattern': 'https://blocked.example.com.*',
      })
    ])
    settings.commit()

    har = _minimal_har()
    har['log']['entries'].append(_minimal_har('https://blocked.example.com/x')['log']['entries'][0])
    path = tmp_path / 'mixed.har'
    path.write_text(json.dumps(har))

    try:
      before = Request.count()
      result = runner.invoke(scenario, ['import', '--format', 'har', str(path)])
      assert result.exit_code == 0, result.output
      assert Request.count() == before + 1
      assert Request.where('host', 'blocked.example.com').count() == 0
    finally:
      settings.proxy.filter.set_filter_rules(str(LOCAL_PROJECT_ID), [])
      settings.commit()
