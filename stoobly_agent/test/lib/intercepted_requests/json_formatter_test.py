import json
import logging
from unittest.mock import MagicMock, patch

from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_NAMESPACE_ENV
from stoobly_agent.lib.intercepted_requests.json_formatter import JSONFormatter


def _workflow_record(msg, source_level='INFO'):
    record = logging.LogRecord(
        name='test', level=logging.INFO, pathname=__file__, lineno=1,
        msg=msg, args=(), exc_info=None,
    )
    record.source = 'workflow'
    record.source_level = source_level
    return record


class TestJSONFormatterWorkflowSource:
    def _format(self, record):
        formatter = JSONFormatter(MagicMock())
        # Patch InterceptSettings so a stray fall-through (red run) fails on the
        # assertion rather than crashing inside scenario lookup.
        with patch('stoobly_agent.lib.intercepted_requests.json_formatter.InterceptSettings') as m:
            m.return_value.scenario_key = None
            return json.loads(formatter.format(record))

    def test_emits_source_message_and_level(self):
        entry = self._format(_workflow_record('[ERROR] disk full', source_level='ERROR'))
        assert entry.get('source') == 'workflow'
        assert entry.get('message') == '[ERROR] disk full'
        assert entry.get('level') == 'ERROR'
        assert 'timestamp' in entry

    def test_skips_request_and_scenario_fields(self):
        entry = self._format(_workflow_record('plain line'))
        for absent in ('scenario_key', 'scenario_name', 'url', 'method', 'status_code'):
            assert absent not in entry

    def test_includes_namespace_from_env(self, monkeypatch):
        monkeypatch.setenv(WORKFLOW_NAMESPACE_ENV, 'mock')
        entry = self._format(_workflow_record('line'))
        assert entry.get('namespace') == 'mock'
