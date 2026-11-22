import os

import pdb
import pytest

from typing import List

from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import (
  DELETE_ACTION,
  LogEvent,
  PUT_ACTION,
  REQUEST_RESOURCE,
  SCENARIO_RESOURCE,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshotV2
from stoobly_agent.test.test_helper import reset

class TestLog():
  @pytest.fixture(scope='class', autouse=True)
  @classmethod
  def settings(cls):
    return reset()

  class TestRemovingProcessedEvents():

    @pytest.fixture(scope='class')
    @classmethod
    def events(cls):
      return [
        LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '1', PUT_ACTION)),
        LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '2', PUT_ACTION)),
        LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '3', PUT_ACTION)),
        LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '4', PUT_ACTION))
      ]

    @pytest.fixture(scope='class')
    @classmethod
    def version_uuids(cls, events: List[LogEvent]):
      log = Log()
      uuids = log.uuids(events)
      return log.generate_version(uuids)

    @pytest.fixture(scope='class')
    @classmethod
    def branch_event(cls):
      return LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'a', PUT_ACTION))

    class TestBranchPointAtStart():
      @pytest.fixture(scope='class')
      @classmethod
      def log_events(cls, events: List[LogEvent], branch_event: LogEvent):
        return [branch_event] + events

      def test_it_returns_event_at_start(self, log_events: List[LogEvent], version_uuids: List[str], branch_event: LogEvent):
        log = Log()
        unprocessed_events = log.remove_processed_events(log_events, version_uuids)
        assert log.uuids(unprocessed_events) == [branch_event.uuid]

    class TestBranchPointAtEnd():
      @pytest.fixture(scope='class')
      @classmethod
      def log_events(cls, events: List[LogEvent], branch_event: LogEvent):
        return events + [branch_event] 

      def test_it_returns_event_at_start(self, log_events: List[LogEvent], version_uuids: List[str], branch_event: LogEvent):
        log = Log()
        unprocessed_events = log.remove_processed_events(log_events, version_uuids)
        assert log.uuids(unprocessed_events) == [branch_event.uuid] 

    class TestBranchPointInMiddle():
      @pytest.fixture(scope='class')
      @classmethod
      def log_events(cls, events: List[LogEvent], branch_event: LogEvent):
        midpoint = int(len(events) / 2)
        return events[0:midpoint] + [branch_event] + events[midpoint:]

      def test_it_returns_event_in_middle(self, log_events: List[LogEvent], version_uuids: List[str], branch_event: LogEvent):
        log = Log()
        unprocessed_events = log.remove_processed_events(log_events, version_uuids)
        assert log.uuids(unprocessed_events) == [branch_event.uuid]

    class TestMultipleBranchEvents():
      @pytest.fixture(scope='class')
      @classmethod
      def branch_events(cls):
        return [
          LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'a', PUT_ACTION)),
          LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'b', PUT_ACTION))
        ]

      @pytest.fixture(scope='class')
      @classmethod
      def log_events(cls, events: List[LogEvent], branch_events: LogEvent):
        midpoint = int(len(events) / 2)
        return events[0:midpoint] + branch_events + events[midpoint:]

      def test_it_returns_branch_events(self, log_events: List[LogEvent], version_uuids: List[str], branch_events: LogEvent):
        log = Log()
        unprocessed_events = log.remove_processed_events(log_events, version_uuids)
        assert log.uuids(unprocessed_events) == log.uuids(branch_events)

  class TestCollapse:
    def test_keeps_latest_action_per_resource(self):
      put = LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'req-1', PUT_ACTION))
      delete = LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'req-1', DELETE_ACTION))
      other = LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'req-2', PUT_ACTION))

      collapsed = Log().collapse([put, other, delete])
      assert Log().uuids(collapsed) == [other.uuid, delete.uuid]
      assert collapsed[-1].action == DELETE_ACTION

  class TestRemoveDanglingEvents:
    def test_drops_request_delete_without_prior_put_or_scenario_ref(self, monkeypatch):
      log = Log()
      delete = LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'req-1', DELETE_ACTION))
      monkeypatch.setattr(log, 'build_scenario_inverted_index', lambda events, index=None, include_deletes=False: {})

      kept = log.remove_dangling_events([], [delete])
      assert kept == []

    def test_keeps_request_delete_when_prior_put_exists(self, monkeypatch):
      log = Log()
      put = LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'req-1', PUT_ACTION))
      delete = LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'req-1', DELETE_ACTION))
      monkeypatch.setattr(log, 'build_scenario_inverted_index', lambda events, index=None, include_deletes=False: {})

      kept = log.remove_dangling_events([put], [delete])
      assert Log().uuids(kept) == [delete.uuid]

    def test_keeps_request_delete_when_scenario_references(self, monkeypatch):
      log = Log()
      delete = LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'req-1', DELETE_ACTION))
      monkeypatch.setattr(
        log,
        'build_scenario_inverted_index',
        lambda events, index=None, include_deletes=False: {'req-1': ['scenario-a']},
      )

      kept = log.remove_dangling_events([], [delete])
      assert Log().uuids(kept) == [delete.uuid]

    def test_keeps_scenario_delete_only_after_put(self, monkeypatch):
      log = Log()
      put = LogEvent(LogEvent.serialize(SCENARIO_RESOURCE, 'flow', PUT_ACTION))
      delete = LogEvent(LogEvent.serialize(SCENARIO_RESOURCE, 'flow', DELETE_ACTION))
      orphan_delete = LogEvent(LogEvent.serialize(SCENARIO_RESOURCE, 'other', DELETE_ACTION))
      monkeypatch.setattr(log, 'build_scenario_inverted_index', lambda events, index=None, include_deletes=False: index or {})

      kept = log.remove_dangling_events([put], [delete, orphan_delete])
      assert Log().uuids(kept) == [delete.uuid]

  class TestMarkProcessedAndNextVersion:
    @pytest.fixture(autouse=True)
    def settings(self):
      return reset()

    def test_mark_processed_appends_uuid(self):
      log = Log()
      first = LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '1', PUT_ACTION))
      second = LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '2', PUT_ACTION))
      log.append(str(first))
      log.append(str(second))

      log.mark_processed(first.uuid)
      assert first.uuid in log.version
      assert second.uuid not in log.version

      log.mark_processed(first.uuid)  # idempotent
      assert log.version.count(first.uuid) == 1

    def test_next_version_through_last_success(self):
      log = Log()
      events = [
        LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '1', PUT_ACTION)),
        LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '2', PUT_ACTION)),
        LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '3', PUT_ACTION)),
      ]
      for event in events:
        log.append(str(event))

      version = log.next_version(events[1].uuid)
      assert version.split('\n') == [events[0].uuid, events[1].uuid]

    def test_next_version_unknown_uuid_returns_all(self):
      log = Log()
      event = LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '1', PUT_ACTION))
      log.append(str(event))
      assert log.next_version('missing-uuid') == log.generate_version([event.uuid])

  class TestBuildRawEvents:
    def test_empty_contents(self):
      assert Log().build_raw_events('') == []
      assert Log().build_raw_events(None or '') == []

    def test_filters_blank_lines(self):
      raw = Log().build_raw_events('a\n\nb\n')
      assert raw == ['a', 'b']

  class TestRemoveRequestSnapshot:
    @pytest.fixture(autouse=True)
    def settings(self):
      return reset()

    def _seed_snapshot(self, uuid: str):
      snapshot = RequestSnapshotV2(uuid, slug='GET-api')
      path = snapshot.path
      snapshot._ensure_parent(path)
      with open(path, 'wb') as fp:
        fp.write(b'payload')
      return snapshot, path

    def test_removes_when_unreferenced(self):
      snapshot, path = self._seed_snapshot('cccccccc-cccc-cccc-cccc-cccccccccccc')
      assert os.path.isfile(path)

      Log().remove_request_snapshot(snapshot, scenario_inverted_index={})
      assert not os.path.exists(path)

    def test_keeps_when_referenced(self):
      uuid = 'dddddddd-dddd-dddd-dddd-dddddddddddd'
      snapshot, path = self._seed_snapshot(uuid)

      Log().remove_request_snapshot(
        snapshot,
        scenario_inverted_index={uuid: ['scenario-a']},
      )
      assert os.path.isfile(path)

    def test_ignore_scenario_ids_allows_exclusive_remove(self):
      uuid = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee'
      snapshot, path = self._seed_snapshot(uuid)

      Log().remove_request_snapshot(
        snapshot,
        scenario_inverted_index={uuid: ['scenario-a']},
        ignore_scenario_ids=['scenario-a'],
      )
      assert not os.path.exists(path)