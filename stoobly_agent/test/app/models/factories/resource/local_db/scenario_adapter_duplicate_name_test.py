import pytest

from stoobly_agent.app.models.factories.resource.local_db.scenario_adapter import LocalDBScenarioAdapter
from stoobly_agent.test.test_helper import reset

@pytest.fixture(autouse=True)
def _reset_db():
  # Isolate each test with a fresh sqlite database + migrations.
  reset()

def test_duplicate_scenario_name_returns_conflict():
  adapter = LocalDBScenarioAdapter()

  first_res, first_status = adapter.create(name='Duplicate Scenario', description='d1')
  assert first_status == 200

  second_res, second_status = adapter.create(name='Duplicate Scenario', description='d2')
  assert second_status == 409
  assert 'already exists' in str(second_res).lower()

def test_scenario_name_exceeding_max_length_returns_bad_request():
  adapter = LocalDBScenarioAdapter()
  name = 'a' * (LocalDBScenarioAdapter.NAME_MAX_LENGTH + 1)

  res, status = adapter.create(name=name, description='too long')
  assert status == 400
  assert 'at most' in str(res).lower()
  assert str(LocalDBScenarioAdapter.NAME_MAX_LENGTH) in str(res)

def test_scenario_name_at_max_length_is_accepted():
  adapter = LocalDBScenarioAdapter()
  name = 'a' * LocalDBScenarioAdapter.NAME_MAX_LENGTH

  res, status = adapter.create(name=name, description='max length')
  assert status == 200
  assert res['name'] == name

@pytest.mark.parametrize('name', [
  '',
  '   ',
  'a/b',
  'a\\b',
  '-leading',
  'trailing-',
  '._punct_.',
])
def test_problematic_scenario_name_returns_bad_request(name):
  adapter = LocalDBScenarioAdapter()

  res, status = adapter.create(name=name, description='invalid')
  assert status == 400
  assert 'filesystem-safe' in str(res).lower() or 'required' in str(res).lower()

def test_space_and_hyphen_scenario_names_are_accepted():
  adapter = LocalDBScenarioAdapter()

  first_res, first_status = adapter.create(name='My Scenario', description='space')
  second_res, second_status = adapter.create(name='My-Scenario', description='hyphen')

  assert first_status == 200
  assert second_status == 200
  assert first_res['name'] == 'My Scenario'
  assert second_res['name'] == 'My-Scenario'

def test_update_rejects_problematic_scenario_name():
  adapter = LocalDBScenarioAdapter()

  created, status = adapter.create(name='valid-name', description='')
  assert status == 200

  res, update_status = adapter.update(created['uuid'], name='a/b')
  assert update_status == 400
  assert 'filesystem-safe' in str(res).lower()
