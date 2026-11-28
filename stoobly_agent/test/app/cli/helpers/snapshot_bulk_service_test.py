from stoobly_agent.app.cli.helpers.snapshot_bulk_service import scenario_snapshot_has_diff


class _FakeRequest:
  def __init__(self, uuid, response=True):
    self.uuid = uuid
    self.response = object() if response else None


class _FakeRequestSnapshot:
  def __init__(self, uuid, current=None):
    self.uuid = uuid
    self._current = current

  def find_resource(self):
    return self._current


class _FakeScenario:
  def __init__(self, name='s', description='d', requests=None):
    self.name = name
    self.description = description
    self.requests = requests or []


class _FakeScenarioSnapshot:
  def __init__(self, metadata, scenario, request_snapshots=None):
    self.exists = True
    self.metadata = metadata
    self.uuid = 'scenario-uuid'
    self._scenario = scenario
    self._request_snapshots = request_snapshots or []

  def find_resource(self):
    return self._scenario

  def iter_request_snapshots(self, handler):
    for request_snapshot in self._request_snapshots:
      handler(request_snapshot)


def test_membership_shrink_is_a_diff():
  snap_req = _FakeRequestSnapshot('req-a', current=_FakeRequest('req-a'))
  scenario = _FakeScenario(requests=[])  # removed from scenario
  snapshot = _FakeScenarioSnapshot(
    {'name': 's', 'description': 'd'},
    scenario,
    request_snapshots=[snap_req],
  )

  assert scenario_snapshot_has_diff(snapshot) is True


def test_membership_grow_is_a_diff():
  scenario = _FakeScenario(requests=[_FakeRequest('req-b')])
  snapshot = _FakeScenarioSnapshot(
    {'name': 's', 'description': 'd'},
    scenario,
    request_snapshots=[],
  )

  assert scenario_snapshot_has_diff(snapshot) is True


def test_matching_membership_without_content_diff_is_not_a_diff(monkeypatch):
  current = _FakeRequest('req-a')
  snap_req = _FakeRequestSnapshot('req-a', current=current)
  scenario = _FakeScenario(requests=[current])
  snapshot = _FakeScenarioSnapshot(
    {'name': 's', 'description': 'd'},
    scenario,
    request_snapshots=[snap_req],
  )

  monkeypatch.setattr(
    'stoobly_agent.app.cli.helpers.snapshot_bulk_service.analyze_request_diff',
    lambda *_args, **_kwargs: None,
  )

  assert scenario_snapshot_has_diff(snapshot) is False


def test_missing_current_response_is_a_diff():
  current = _FakeRequest('req-a', response=False)
  snap_req = _FakeRequestSnapshot('req-a', current=current)
  scenario = _FakeScenario(requests=[current])
  snapshot = _FakeScenarioSnapshot(
    {'name': 's', 'description': 'd'},
    scenario,
    request_snapshots=[snap_req],
  )

  assert scenario_snapshot_has_diff(snapshot) is True
