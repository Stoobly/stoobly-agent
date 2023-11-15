import pdb
import pytest

from typing import List

from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log, LogEvent
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import PUT_ACTION, LogEvent, REQUEST_RESOURCE
from stoobly_agent.test.test_helper import reset

class TestLog():
  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  class TestRemovingProcessedEvents():

    @pytest.fixture(scope='class')
    def events(self):
      return [
        LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '1', PUT_ACTION)),
        LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '2', PUT_ACTION)),
        LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '3', PUT_ACTION)),
        LogEvent(LogEvent.serialize(REQUEST_RESOURCE, '4', PUT_ACTION))
      ]

    @pytest.fixture(scope='class')
    def version_uuids(self, events: List[LogEvent]):
      log = Log()
      uuids = log.uuids(events)
      return log.generate_version(uuids)

    @pytest.fixture(scope='class')
    def branch_event(self):
      return LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'a', PUT_ACTION))

    class TestBranchPointAtStart():
      @pytest.fixture(scope='class')
      def log_events(self, events: List[LogEvent], branch_event: LogEvent):
        return [branch_event] + events

      def test_it_returns_event_at_start(self, log_events: List[LogEvent], version_uuids: List[str], branch_event: LogEvent):
        log = Log()
        unprocessed_events = log.remove_processed_events(log_events, version_uuids)
        assert log.uuids(unprocessed_events) == [branch_event.uuid]

    class TestBranchPointAtEnd():
      @pytest.fixture(scope='class')
      def log_events(self, events: List[LogEvent], branch_event: LogEvent):
        return events + [branch_event] 

      def test_it_returns_event_at_start(self, log_events: List[LogEvent], version_uuids: List[str], branch_event: LogEvent):
        log = Log()
        unprocessed_events = log.remove_processed_events(log_events, version_uuids)
        assert log.uuids(unprocessed_events) == [branch_event.uuid] 

    class TestBranchPointInMiddle():
      @pytest.fixture(scope='class')
      def log_events(self, events: List[LogEvent], branch_event: LogEvent):
        midpoint = int(len(events) / 2)
        return events[0:midpoint] + [branch_event] + events[midpoint:]

      def test_it_returns_event_in_middle(self, log_events: List[LogEvent], version_uuids: List[str], branch_event: LogEvent):
        log = Log()
        unprocessed_events = log.remove_processed_events(log_events, version_uuids)
        assert log.uuids(unprocessed_events) == [branch_event.uuid]

    class TestMultipleBranchEvents():
      @pytest.fixture(scope='class')
      def branch_events(self):
        return [
          LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'a', PUT_ACTION)),
          LogEvent(LogEvent.serialize(REQUEST_RESOURCE, 'b', PUT_ACTION))
        ]

      @pytest.fixture(scope='class')
      def log_events(self, events: List[LogEvent], branch_events: LogEvent):
        midpoint = int(len(events) / 2)
        return events[0:midpoint] + branch_events + events[midpoint:]

      def test_it_returns_branch_events(self, log_events: List[LogEvent], version_uuids: List[str], branch_events: LogEvent):
        log = Log()
        unprocessed_events = log.remove_processed_events(log_events, version_uuids)
        assert log.uuids(unprocessed_events) == log.uuids(branch_events)