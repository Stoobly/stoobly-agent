from pathlib import Path
from pprint import pprint
import pdb

import pytest

from stoobly_agent.app.cli.helpers.openapi_endpoint_adapter import (
  OpenApiEndpointAdapter,
)

@pytest.fixture
def mock_data_directory_path():
  return Path(__file__).parent.parent.parent.parent / 'mock_data'

@pytest.fixture
def petstore_file_path(mock_data_directory_path):
  path = mock_data_directory_path / "petstore.yaml"
  return path 

@pytest.fixture
def petstore_expanded_file_path(mock_data_directory_path):
  path = mock_data_directory_path / "petstore-expanded.yaml"
  return path 

@pytest.fixture(scope='class')
def open_api_endpoint_adapter():
  adapter = OpenApiEndpointAdapter()
  return adapter

class TestOpenApiEndpointAdapter():
  def test_create(self, open_api_endpoint_adapter, petstore_expanded_file_path):
    adapter = open_api_endpoint_adapter
    file_path = petstore_expanded_file_path

    endpoints = adapter.adapt_from_file(file_path)

    # pdb.set_trace()
    assert len(endpoints) == 4

