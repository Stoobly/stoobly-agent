from pathlib import Path
from unittest.mock import patch

import pytest

from stoobly_agent.app.proxy.mock.hashed_request_decorator import COMPONENT_TYPES
from stoobly_agent.app.proxy.mock.search_open_api_endpoint import (
  build_ignored_components_from_openapi_endpoint,
  inject_search_open_api_endpoint,
  load_openapi_endpoints_from_file,
  search_open_api_endpoint,
  sql_like,
)
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import env_vars


@pytest.fixture(autouse=True)
def clear_openapi_endpoint_cache():
  from stoobly_agent.app.proxy.mock import search_open_api_endpoint as mod

  mod._endpoint_cache._by_path.clear()
  yield
  mod._endpoint_cache._by_path.clear()


@pytest.fixture
def petstore_expanded_path():
  test_dir = Path(__file__).resolve().parent.parent.parent.parent
  return test_dir / "mock_data" / "petstore-expanded.yaml"


@pytest.fixture
def localhost_users_spec_path():
  test_dir = Path(__file__).resolve().parent.parent.parent.parent
  return test_dir / "mock_data" / "localhost-users-optional-query.yaml"


class TestSqlLike:
  def test_percent_wildcard_prefix(self):
    assert sql_like("/api/v2/pets", "%/v2/pets")

  def test_no_match(self):
    assert not sql_like("/v2/cats", "%/v2/pets")


class TestSearchOpenApiEndpoint:
  def test_returns_matching_endpoint(self, petstore_expanded_path):
    ep = search_open_api_endpoint(
      str(petstore_expanded_path),
      "GET",
      "https://petstore.swagger.io/v2/pets",
    )
    assert ep is not None
    assert ep["method"] == "GET"
    assert ep["id"] == 1
    assert ep["match_pattern"] == "/v2/pets"

  def test_returns_none_when_no_match(self, petstore_expanded_path):
    assert (
      search_open_api_endpoint(
        str(petstore_expanded_path),
        "GET",
        "https://petstore.swagger.io/v2/unknown",
      )
      is None
    )

  def test_lazy_load_parses_spec_once(self, petstore_expanded_path):
    with patch(
      "stoobly_agent.app.proxy.mock.search_open_api_endpoint.load_openapi_endpoints_from_file",
      wraps=load_openapi_endpoints_from_file,
    ) as load:
      search_open_api_endpoint(
        str(petstore_expanded_path),
        "GET",
        "https://petstore.swagger.io/v2/pets",
      )
      search_open_api_endpoint(
        str(petstore_expanded_path),
        "POST",
        "https://petstore.swagger.io/v2/pets",
      )
      assert load.call_count == 1

  def test_inject_search_open_api_endpoint_delegates(self, petstore_expanded_path, monkeypatch):
    monkeypatch.setenv(env_vars.AGENT_OPENAPI_SPECIFICATION_PATH, str(petstore_expanded_path))
    settings = Settings.instance()
    inject = inject_search_open_api_endpoint(InterceptSettings(settings))
    ep = inject("GET", "https://petstore.swagger.io/v2/pets")
    assert ep is not None
    assert ep["method"] == "GET"

  def test_inject_returns_none_when_openapi_spec_path_unset(self, monkeypatch):
    monkeypatch.delenv(env_vars.AGENT_OPENAPI_SPECIFICATION_PATH, raising=False)
    settings = Settings.instance()
    inject = inject_search_open_api_endpoint(InterceptSettings(settings))
    assert inject("GET", "https://petstore.swagger.io/v2/pets") is None

  def test_matches_when_server_netloc_includes_port_but_request_url_omits_explicit_port(
    self, localhost_users_spec_path
  ):
    """Adapter host is 'localhost:80'; http://localhost/... uses implicit port 80."""
    ep = search_open_api_endpoint(
      str(localhost_users_spec_path),
      "GET",
      "http://localhost/users?b=1&a=4",
    )
    assert ep is not None
    assert ep["method"] == "GET"
    assert ep["match_pattern"] == "/users"

  def test_ignored_components_matches_ignoreable_optional_query_params(
    self, localhost_users_spec_path
  ):
    """Optional query params are ignored per Ignoreable#ignored? (OpenAPI: required: false)."""
    ep = search_open_api_endpoint(
      str(localhost_users_spec_path),
      "GET",
      "http://localhost/users",
    )
    assert ep is not None
    ig = ep.get("ignored_components") or []
    names_types = {(c["name"], c["type"], c.get("query")) for c in ig}
    assert ("a", COMPONENT_TYPES["QUERY_PARAM"], "a") in names_types
    assert ("b", COMPONENT_TYPES["QUERY_PARAM"], "b") in names_types

  def test_build_ignored_components_from_cached_endpoint_without_side_effect(
    self, localhost_users_spec_path
  ):
    eps = load_openapi_endpoints_from_file(str(localhost_users_spec_path))
    assert eps
    ig = build_ignored_components_from_openapi_endpoint(eps[0])
    assert len(ig) == 2
    assert eps[0].get("ignored_components") is None
