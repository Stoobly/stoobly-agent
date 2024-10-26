import pdb
import pytest
import time

from typing import List

from stoobly_agent.app.models.factories.resource.local_db.helpers.tiebreak_scenario_request import (
  access_request, generate_session_id, reset as reset_tiebreak, tiebreak_scenario_request
)
from stoobly_agent.lib.cache import Cache
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.test.test_helper import reset

class RequestMock():

  def __init__(self, id):
    self.__id = id

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

  class TestWhenReset():
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
      reset_tiebreak()

      assert cache.read('persists') != None
      assert len(cache.read_all()) == 1