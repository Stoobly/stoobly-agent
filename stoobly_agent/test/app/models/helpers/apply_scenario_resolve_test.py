import pytest

from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True)
def _reset_db():
  reset()


def test_resolve_scenario_uuid_by_name_after_yaml_gone():
  scenario = Scenario.create(name='checkout-flow', description='')

  uuid = Apply()._Apply__resolve_scenario_uuid('checkout-flow')
  assert uuid == scenario.uuid


def test_resolve_scenario_uuid_prefers_exact_name():
  target = Scenario.create(name='My Scenario', description='')
  Scenario.create(name='My-Scenario', description='')

  uuid = Apply()._Apply__resolve_scenario_uuid('My Scenario')
  assert uuid == target.uuid
