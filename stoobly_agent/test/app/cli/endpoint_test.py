from pathlib import Path
import pytest
from stoobly_agent.app.cli.helpers.endpoint_facade import EndpointFacade

from stoobly_agent.app.settings import Settings


@pytest.fixture
def petstore_file_path():
  path = Path(__file__).parent / "petstore.yaml"
  return path 

class TestEndpointFacade():
  def test_main_foo(self, petstore_file_path):
    settings = Settings.instance()
    open_api_facade = EndpointFacade(settings=settings)

    open_api_facade.main_foo(petstore_file_path)
