import pdb
import pytest

from stoobly_agent.mock import Mock
from stoobly_agent.app.models.schemas.request import Request

@pytest.fixture
def request_with_body_headers_query_params_response():
  res = Mock.get('http://0.0.0.0:3002/requests/14812?project_id=67&body=True&headers=True&query_params=True&response=True')
  return res.json()

@pytest.fixture
def stoobly_request(request_with_body_headers_query_params_response):
  return Request(request_with_body_headers_query_params_response)

class TestRequest():
  
  def test_url(self, stoobly_request: Request):
    assert stoobly_request.url == 'http://www.google.com/'

  def test_path(self, stoobly_request: Request):
    assert stoobly_request.path == '/'

  def test_method(self, stoobly_request: Request):
    assert stoobly_request.method == 'GET'

  def test_query_params(self, stoobly_request: Request):
    assert len(stoobly_request.query_params) == 0

  def test_body(self, stoobly_request: Request):
    assert stoobly_request.body == ''

  def test_headers(self, stoobly_request: Request):
    assert stoobly_request.headers['content-length'] == '0'