import pytest

from stoobly_agent.app.models.factories.resource.local_db.helpers import snapshot_scenarios_since_service


class FakeScenarioModel:
  def __init__(self, responses, snapshot_results):
    self._responses = responses
    self._snapshot_results = snapshot_results
    self.as_local_called = False
    self.index_calls = []
    self.snapshot_calls = []

  def as_local(self):
    self.as_local_called = True

  def index(self, **kwargs):
    self.index_calls.append(kwargs)
    page = kwargs.get('page', 0)
    return self._responses[page]

  def snapshot(self, scenario_id, **kwargs):
    self.snapshot_calls.append((scenario_id, kwargs))
    return self._snapshot_results.get(scenario_id, (None, 500))


def test_snapshot_scenarios_since_collects_snapshots_with_pagination(monkeypatch):
  fake_model = FakeScenarioModel(
    responses=[
      ({
        'list': [
          {'uuid': 'scenario-a'},
          {'id': 'scenario-b'},
          {'name': 'missing-id'},
        ],
        'total': 101
      }, 200),
      ({
        'list': [{'uuid': 'scenario-c'}],
        'total': 101
      }, 200)
    ],
    snapshot_results={
      'scenario-a': ('/tmp/a.yml', 200),
      'scenario-b': ('', 200),  # Empty path should not be included.
      'scenario-c': ('/tmp/c.yml', 200),
    }
  )

  monkeypatch.setattr(snapshot_scenarios_since_service.Settings, 'instance', staticmethod(lambda: object()))
  monkeypatch.setattr(snapshot_scenarios_since_service, 'ScenarioModel', lambda _settings: fake_model)

  snapshots = snapshot_scenarios_since_service.snapshot_scenarios_since('2026-01-01T00:00:00Z')

  assert fake_model.as_local_called is True
  assert fake_model.index_calls == [
    {'page': 0, 'size': 100, 'updated_since': '2026-01-01 00:00:00'},
    {'page': 1, 'size': 100, 'updated_since': '2026-01-01 00:00:00'},
  ]
  assert fake_model.snapshot_calls == [
    ('scenario-a', {'action': snapshot_scenarios_since_service.PUT_ACTION}),
    ('scenario-b', {'action': snapshot_scenarios_since_service.PUT_ACTION}),
    ('scenario-c', {'action': snapshot_scenarios_since_service.PUT_ACTION}),
  ]
  assert snapshots == [
    ({'uuid': 'scenario-a'}, '/tmp/a.yml'),
    ({'uuid': 'scenario-c'}, '/tmp/c.yml'),
  ]


def test_snapshot_scenarios_since_stops_when_index_non_200(monkeypatch):
  fake_model = FakeScenarioModel(
    responses=[({'list': [{'uuid': 'scenario-a'}], 'total': 1}, 500)],
    snapshot_results={'scenario-a': ('/tmp/a.yml', 200)}
  )

  monkeypatch.setattr(snapshot_scenarios_since_service.Settings, 'instance', staticmethod(lambda: object()))
  monkeypatch.setattr(snapshot_scenarios_since_service, 'ScenarioModel', lambda _settings: fake_model)

  snapshots = snapshot_scenarios_since_service.snapshot_scenarios_since('2026-01-01T00:00:00Z')

  assert snapshots == []
  assert fake_model.snapshot_calls == []


def test_snapshot_scenarios_since_passes_custom_snapshot_options(monkeypatch):
  fake_model = FakeScenarioModel(
    responses=[({'list': [{'uuid': 'scenario-a'}], 'total': 1}, 200)],
    snapshot_results={'scenario-a': ('/tmp/a.yml', 200)}
  )

  monkeypatch.setattr(snapshot_scenarios_since_service.Settings, 'instance', staticmethod(lambda: object()))
  monkeypatch.setattr(snapshot_scenarios_since_service, 'ScenarioModel', lambda _settings: fake_model)

  snapshot_scenarios_since_service.snapshot_scenarios_since(
    '2026-01-01T00:00:00Z',
    action='CUSTOM_ACTION',
    persist=True
  )

  assert fake_model.snapshot_calls == [
    ('scenario-a', {'action': 'CUSTOM_ACTION', 'persist': True})
  ]


def test_normalize_iso_datetime_transforms_utc_z():
  normalized = snapshot_scenarios_since_service.__normalize_iso_datetime('2026-03-01T05:06:07Z')
  assert normalized == '2026-03-01 05:06:07'


def test_normalize_iso_datetime_converts_to_utc():
  normalized = snapshot_scenarios_since_service.__normalize_iso_datetime('2026-03-01T05:06:07+02:00')
  assert normalized == '2026-03-01 03:06:07'


def test_normalize_iso_datetime_rejects_empty_value():
  with pytest.raises(ValueError, match='updated_since is required'):
    snapshot_scenarios_since_service.__normalize_iso_datetime('')
