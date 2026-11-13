from stoobly_agent.app.proxy import intercept_handler


class FakeScenarioModel:
  instances = 0

  def __init__(self, settings):
    FakeScenarioModel.instances += 1


def test_scenario_model_is_created_once_on_first_use(monkeypatch):
  FakeScenarioModel.instances = 0
  monkeypatch.setattr(intercept_handler, 'ScenarioModel', FakeScenarioModel)
  monkeypatch.setattr(intercept_handler, 'scenario_model', None)

  assert FakeScenarioModel.instances == 0

  first = intercept_handler.__get_scenario_model()
  second = intercept_handler.__get_scenario_model()

  assert isinstance(first, FakeScenarioModel)
  assert first is second
  assert FakeScenarioModel.instances == 1
