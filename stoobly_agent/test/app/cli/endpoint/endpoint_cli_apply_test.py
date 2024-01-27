import json
import pdb
import pytest

from click.testing import CliRunner
from pathlib import Path

from stoobly_agent.test.test_helper import reset

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.types import OPENAPI_FORMAT
from stoobly_agent.app.settings import Settings
from stoobly_agent.cli import endpoint
from stoobly_agent.lib.orm.request import Request

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

@pytest.fixture(scope='module')
def mock_data_directory_path() -> str:
  return Path(__file__).parent.parent.parent.parent / 'mock_data'

@pytest.fixture(scope='module')
def petstore_expanded_file_path(mock_data_directory_path) -> str:
  path = mock_data_directory_path / "petstore-expanded.yaml"
  return str(path)

@pytest.mark.openapi
class TestApply():
    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def request_body_one(self):
        return {
            'name': 'pet1',
            'tag': 'best',
        }

    @pytest.fixture(scope='class', autouse=True)
    def created_request_extra_body_param(self, settings: Settings, request_body_one):
        body = {
            **request_body_one,
            'delete': 1,
        }

        status = RequestBuilder(
            method='POST',
            request_body=body,
            request_headers={
                'content-type': 'application/json'
            },
            response_body=body,
            response_headers={
                'content-type': 'application/json'
            },
            status_code=200,
            url='https://petstore.swagger.io/v2/pets',
        ).with_settings(settings).build()[1]
        assert status == 200

        return Request.last()

    @pytest.fixture(scope='class')
    def request_body_two(self):
        return {
            'name': 'pet1',
        }

    @pytest.fixture(scope='class', autouse=True)
    def created_request_missing_body_param(self, settings: Settings):
        body = {
          'tag': 'best',
        }

        status = RequestBuilder(
            method='POST',
            request_body=body,
            request_headers={
                'content-type': 'application/json'
            },
            response_body=body,
            response_headers={
                'content-type': 'application/json'
            },
            status_code=200,
            url='https://petstore.swagger.io/v2/pets',
        ).with_settings(settings).build()[1]
        assert status == 200

        return Request.last()

    class TestWhenApplyingPestoreExpanded():

        @pytest.fixture(scope='class', autouse=True)
        def import_result(self, runner: CliRunner, petstore_expanded_file_path: str):
            record_result = runner.invoke(endpoint, ['apply', '--source-format', OPENAPI_FORMAT, '--source-path', petstore_expanded_file_path])
            assert record_result.exit_code == 0
            return record_result

        def test_it_deletes(self, created_request_extra_body_param: Request, request_body_one):
            _created_request = Request.find(created_request_extra_body_param.id)
            python_request = RawHttpRequestAdapter(_created_request.raw).to_request()
            assert python_request.data == json.dumps(request_body_one).encode()

        def test_it_adds(self, created_request_missing_body_param: Request):
            _created_request = Request.find(created_request_missing_body_param.id)
            python_request = RawHttpRequestAdapter(_created_request.raw).to_request()

            assert python_request.data == json.dumps({
                'tag': 'best',
                'name': '',
            }).encode()

