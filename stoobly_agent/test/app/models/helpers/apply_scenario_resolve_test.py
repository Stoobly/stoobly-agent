import pytest

from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True)
def _reset_db():
  reset()


def test_resolve_scenario_uuid_bare_uuid():
  scenario = Scenario.create(name='checkout-flow', description='')

  uuid = Apply()._Apply__resolve_scenario_uuid(scenario.uuid)
  assert uuid == scenario.uuid


def test_resolve_scenario_uuid_from_name_uuid_locator():
  scenario = Scenario.create(name='My Scenario', description='')

  uuid = Apply()._Apply__resolve_scenario_uuid(f'My Scenario/{scenario.uuid}')
  assert uuid == scenario.uuid


def test_resolve_scenario_uuid_rejects_name_only():
  Scenario.create(name='checkout-flow', description='')

  assert Apply()._Apply__resolve_scenario_uuid('checkout-flow') is None
