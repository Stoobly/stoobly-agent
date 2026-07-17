import pdb
import pytest
import time

from typing import List

from stoobly_agent.app.models.factories.resource.local_db.helpers.tiebreak_scenario_request import (
  SUFFIX, access_request, generate_session_id, reset_sessions, tiebreak_scenario_request
)
from stoobly_agent.lib.cache import Cache
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.test.test_helper import reset

def build_raw_request(path_with_query: str, headers: dict = None) -> bytes:
  lines = [f'GET https://example.com{path_with_query} HTTP/1.1']
  for name, value in (headers or {}).items():
    lines.append(f'{name}: {value}')
  lines.append('')
  lines.append('')
  return '\r\n'.join(lines).encode()

class RequestMock():

  def __init__(self, id, raw: bytes = None, http_version = 1.1, sequence_id = None):
    self.__id = id
    self.raw = raw
    self.http_version = http_version
    self.sequence_id = sequence_id

  @property
  def id(self):
    return self.__id

@pytest.fixture(autouse=True, scope='class')
def settings():
  return reset()

class TestTiebreakScenarioRequest():
  @pytest.fixture(scope='class')
  def created_request_one(self):
    return RequestMock(1)

  @pytest.fixture(scope='class')
  def created_request_two(self):
    return RequestMock(2)

  @pytest.fixture(scope='class')
  def created_request_three(self):
    return RequestMock(3)

  @pytest.fixture(scope='class')
  def session_id(self):
    return generate_session_id({
      'scenario_id': 'test'
    })

  @pytest.fixture(scope='class')
  def requests(self, created_request_one: Request, created_request_two: Request):
    return [created_request_one, created_request_two]

  def test_it_returns_request_one(self, session_id: str, requests: List[Request]):
    request = tiebreak_scenario_request(session_id, requests)
    assert request.id == 1

  def test_it_returns_request_two(self, session_id: str, requests: List[Request]):
    access_request(session_id, requests[0].id)
    request = tiebreak_scenario_request(session_id, requests)
    assert request.id == 2

  def test_it_returns_request_two_again(self, session_id: str, requests: List[Request]):
    request = tiebreak_scenario_request(session_id, requests)
    assert request.id == 2

  def test_it_returns_request_three(self, session_id: str, requests: List[Request]):
    access_request(session_id, requests[0].id)
    request = tiebreak_scenario_request(session_id, requests)
    assert request.id == 2

  def test_it_returns_request_one_again(self, session_id: str, requests: List[Request]):
    access_request(session_id, requests[1].id)
    request = tiebreak_scenario_request(session_id, requests)
    assert request.id == 1

  class TestWhenTimeout():
    @pytest.fixture(autouse=True, scope='class')
    def cache(self):
      cache = Cache.instance()
      return cache

    def test_it_returns_request_one(self, session_id: str, requests: List[Request]):
      access_request(session_id, requests[0].id, 100)

      time.sleep(1)

      request = tiebreak_scenario_request(session_id, requests)
      assert request.id == 1

    def test_it_returns_request_two(self, session_id: str, requests: List[Request]):
      access_request(session_id, requests[0].id, 100)

      time.sleep(0.05)

      request = tiebreak_scenario_request(session_id, requests)
      assert request.id == 2

  class TestWhenResetSessions():
    @pytest.fixture(scope='class')
    def created_request_one(self):
      return RequestMock(1)

    @pytest.fixture(autouse=True, scope='class')
    def cache(self):
      cache = Cache.instance()
      return cache

    def test_it_resets(self, cache: Cache, created_request_one: Request):
      cache.write('persists', 1)
      access_request('1', created_request_one.id)
      assert cache.read(f'1.{SUFFIX}') is not None

      reset_sessions()

      assert cache.read('persists') != None
      assert cache.read(f'1.{SUFFIX}') is None

  class TestWhenHeuristics():
    @pytest.fixture(scope='function')
    def session_id(self, request):
      return generate_session_id({
        'scenario_id': f'heuristics-{request.node.name}'
      })

    def test_it_picks_by_query_params(self, session_id: str):
      requests = [
        RequestMock(1, build_raw_request('/api?role=admin')),
        RequestMock(2, build_raw_request('/api?role=user')),
      ]

      request = tiebreak_scenario_request(
        session_id,
        requests,
        query_params={ 'role': 'user' },
      )
      assert request.id == 2

    def test_it_picks_higher_query_param_overlap(self, session_id: str):
      requests = [
        RequestMock(1, build_raw_request('/api?role=admin&env=prod')),
        RequestMock(2, build_raw_request('/api?role=admin&env=staging&region=us')),
      ]

      request = tiebreak_scenario_request(
        session_id,
        requests,
        query_params={ 'role': 'admin', 'env': 'staging', 'region': 'us' },
      )
      assert request.id == 2

    def test_it_picks_by_multi_value_query_param(self, session_id: str):
      requests = [
        RequestMock(1, build_raw_request('/api?tag=a&tag=b')),
        RequestMock(2, build_raw_request('/api?tag=c')),
      ]

      request = tiebreak_scenario_request(
        session_id,
        requests,
        query_params={ 'tag': ['a', 'b'] },
      )
      assert request.id == 1

    def test_it_prefers_query_params_over_sequence_id(self, session_id: str):
      requests = [
        RequestMock(1, build_raw_request('/api?role=admin'), sequence_id=9),
        RequestMock(2, build_raw_request('/api?role=user'), sequence_id=1),
      ]

      request = tiebreak_scenario_request(
        session_id,
        requests,
        query_params={ 'role': 'user' },
        sequence_id=9,
      )
      assert request.id == 2

    def test_it_picks_by_sequence_id_when_query_tied(self, session_id: str):
      requests = [
        RequestMock(1, build_raw_request('/api?role=admin'), sequence_id=1),
        RequestMock(2, build_raw_request('/api?role=admin'), sequence_id=3),
        RequestMock(3, build_raw_request('/api?role=admin'), sequence_id=5),
      ]

      request = tiebreak_scenario_request(
        session_id,
        requests,
        query_params={ 'role': 'admin' },
        sequence_id=3,
      )
      assert request.id == 2

    def test_it_picks_by_sequence_id_when_query_has_no_matches(self, session_id: str):
      requests = [
        RequestMock(1, build_raw_request('/api?role=admin'), sequence_id=1),
        RequestMock(2, build_raw_request('/api?role=user'), sequence_id=2),
      ]

      request = tiebreak_scenario_request(
        session_id,
        requests,
        query_params={ 'missing': 'value' },
        sequence_id=2,
      )
      assert request.id == 2

    def test_it_picks_exact_sequence_id(self, session_id: str):
      requests = [
        RequestMock(1, sequence_id=1),
        RequestMock(2, sequence_id=10),
        RequestMock(3, sequence_id=4),
      ]

      request = tiebreak_scenario_request(session_id, requests, sequence_id=4)
      assert request.id == 3

    def test_it_picks_sequence_id_zero(self, session_id: str):
      requests = [
        RequestMock(1, sequence_id=1),
        RequestMock(2, sequence_id=0),
        RequestMock(3, sequence_id=2),
      ]

      request = tiebreak_scenario_request(session_id, requests, sequence_id=0)
      assert request.id == 2

    def test_it_ignores_null_sequence_ids(self, session_id: str):
      requests = [
        RequestMock(1, sequence_id=None),
        RequestMock(2, sequence_id=5),
        RequestMock(3, sequence_id=None),
      ]

      request = tiebreak_scenario_request(session_id, requests, sequence_id=5)
      assert request.id == 2

    def test_it_falls_back_to_order_when_incoming_sequence_id_unset(self, session_id: str):
      requests = [
        RequestMock(1, sequence_id=1),
        RequestMock(2, sequence_id=2),
      ]

      access_request(session_id, requests[0].id)
      request = tiebreak_scenario_request(session_id, requests)
      assert request.id == 2

    def test_it_falls_back_to_order_when_all_recorded_sequence_ids_null(self, session_id: str):
      requests = [
        RequestMock(1, sequence_id=None),
        RequestMock(2, sequence_id=None),
      ]

      access_request(session_id, requests[0].id)
      request = tiebreak_scenario_request(session_id, requests, sequence_id=5)
      assert request.id == 2

    def test_it_falls_back_to_order_when_no_exact_sequence_id(self, session_id: str):
      requests = [
        RequestMock(1, build_raw_request('/api?role=admin'), sequence_id=1),
        RequestMock(2, build_raw_request('/api?role=admin'), sequence_id=2),
      ]

      access_request(session_id, requests[0].id)
      request = tiebreak_scenario_request(
        session_id,
        requests,
        query_params={ 'role': 'admin' },
        sequence_id=10,
      )
      assert request.id == 2

    def test_it_falls_back_to_order_when_query_tied_and_sequence_id_unset(self, session_id: str):
      requests = [
        RequestMock(1, build_raw_request('/api?role=admin'), sequence_id=1),
        RequestMock(2, build_raw_request('/api?role=admin'), sequence_id=2),
      ]

      access_request(session_id, requests[0].id)
      request = tiebreak_scenario_request(
        session_id,
        requests,
        query_params={ 'role': 'admin' },
      )
      assert request.id == 2

    def test_it_falls_back_to_first_when_no_session_and_no_heuristics_match(self, session_id: str):
      requests = [
        RequestMock(1, build_raw_request('/api?role=admin'), sequence_id=1),
        RequestMock(2, build_raw_request('/api?role=user'), sequence_id=2),
      ]

      request = tiebreak_scenario_request(
        session_id,
        requests,
        query_params={ 'missing': 'value' },
        sequence_id=99,
      )
      assert request.id == 1
