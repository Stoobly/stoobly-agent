from pathlib import Path
import pytest
from stoobly_agent.app.cli.helpers.endpoint_facade import EndpointFacade

from stoobly_agent.app.settings import Settings
from stoobly_agent.app.models.types import EndpointCreateParams, OPENAPI_FORMAT


@pytest.fixture
def petstore_file_path():
  path = Path(__file__).parent / "petstore.yaml"
  return path 

@pytest.fixture
def petstore_expanded_file_path():
  path = Path(__file__).parent / "petstore-expanded.yaml"
  return path 

class TestEndpointFacade():
  def test_create(self, petstore_expanded_file_path):
    settings = Settings.instance()
    open_api_facade = EndpointFacade(settings)
    params: EndpointCreateParams = {}
    params['format'] = OPENAPI_FORMAT
    params['endpoints'] = petstore_expanded_file_path

    open_api_facade.create(**params)

