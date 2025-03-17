import copy
import pdb

from pathlib import Path
from pprint import pprint
from typing import Dict

import pytest

from stoobly_agent.app.cli.helpers.openapi_endpoint_adapter import (
  OpenApiEndpointAdapter,
)


@pytest.mark.openapi
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
  def petstore_references_file_path(self, mock_data_directory_path):
    path = mock_data_directory_path / "petstore-references.yaml"
    return path

  @pytest.fixture(scope='class')
  def uspto_file_path(self, mock_data_directory_path):
    path = mock_data_directory_path / "uspto.yaml"
    return path

  @pytest.fixture(scope='class')
  def petstore_swagger_io_file_path(self, mock_data_directory_path):
    path = mock_data_directory_path / "petstore-swagger-io.yaml"
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
            'is_deterministic': True,
            'is_required': False,
            'name': 'tagsElement',
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
        ],
        'path_segment_names': [
          {
            'name': 'v2',
            'type': 'static'
          },
          {
            'name': 'pets',
            'type': 'static'
          }
        ],
        'response_param_names': [
          {
            'endpoint_id': 1,
            'id': 1,
            'inferred_type': 'Hash',
            'is_deterministic': True,
            'is_required': False,
            'name': 'Element',
            'query': '[*]',
            'response_param_name_id': None
          },
          {
            'endpoint_id': 1,
            'id': 2,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': True,
            'name': 'name',
            'query': '[*].name',
            'response_param_name_id': 1,
            'values': ['']
          },
          {
            'endpoint_id': 1,
            'id': 3,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'tag',
            'query': '[*].tag',
            'response_param_name_id': 1
          },
          {
            'endpoint_id': 1,
            'id': 4,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': True,
            'name': 'id',
            'query': '[*].id',
            'response_param_name_id': 1,
            'values': [0]
          },
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
        'path_segment_names': [
          {
              'name': 'v2',
              'type': 'static',
          },
          {
              'name': 'pets',
              'type': 'static',
          },
        ],
        'response_param_names': [
          {
              'endpoint_id': 2,
              'id': 1,
              'inferred_type': 'String',
              'is_deterministic': True,
              'is_required': True,
              'name': 'name',
              'query': 'name',
              'response_param_name_id': None,
              'values': [''],
          },
          {
              'endpoint_id': 2,
              'id': 2,
              'inferred_type': 'String',
              'is_deterministic': True,
              'is_required': False,
              'name': 'tag',
              'query': 'tag',
              'response_param_name_id': None,
          },
          {
              'endpoint_id': 2,
              'id': 3,
              'inferred_type': 'Integer',
              'is_deterministic': True,
              'is_required': True,
              'name': 'id',
              'query': 'id',
              'response_param_name_id': None,
              'values': [0],
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
        'path_segment_names': [
            {
                'name': 'v2',
                'type': 'static',
            },
            {
                'name': 'pets',
                'type': 'static',
            },
            {
                'name': ':id',
                'type': 'alias',
            },
        ],
        'response_param_names': [
            {
                'endpoint_id': 3,
                'id': 1,
                'inferred_type': 'String',
                'is_deterministic': True,
                'is_required': True,
                'name': 'name',
                'query': 'name',
                'response_param_name_id': None,
                'values': [''],
            },
            {
                'endpoint_id': 3,
                'id': 2,
                'inferred_type': 'String',
                'is_deterministic': True,
                'is_required': False,
                'name': 'tag',
                'query': 'tag',
                'response_param_name_id': None,
            },
            {
                'endpoint_id': 3,
                'id': 3,
                'inferred_type': 'Integer',
                'is_deterministic': True,
                'is_required': True,
                'name': 'id',
                'query': 'id',
                'response_param_name_id': None,
                'values': [0],
            },
        ],
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
        'path_segment_names': [
          {
            'name': 'v2',
            'type': 'static',
          },
          {
            'name': 'pets',
            'type': 'static',
          },
          {
            'name': ':id',
            'type': 'alias',
          },
        ],
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
        'path_segment_names': [
          {
            'name': 'ds-api',
            'type': 'static',
          },
        ],
        'response_param_names': [
          {
            'endpoint_id': 1,
            'id': 1,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'total',
            'query': 'total',
            'response_param_name_id': None,
          },
          {
            'endpoint_id': 1,
            'id': 2,
            'inferred_type': 'Array',
            'is_deterministic': True,
            'is_required': False,
            'name': 'apis',
            'query': 'apis',
            'response_param_name_id': None,
          },
          {
              'endpoint_id': 1,
              'id': 3,
              'inferred_type': 'Hash',
              'is_deterministic': True,
              'is_required': False,
              'name': 'apisElement',
              'query': 'apis[*]',
              'response_param_name_id': 2,
          },
          {
              'endpoint_id': 1,
              'id': 4,
              'inferred_type': 'String',
              'is_deterministic': True,
              'is_required': False,
              'name': 'apiKey',
              'query': 'apis[*].apiKey',
              'response_param_name_id': 3,
          },
          {
              'endpoint_id': 1,
              'id': 5,
              'inferred_type': 'String',
              'is_deterministic': True,
              'is_required': False,
              'name': 'apiVersionNumber',
              'query': 'apis[*].apiVersionNumber',
              'response_param_name_id': 3,
          },
          {
              'endpoint_id': 1,
              'id': 6,
              'inferred_type': 'String',
              'is_deterministic': True,
              'is_required': False,
              'name': 'apiUrl',
              'query': 'apis[*].apiUrl',
              'response_param_name_id': 3,
          },
          {
              'endpoint_id': 1,
              'id': 7,
              'inferred_type': 'String',
              'is_deterministic': True,
              'is_required': False,
              'name': 'apiDocumentationUrl',
              'query': 'apis[*].apiDocumentationUrl',
              'response_param_name_id': 3,
          },
        ],
      }

    @pytest.fixture(scope='class')
    def expected_get_root_http(self, expected_get_root_https) -> Dict:
      http_endpoint_version = copy.deepcopy(expected_get_root_https)
      http_endpoint_version['id'] = 4
      http_endpoint_version['port'] = '80'
      for response_param_name in http_endpoint_version['response_param_names']:
        response_param_name['endpoint_id'] = 4
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
        'path_segment_names': [
          {
            'name': 'ds-api',
            'type': 'static',
          },
          {
            'name': ':dataset',
            'type': 'alias',
          },
          {
            'name': ':version',
            'type': 'alias',
          },
          {
            'name': 'fields',
            'type': 'static',
          },
        ],
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
        'path_segment_names': [
          {
            'name': 'ds-api',
            'type': 'static',
          },
          {
            'name': ':dataset',
            'type': 'alias',
          },
          {
            'name': ':version',
            'type': 'alias',
          },
          {
            'name': 'records',
            'type': 'static',
          },
        ],
     'response_param_names': [
          {
              'endpoint_id': 3,
              'id': 1,
              'inferred_type': 'Hash',
              'is_deterministic': True,
              'is_required': False,
              'name': 'Element',
              'query': '[*]',
              'response_param_name_id': None,
          },
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
      http_endpoint_version['response_param_names'][0]['endpoint_id'] = 6
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


  class TestWhenAdaptingPetstoreReferences():

    @pytest.fixture(scope='class')
    def expected_get_v1_pets_ref(self) -> Dict:
      return {
        'id': 1,
        'method': 'POST',
        'host': 'petstore.swagger.io',
        'port': '80',
        'match_pattern': '/v1/pets',
        'path': '/v1/pets',
        'body_param_names': [
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 1,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': True,
            'name': 'name',
            'query': 'name',
            'values': ['']
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 2,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'tag',
            'query': 'tag'
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 3,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': True,
            'name': 'color',
            'query': 'color',
            'values': ['']
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 4,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': True,
            'name': 'age',
            'query': 'age',
            'values': [0]
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 5,
            'inferred_type': 'Hash',
            'is_deterministic': True,
            'is_required': False,
            'name': 'adoption',
            'query': 'adoption',
          },
          {
            'body_param_name_id': 5,
            'endpoint_id': 1,
            'id': 6,
            'inferred_type': 'Boolean',
            'is_deterministic': True,
            'is_required': True,
            'name': 'adopted',
            'query': 'adoption.adopted',
            'values': [False],
          },
          {
            'body_param_name_id': 5,
            'endpoint_id': 1,
            'id': 7,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'shelter',
            'query': 'adoption.shelter',
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 8,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': True,
            'name': 'id',
            'query': 'id',
            'values': [0],
          },
        ],
        'path_segment_names': [
          {
            'name': 'v1',
            'type': 'static',
          },
          {
            'name': 'pets',
            'type': 'static',
          },
        ],
      }

    @pytest.fixture(scope='class')
    def expected_get_v2_pets_ref(self) -> Dict:
      return {
        'host': 'petstore.swagger.io',
        'id': 2,
        'match_pattern': '/v2/pets',
        'method': 'POST',
        'path': '/v2/pets',
        'port': '80',
        'body_param_names': [
          {
            'body_param_name_id': None,
            'endpoint_id': 2,
            'id': 1,
            'inferred_type': 'Hash',
            'is_deterministic': True,
            'is_required': False,
            'name': 'base',
            'query': 'base'
          },
          {
            'body_param_name_id': 1,
            'endpoint_id': 2,
            'id': 2,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': True,
            'name': 'name',
            'query': 'base.name',
            'values': ['']
          },
          {
            'body_param_name_id': 1,
            'endpoint_id': 2,
            'id': 3,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'tag',
            'query': 'base.tag'
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 2,
            'id': 4,
            'inferred_type': 'Hash',
            'is_deterministic': True,
            'is_required': False,
            'name': 'extra',
            'query': 'extra'
          },
          {
            'body_param_name_id': 4,
            'endpoint_id': 2,
            'id': 5,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': True,
            'name': 'color',
            'query': 'extra.color',
            'values': ['']
          },
          {
            'body_param_name_id': 4,
            'endpoint_id': 2,
            'id': 6,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': True,
            'name': 'age',
            'query': 'extra.age',
            'values': [0]
          },
          {
            'body_param_name_id': 4,
            'endpoint_id': 2,
            'id': 7,
            'inferred_type': 'Hash',
            'is_deterministic': True,
            'is_required': False,
            'name': 'adoption',
            'query': 'extra.adoption'
          },
          {
            'body_param_name_id': 7,
            'endpoint_id': 2,
            'id': 8,
            'inferred_type': 'Boolean',
            'is_deterministic': True,
            'is_required': True,
            'name': 'adopted',
            'query': 'extra.adoption.adopted',
            'values': [False]
          },
          {
            'body_param_name_id': 7,
            'endpoint_id': 2,
            'id': 9,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'shelter',
            'query': 'extra.adoption.shelter'
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 2,
            'id': 10,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': True,
            'name': 'id',
            'query': 'id',
            'values': [0]}
          ],
          'path_segment_names': [
            {
              'name': 'v2',
              'type': 'static',
            },
            {
              'name': 'pets',
              'type': 'static',
            },
          ],
        }

    def test_adapt_from_file(self, open_api_endpoint_adapter, petstore_references_file_path, expected_get_v1_pets_ref, expected_get_v2_pets_ref):
      adapter = open_api_endpoint_adapter
      file_path = petstore_references_file_path

      endpoints = adapter.adapt_from_file(file_path)

      assert len(endpoints) == 2

      get_v1_pets_ref = endpoints[0]
      get_v2_pets_ref = endpoints[1]

      assert get_v1_pets_ref == expected_get_v1_pets_ref
      assert get_v2_pets_ref == expected_get_v2_pets_ref

  class TestWhenAdaptingPetstoreSwaggerIo():

    @pytest.fixture(scope='class')
    def expected_put_v3_pets_ref(self) -> Dict:
      return {
        'host': '-',
        'id': 1,
        'match_pattern': '/v3/pet',
        'method': 'PUT',
        'path': '/v3/pet',
        'port': '0',
        'body_param_names': [
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 1,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'id',
            'query': 'id'
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 2,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': True,
            'name': 'name',
            'query': 'name',
            'values': ['']
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 3,
            'inferred_type': 'Hash',
            'is_deterministic': True,
            'is_required': False,
            'name': 'category',
            'query': 'category'
          },
          {
            'body_param_name_id': 3,
            'endpoint_id': 1,
            'id': 4,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'id',
            'query': 'category.id'
          },
          {
            'body_param_name_id': 3,
            'endpoint_id': 1,
            'id': 5,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'name',
            'query': 'category.name',
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 6,
            'inferred_type': 'Array',
            'is_deterministic': True,
            'is_required': True,
            'name': 'photoUrls',
            'query': 'photoUrls',
            'values': [[]],
          },
          {
            'body_param_name_id': 6,
            'endpoint_id': 1,
            'id': 7,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'photoUrlsElement',
            'query': 'photoUrls[*]'
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 8,
            'inferred_type': 'Array',
            'is_deterministic': True,
            'is_required': False,
            'name': 'tags',
            'query': 'tags'
          },
          {
            'body_param_name_id': 8,
            'endpoint_id': 1,
            'id': 9,
            'inferred_type': 'Hash',
            'is_deterministic': True,
            'is_required': False,
            'name': 'tagsElement',
            'query': 'tags[*]'
          },
          {
            'body_param_name_id': 9,
            'endpoint_id': 1,
            'id': 10,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'id',
            'query': 'tags[*].id'
          },
          {
            'body_param_name_id': 9,
            'endpoint_id': 1,
            'id': 11,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'name',
            'query': 'tags[*].name',
          },
          {
            'body_param_name_id': None,
            'endpoint_id': 1,
            'id': 12,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'status',
            'query': 'status'
          },
        ],
        'path_segment_names': [
          {
              'name': 'v3',
              'type': 'static',
          },
          {
              'name': 'pet',
              'type': 'static',
          },
        ],
        'response_param_names': [
          {
              'endpoint_id': 1,
              'id': 1,
              'inferred_type': 'Integer',
              'is_deterministic': True,
              'is_required': False,
              'name': 'id',
              'query': 'id',
              'response_param_name_id': None,
          },
          {
              'endpoint_id': 1,
              'id': 2,
              'inferred_type': 'String',
              'is_deterministic': True,
              'is_required': True,
              'name': 'name',
              'query': 'name',
              'response_param_name_id': None,
              'values': [''],
          },
          {
              'endpoint_id': 1,
              'id': 3,
              'inferred_type': 'Hash',
              'is_deterministic': True,
              'is_required': False,
              'name': 'category',
              'query': 'category',
              'response_param_name_id': None,
          },
          {
              'endpoint_id': 1,
              'id': 4,
              'inferred_type': 'Integer',
              'is_deterministic': True,
              'is_required': False,
              'name': 'id',
              'query': 'category.id',
              'response_param_name_id': 3,
          },
          {
              'endpoint_id': 1,
              'id': 5,
              'inferred_type': 'String',
              'is_deterministic': True,
              'is_required': False,
              'name': 'name',
              'query': 'category.name',
              'response_param_name_id': 3,
          },
          {
              'endpoint_id': 1,
              'id': 6,
              'inferred_type': 'Array',
              'is_deterministic': True,
              'is_required': True,
              'name': 'photoUrls',
              'query': 'photoUrls',
              'response_param_name_id': None,
              'values': [[]],
          },
          {
            'endpoint_id': 1,
            'id': 7,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'photoUrlsElement',
            'query': 'photoUrls[*]',
            'response_param_name_id': 6,
          },
          {
            'endpoint_id': 1,
            'id': 8,
            'inferred_type': 'Array',
            'is_deterministic': True,
            'is_required': False,
            'name': 'tags',
            'query': 'tags',
            'response_param_name_id': None,
          },
          {
            'endpoint_id': 1,
            'id': 9,
            'inferred_type': 'Hash',
            'is_deterministic': True,
            'is_required': False,
            'name': 'tagsElement',
            'query': 'tags[*]',
            'response_param_name_id': 8,
          },
          {
            'endpoint_id': 1,
            'id': 10,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'id',
            'query': 'tags[*].id',
            'response_param_name_id': 9,
          },
          {
            'endpoint_id': 1,
            'id': 11,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'name',
            'query': 'tags[*].name',
            'response_param_name_id': 9,
          },
          {
            'endpoint_id': 1,
            'id': 12,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'status',
            'query': 'status',
            'response_param_name_id': None,
          },
        ],
      }

    @pytest.fixture(scope='class')
    def expected_post_v3_user_createwithlist(self) -> Dict:
      return {
        'host': '-',
        'id': 14,
        'match_pattern': '/v3/user/createWithList',
        'method': 'POST',
        'path': '/v3/user/createWithList',
        'port': '0',
        'body_param_names': [
          {
            'body_param_name_id': None,
            'endpoint_id': 14,
            'id': 1,
            'inferred_type': 'Hash',
            'is_deterministic': True,
            'is_required': False,
            'name': 'Element',
            'query': '[*]'
          },
          {
            'body_param_name_id': 1,
            'endpoint_id': 14,
            'id': 2,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'id',
            'query': '[*].id'
          },
          {
            'body_param_name_id': 1,
            'endpoint_id': 14,
            'id': 3,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'username',
            'query': '[*].username'
          },
          {
            'body_param_name_id': 1,
            'endpoint_id': 14,
            'id': 4,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'firstName',
            'query': '[*].firstName'
          },
          {
            'body_param_name_id': 1,
            'endpoint_id': 14,
            'id': 5,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'lastName',
            'query': '[*].lastName'
          },
          {
            'body_param_name_id': 1,
            'endpoint_id': 14,
            'id': 6,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'email',
            'query': '[*].email'
          },
          {
            'body_param_name_id': 1,
            'endpoint_id': 14,
            'id': 7,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'password',
            'query': '[*].password'
          },
          {
            'body_param_name_id': 1,
            'endpoint_id': 14,
            'id': 8,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'phone',
            'query': '[*].phone'
          },
          {
            'body_param_name_id': 1,
            'endpoint_id': 14,
            'id': 9,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'userStatus',
            'query': '[*].userStatus'
          }
        ],
        'path_segment_names': [
          {
            'name': 'v3',
            'type': 'static',
          },
          {
            'name': 'user',
            'type': 'static',
          },
          {
            'name': 'createWithList',
            'type': 'static',
          },
        ],
        'response_param_names': [
          {
            'endpoint_id': 14,
            'id': 1,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'id',
            'query': 'id',
            'response_param_name_id': None,
          },
          {
            'endpoint_id': 14,
            'id': 2,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'username',
            'query': 'username',
            'response_param_name_id': None,
          },
          {
            'endpoint_id': 14,
            'id': 3,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'firstName',
            'query': 'firstName',
            'response_param_name_id': None,
          },
          {
            'endpoint_id': 14,
            'id': 4,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'lastName',
            'query': 'lastName',
            'response_param_name_id': None,
          },
          {
            'endpoint_id': 14,
            'id': 5,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'email',
            'query': 'email',
            'response_param_name_id': None,
          },
          {
            'endpoint_id': 14,
            'id': 6,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'password',
            'query': 'password',
            'response_param_name_id': None,
          },
          {
            'endpoint_id': 14,
            'id': 7,
            'inferred_type': 'String',
            'is_deterministic': True,
            'is_required': False,
            'name': 'phone',
            'query': 'phone',
            'response_param_name_id': None,
          },
          {
            'endpoint_id': 14,
            'id': 8,
            'inferred_type': 'Integer',
            'is_deterministic': True,
            'is_required': False,
            'name': 'userStatus',
            'query': 'userStatus',
            'response_param_name_id': None,
          },
        ],

      }

    def test_adapt_from_file(self, open_api_endpoint_adapter, petstore_swagger_io_file_path, expected_put_v3_pets_ref, expected_post_v3_user_createwithlist):
      adapter = open_api_endpoint_adapter
      file_path = petstore_swagger_io_file_path

      endpoints = adapter.adapt_from_file(file_path)

      assert len(endpoints) == 19

      put_v3_pets_ref = endpoints[0]
      post_v3_user_createwithlist = endpoints[13]

      assert put_v3_pets_ref == expected_put_v3_pets_ref
      assert post_v3_user_createwithlist == expected_post_v3_user_createwithlist

