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
