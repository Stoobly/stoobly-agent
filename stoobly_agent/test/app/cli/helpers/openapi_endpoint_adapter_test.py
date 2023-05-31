from pathlib import Path
import pdb
from pprint import pprint
from typing import Dict

import pytest

from stoobly_agent.app.cli.helpers.openapi_endpoint_adapter import (
  OpenApiEndpointAdapter,
)

@pytest.fixture(scope='class')
def mock_data_directory_path():
  return Path(__file__).parent.parent.parent.parent / 'mock_data'

@pytest.fixture(scope='class')
def petstore_file_path(mock_data_directory_path):
  path = mock_data_directory_path / "petstore.yaml"
  return path

@pytest.fixture(scope='class')
def petstore_expanded_file_path(mock_data_directory_path):
  path = mock_data_directory_path / "petstore-expanded.yaml"
  return path

@pytest.fixture(scope='class')
def expected_get_pets_endpoint() -> Dict:
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
def expected_post_pets_endpoint() -> Dict:
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
def expected_get_pets_id_endpoint() -> Dict:
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
def expected_delete_pets_id_endpoint() -> Dict:
  return {
    'id': 4,
    'method': 'DELETE',
    'host': 'petstore.swagger.io',
    'path': '/v2/pets/{id}',
    'match_pattern': '/v2/pets/%',
    'port': '443',
    'aliases': [{'id': 1, 'name': '{id}'}],
  }

@pytest.fixture(scope='class')
def open_api_endpoint_adapter():
  adapter = OpenApiEndpointAdapter()
  return adapter

class TestOpenApiEndpointAdapter():
  def test_adapt_from_file(self, open_api_endpoint_adapter, petstore_expanded_file_path, expected_get_pets_endpoint, expected_post_pets_endpoint, expected_get_pets_id_endpoint, expected_delete_pets_id_endpoint):
    adapter = open_api_endpoint_adapter
    file_path = petstore_expanded_file_path

    endpoints = adapter.adapt_from_file(file_path)

    assert len(endpoints) == 4

    get_pets_endpoint = endpoints[0]
    post_gets_endpoint = endpoints[1]
    get_pets_id_endpoint = endpoints[2]
    delete_pets_id_endpoint = endpoints[3]

    assert get_pets_endpoint == expected_get_pets_endpoint
    assert post_gets_endpoint == expected_post_pets_endpoint
    assert get_pets_id_endpoint == expected_get_pets_id_endpoint
    assert delete_pets_id_endpoint == expected_delete_pets_id_endpoint

