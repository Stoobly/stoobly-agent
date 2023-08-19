from pathlib import Path
from typing import Dict

import pytest

from stoobly_agent.app.cli.helpers.openapi_endpoint_adapter import (
  OpenApiEndpointAdapter,
)


@pytest.mark.openapi
class TestOpenApiEndpointAdapterMissingOauthScopes():
  @pytest.fixture(scope='class')
  def mock_data_directory_path(self):
    return Path(__file__).parent.parent.parent.parent / 'mock_data'

  @pytest.fixture(scope='class')
  def petstore_file_path(self, mock_data_directory_path):
    path = mock_data_directory_path / "petstore-missing-oauth2-scopes.yaml"
    return path

  @pytest.fixture(scope='class')
  def open_api_endpoint_adapter(self):
    adapter = OpenApiEndpointAdapter()
    return adapter

  @pytest.fixture(scope='class')
  def expected_get_pets_endpoint(self) -> Dict:
    return {
      "id": 1,
      "method": "GET",
      "host": "petstore.swagger.io",
      "match_pattern": "/v1/pets",
      "path": "/v1/pets",
      "port": "80",
      "query_param_names": [
        {
          "endpoint_id": 1,
          "inferred_type": "Integer",
          "is_required": False,
          "is_deterministic": True,
          "name": "limit",
          "query": "limit",
          "query_param_name_id": None,
          "id": 1
        }
      ]
    }

  def test_adapt_from_file(self, open_api_endpoint_adapter, petstore_file_path, expected_get_pets_endpoint):
    adapter = open_api_endpoint_adapter

    endpoints = adapter.adapt_from_file(petstore_file_path)

    assert len(endpoints) == 1
    get_pets_endpoint = endpoints[0]
    assert get_pets_endpoint == expected_get_pets_endpoint

