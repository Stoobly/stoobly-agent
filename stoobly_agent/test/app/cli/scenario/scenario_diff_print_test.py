import io
import sys

from stoobly_agent.app.cli.handlers.scenario_cli_handler import _print_scenario_diff


class _FakeScenario:
    def __init__(self, name, description, scenario_key):
        self.name = name
        self.description = description
        self._key = scenario_key
        self.requests = []

    def key(self):
        return self._key


class _FakeRequestSnapshot:
    def __init__(self, uuid, url=""):
        self.uuid = uuid
        self._url = url

    def find_resource(self):
        return None

    @property
    def python_request(self):
        if not self._url:
            return None

        class _PyReq:
            def __init__(self, url):
                self.url = url

        return _PyReq(self._url)


class _FakeSnapshot:
    def __init__(self, metadata, scenario, request_snapshots=None):
        self.metadata = metadata
        self.metadata_path = "/tmp/scenario_snapshot_metadata"
        self.uuid = "15489e9e-9f87-4953-b3b7-352e867979ac"
        self._scenario = scenario
        self._request_snapshots = request_snapshots or []

    def find_resource(self):
        return self._scenario

    def iter_request_snapshots(self, handler):
        for request_snapshot in self._request_snapshots:
            handler(request_snapshot)


def test_scenario_header_plain_name_when_only_description_differs():
    current = _FakeScenario(
        "Test2", "current-desc", "p0.i15489e9e9f874953b3b7352e867979ac"
    )
    snap = _FakeSnapshot({"name": "Test2", "description": "snapshot-desc"}, current)

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        # Description diff is emitted only when full=True (see _print_scenario_diff).
        _print_scenario_diff(snap, full=True, strict=True)
    finally:
        sys.stdout = old

    out = buf.getvalue()
    first_line = out.split("\n", 1)[0]
    assert first_line == "=== Scenario Test2 p0.i15489e9e9f874953b3b7352e867979ac"
    assert "~ Description" in out
    assert "=== Scenario metadata" not in out
    assert "/tmp/scenario_snapshot_metadata" not in out
    assert '"description"' not in out


def test_name_diff_is_on_first_line_no_description_section():
    current = _FakeScenario("Test2", "d", "p0.i15489e9e9f874953b3b7352e867979ac")
    snap = _FakeSnapshot({"name": "OldName", "description": "d"}, current)

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        _print_scenario_diff(snap, full=False, strict=True)
    finally:
        sys.stdout = old

    out = buf.getvalue()
    assert "~ Description" not in out
    assert "OldName" in out
    assert "Test2" in out
    first_line = out.split("\n", 1)[0]
    assert first_line.startswith("=== Scenario ")
    assert first_line.endswith(" p0.i15489e9e9f874953b3b7352e867979ac")


def test_name_and_description_diff_shows_description_section_only():
    current = _FakeScenario("NewN", "d2", "p0.i15489e9e9f874953b3b7352e867979ac")
    snap = _FakeSnapshot({"name": "OldN", "description": "d1"}, current)

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        _print_scenario_diff(snap, full=True, strict=True)
    finally:
        sys.stdout = old

    out = buf.getvalue()
    assert "~ Description" in out
    assert "=== Scenario metadata" not in out
    assert "/tmp/scenario_snapshot_metadata" not in out


def test_request_removed_from_scenario_is_shown():
    current = _FakeScenario(
        "Test2", "d", "p0.i15489e9e9f874953b3b7352e867979ac"
    )
    snap = _FakeSnapshot(
        {"name": "Test2", "description": "d"},
        current,
        request_snapshots=[
            _FakeRequestSnapshot(
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                url="https://example.com/gone",
            )
        ],
    )

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        _print_scenario_diff(snap, full=False, strict=True)
    finally:
        sys.stdout = old

    out = buf.getvalue()
    assert "=== Scenario Test2 p0.i15489e9e9f874953b3b7352e867979ac" in out
    assert "https://example.com/gone" in out
    assert "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee" in out
    assert "Request not found" in out
