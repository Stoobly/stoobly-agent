import copy
from pathlib import Path
import pdb
from pprint import pprint
from typing import Dict

import pytest

from stoobly_agent.app.cli.helpers.openapi_endpoint_adapter import (
  OpenApiEndpointAdapter,
)


class TestOpenApiEndpointAdapter():
  @pytest.fixture(scope='class')
  def mock_data_directory_path(self):
    return Path(__file__).parent.parent.parent.parent / 'mock_data'

  @pytest.fixture(scope='class')
  def petstore_file_path(self, mock_data_directory_path):
    path = mock_data_directory_path / "petstore.yaml"
    return path

  @pytest.fixture(scope='class')
  def petstore_expanded_file_path(self, mock_data_directory_path):
    path = mock_data_directory_path / "petstore-expanded.yaml"
    return path

  @pytest.fixture(scope='class')
  def uspto_file_path(self, mock_data_directory_path):
    path = mock_data_directory_path / "uspto.yaml"
    return path

  @pytest.fixture(scope='class')
  def open_api_endpoint_adapter(self):
    adapter = OpenApiEndpointAdapter()
    return adapter

  class TestWhenAdaptingPestoreExpanded():

    @pytest.fixture(scope='class')
    def expected_v2_get_pets_endpoint(self) -> Dict:
      return {
        'id': 1,
        'method': 'GET',
        'host': 'petstore.swagger.io',
        'port': '443',
        'match_pattern': '/v2/pets',
        'path': '/v2/pets',
        'query_param_names': [
          {
            'endpoint_id': 1,
            'id': 1,
            'inferred_type': 'Array',
            'is_deterministic': True,
            'is_required': False,
            'name': 'tags',
            'query': 'tags',
            'query_param_name_id': None,
          },
          {
            'endpoint_id': 1,
            'id': 2,
            'inferred_type': 'String',
            'is_required': False,
            'name': 'TagsElement',
            'query': 'tags[*]',
            'query_param_name_id': 1,
          },
          {
            'endpoint_id': 1,
            'id': 3,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'limit',
            'query': 'limit',
            'query_param_name_id': None,
          }
        ]
      }

    @pytest.fixture(scope='class')
    def expected_v2_post_pets_endpoint(self) -> Dict:
      return {
        'id': 2,
        'method': 'POST',
        'host': 'petstore.swagger.io',
        'port': '443',
        'match_pattern': '/v2/pets',
        'path': '/v2/pets',
        'body_param_names': [
          {
            'body_param_name_id': None,
            'endpoint_id': 2,
            'id': 1,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': True,
            'name': 'name',
            'query': 'name',
            'values': [''],
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 2,
            'id': 2,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'tag',
            'query': 'tag',
          },
        ],
      }

    @pytest.fixture(scope='class')
    def expected_v2_get_pets_id_endpoint(self) -> Dict:
      return {
        'id': 3,
        'method': 'GET',
        'host': 'petstore.swagger.io',
        'port': '443',
        'path': '/v2/pets/{id}',
        'match_pattern': '/v2/pets/%',
        'aliases': [{'id': 1, 'name': '{id}'}],
      }

    @pytest.fixture(scope='class')
    def expected_v2_delete_pets_id_endpoint(self) -> Dict:
      return {
        'id': 4,
        'method': 'DELETE',
        'host': 'petstore.swagger.io',
        'path': '/v2/pets/{id}',
        'match_pattern': '/v2/pets/%',
        'port': '443',
        'aliases': [{'id': 1, 'name': '{id}'}],
      }

    def test_adapt_from_file(self, open_api_endpoint_adapter, petstore_expanded_file_path, expected_v2_get_pets_endpoint, expected_v2_post_pets_endpoint, expected_v2_get_pets_id_endpoint, expected_v2_delete_pets_id_endpoint):
      adapter = open_api_endpoint_adapter
      file_path = petstore_expanded_file_path

      endpoints = adapter.adapt_from_file(file_path)

      assert len(endpoints) == 4

      get_pets_endpoint = endpoints[0]
      post_gets_endpoint = endpoints[1]
      get_pets_id_endpoint = endpoints[2]
      delete_pets_id_endpoint = endpoints[3]

      assert get_pets_endpoint == expected_v2_get_pets_endpoint
      assert post_gets_endpoint == expected_v2_post_pets_endpoint
      assert get_pets_id_endpoint == expected_v2_get_pets_id_endpoint
      assert delete_pets_id_endpoint == expected_v2_delete_pets_id_endpoint


  class TestWhenAdaptingUspto():

    @pytest.fixture(scope='class')
    def expected_get_root_https(self) -> Dict:
      return {
        'id': 1,
        'method': 'GET',
        'host': 'developer.uspto.gov',
        'port': '443',
        'path': '/ds-api/',
        'match_pattern': '/ds-api/',
      }

    @pytest.fixture(scope='class')
    def expected_get_root_http(self, expected_get_root_https) -> Dict:
      http_endpoint_version = copy.deepcopy(expected_get_root_https)
      http_endpoint_version['id'] = 4
      http_endpoint_version['port'] = '80'
      return http_endpoint_version

    @pytest.fixture(scope='class')
    def expected_get_dataset_version_fields_https(self) -> Dict:
      return {
        'id': 2,
        'method': 'GET',
        'host': 'developer.uspto.gov',
        'port': '443',
        'match_pattern': '/ds-api/%/%/fields',
        'path': '/ds-api/{dataset}/{version}/fields',
        'aliases': [{'id': 1, 'name': '{dataset}'}, {'id': 2, 'name': '{version}'}],
      }

    @pytest.fixture(scope='class')
    def expected_get_dataset_version_fields_http(self, expected_get_dataset_version_fields_https) -> Dict:
      http_endpoint_version = copy.deepcopy(expected_get_dataset_version_fields_https)
      http_endpoint_version['id'] = 5
      http_endpoint_version['port'] = '80'
      return http_endpoint_version

    @pytest.fixture(scope='class')
    def expected_post_dataset_version_records_https(self) -> Dict:
      return {
        'id': 3,
        'method': 'POST',
        'host': 'developer.uspto.gov',
        'port': '443',
        'path': '/ds-api/{dataset}/{version}/records',
        'match_pattern': '/ds-api/%/%/records',
        'aliases': [{'id': 1, 'name': '{version}'}, {'id': 2, 'name': '{dataset}'}],
        'body_param_names': [
          {
            'body_param_name_id': None,
            'endpoint_id': 3,
            'id': 1,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': True,
            'name': 'criteria',
            'query': 'criteria',
            'values': [''],
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 3,
            'id': 2,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'start',
            'query': 'start',
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 3,
            'id': 3,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'rows',
            'query': 'rows',
          }
        ],
      }

    @pytest.fixture(scope='class')
    def expected_post_dataset_version_records_http(self, expected_post_dataset_version_records_https) -> Dict:
      http_endpoint_version = copy.deepcopy(expected_post_dataset_version_records_https)
      http_endpoint_version['id'] = 6
      http_endpoint_version['port'] = '80'
      http_endpoint_version['body_param_names'][0]['endpoint_id'] = 6
      http_endpoint_version['body_param_names'][1]['endpoint_id'] = 6
      http_endpoint_version['body_param_names'][2]['endpoint_id'] = 6
      return http_endpoint_version

    def test_adapt_from_file(self, open_api_endpoint_adapter, uspto_file_path, expected_get_root_https, expected_get_root_http, expected_get_dataset_version_fields_https, expected_get_dataset_version_fields_http, expected_post_dataset_version_records_https, expected_post_dataset_version_records_http):
      adapter = open_api_endpoint_adapter
      file_path = uspto_file_path 

      endpoints = adapter.adapt_from_file(file_path)

      assert len(endpoints) == 6

      get_root_https_endpoint = endpoints[0]
      get_dataset_version_fields_https = endpoints[1]
      post_dataset_version_records_https = endpoints[2]
      get_root_http_endpoint = endpoints[3]
      get_dataset_version_fields_http = endpoints[4]
      post_dataset_version_records_http = endpoints[5]

      assert get_root_https_endpoint == expected_get_root_https
      assert get_root_http_endpoint == expected_get_root_http
      assert get_dataset_version_fields_https == expected_get_dataset_version_fields_https
      assert get_dataset_version_fields_http == expected_get_dataset_version_fields_http

      assert post_dataset_version_records_https == expected_post_dataset_version_records_https
      assert post_dataset_version_records_http == expected_post_dataset_version_records_http
