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


class _FakeSnapshot:
    def __init__(self, metadata, scenario):
        self.metadata = metadata
        self.metadata_path = "/tmp/scenario_snapshot_metadata"
        self.uuid = "15489e9e-9f87-4953-b3b7-352e867979ac"
        self._scenario = scenario

    def find_resource(self):
        return self._scenario

    def iter_request_snapshots(self, _handler):
        pass


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
