import json
import pdb
import pytest
import requests

from click.testing import CliRunner
from io import BytesIO
from urllib3 import HTTPResponse
from pathlib import Path

from stoobly_agent.test.test_helper import reset

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.helpers.create_request_params_service import build_params_from_python
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.types import OPENAPI_FORMAT
from stoobly_agent.app.settings import Settings
from stoobly_agent.cli import endpoint
from stoobly_agent.lib.orm.request import Request

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

class TestImport():
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
    def created_request_one(self, settings: Settings, request_body_one):
        body = json.dumps({
            **request_body_one,
            'delete': 1,
        })

        req = requests.Request(
            method='POST',
            url='https://petstore.swagger.io/v2/pets',
            headers={
                'content-type': 'application/json'
            },
            data=body
        )
        
        res_headers = {
            'content-type': 'application/json'
        }
        res = requests.Response()
        res.headers = res_headers
        res.raw =  HTTPResponse(
            body=BytesIO(body.encode()),
            decode_content=False,
            headers=res_headers,
            preload_content=False
        ) 
        res.status_code = 200

        params = build_params_from_python(req, res)

        model = RequestModel(settings)
        status = model.create(**params)[1]
        assert status == 200
        return Request.last()

    @pytest.fixture(scope='class')
    def request_body_two(self):
        return {
            'name': 'pet1',
        }

    @pytest.fixture(scope='class', autouse=True)
    def created_request_two(self, settings: Settings, request_body_two):
        body = json.dumps({
            **request_body_two,
        })

        req = requests.Request(
            method='POST',
            url='https://petstore.swagger.io/v2/pets',
            headers={
                'content-type': 'application/json'
            },
            data=body
        )
        
        res_headers = {
            'content-type': 'application/json'
        }
        res = requests.Response()
        res.headers = res_headers
        res.raw =  HTTPResponse(
            body=BytesIO(body.encode()),
            decode_content=False,
            headers=res_headers,
            preload_content=False
        ) 
        res.status_code = 200

        params = build_params_from_python(req, res)

        model = RequestModel(settings)
        status = model.create(**params)[1]
        assert status == 200
        return Request.last()

    class TestWhenImportingPestoreExpanded():

        @pytest.fixture(scope='class', autouse=True)
        def import_result(self, runner: CliRunner, petstore_expanded_file_path: str):
            record_result = runner.invoke(endpoint, ['import', '--format', OPENAPI_FORMAT, petstore_expanded_file_path])
            assert record_result.exit_code == 0
            return record_result

        def test_it_deletes(self, created_request_one: Request, request_body_one):
            _created_request = Request.find(created_request_one.id)
            python_request = RawHttpRequestAdapter(_created_request.raw).to_request()
            assert python_request.data == json.dumps(request_body_one).encode()

        def test_it_adds(self, created_request_two: Request, request_body_two):
            _created_request = Request.find(created_request_two.id)
            python_request = RawHttpRequestAdapter(_created_request.raw).to_request()
            assert python_request.data == json.dumps({
                **request_body_two,
                'tag': '',
            }).encode()

