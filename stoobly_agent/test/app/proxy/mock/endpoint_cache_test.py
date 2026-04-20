from types import SimpleNamespace
from unittest.mock import patch

import pytest

from stoobly_agent.app.proxy.mock import endpoint_cache as endpoint_cache_module
from stoobly_agent.lib.api.keys.project_key import ProjectKey


@pytest.fixture(autouse=True)
def reset_endpoint_cache_singleton():
  original = endpoint_cache_module.EndpointCache._instance
  endpoint_cache_module.EndpointCache._instance = None
  yield
  endpoint_cache_module.EndpointCache._instance = None
  endpoint_cache_module.EndpointCache._instance = original


def _make_settings(intercept_project_key=None, remote_project_key=None):
  return SimpleNamespace(
    cli=SimpleNamespace(features=SimpleNamespace(remote=True)),
    proxy=SimpleNamespace(intercept=SimpleNamespace(project_key=intercept_project_key)),
    remote=SimpleNamespace(
      project_key=remote_project_key,
      api_url="https://example.invalid",
      api_key="secret",
    ),
  )


class TestEndpointCache:
  def test_instance_prefetches_intercept_and_remote_project_keys(self):
    intercept_key = ProjectKey.encode(101, 1).decode()
    remote_key = ProjectKey.encode(202, 1).decode()
    settings = _make_settings(intercept_project_key=intercept_key, remote_project_key=remote_key)

    with patch.object(endpoint_cache_module, "remote_feature", return_value=True), patch.object(
      endpoint_cache_module.Settings, "instance", return_value=settings
    ), patch.object(endpoint_cache_module.EndpointCache, "with_project") as with_project:
      endpoint_cache_module.EndpointCache.instance()

      assert with_project.call_count == 2
      with_project.assert_any_call("101")
      with_project.assert_any_call("202")

  def test_with_project_is_idempotent_for_same_project_key(self):
    settings = _make_settings()
    project_key = ProjectKey.encode(303, 1).decode()
    remote_endpoint = [{"id": "1", "method": "GET", "host": "api.example.com", "port": "443", "match_pattern": "/project"}]

    with patch.object(endpoint_cache_module, "remote_feature", return_value=True), patch.object(
      endpoint_cache_module.Settings, "instance", return_value=settings
    ), patch.object(endpoint_cache_module.EndpointCache, "_fetch_project_endpoints", return_value=remote_endpoint) as fetch:
      cache = endpoint_cache_module.EndpointCache()

      cache.with_project(project_key)
      cache.with_project(project_key)

      assert fetch.call_count == 1
      assert cache.show("1") is not None

  def test_with_openapi_specification_is_idempotent_for_same_path(self):
    openapi_endpoint = [{"id": "100", "method": "GET", "host": "api.example.com", "port": "443", "match_pattern": "/openapi"}]

    with patch.object(
      endpoint_cache_module, "load_openapi_endpoints_from_file", return_value=openapi_endpoint
    ) as load_openapi:
      cache = endpoint_cache_module.EndpointCache()

      cache.with_openapi_specification("./tmp/../tmp/spec.yaml")
      cache.with_openapi_specification("tmp/spec.yaml")

      assert load_openapi.call_count == 1
      assert cache.show("100") is not None

  def test_search_uses_all_loaded_data_sources(self):
    settings = _make_settings()
    project_key = ProjectKey.encode(404, 1).decode()
    openapi_endpoint = [{"id": "100", "method": "GET", "host": "api.example.com", "port": "443", "match_pattern": "/openapi"}]
    remote_endpoint = [{"id": "200", "method": "GET", "host": "api.example.com", "port": "443", "match_pattern": "/project"}]

    with patch.object(endpoint_cache_module, "remote_feature", return_value=True), patch.object(
      endpoint_cache_module.Settings, "instance", return_value=settings
    ), patch.object(
      endpoint_cache_module, "load_openapi_endpoints_from_file", return_value=openapi_endpoint
    ), patch.object(endpoint_cache_module.EndpointCache, "_fetch_project_endpoints", return_value=remote_endpoint):
      cache = endpoint_cache_module.EndpointCache()
      cache.with_openapi_specification("tmp/spec.yaml")
      cache.with_project(project_key)

      assert cache.search("GET", "https://api.example.com/openapi")["id"] == "100"
      assert cache.search("GET", "https://api.example.com/project")["id"] == "200"

  def test_latest_merge_wins_when_openapi_and_project_share_endpoint_id(self):
    settings = _make_settings()
    project_key = ProjectKey.encode(505, 1).decode()
    openapi_endpoint = [{"id": "777", "method": "GET", "host": "api.example.com", "port": "443", "match_pattern": "/items"}]
    remote_endpoint = [{"id": "777", "method": "GET", "host": "api.example.com", "port": "443", "match_pattern": "/items"}]

    with patch.object(endpoint_cache_module, "remote_feature", return_value=True), patch.object(
      endpoint_cache_module.Settings, "instance", return_value=settings
    ), patch.object(
      endpoint_cache_module, "load_openapi_endpoints_from_file", return_value=openapi_endpoint
    ), patch.object(endpoint_cache_module.EndpointCache, "_fetch_project_endpoints", return_value=remote_endpoint):
      cache = endpoint_cache_module.EndpointCache()
      cache.with_openapi_specification("tmp/spec.yaml")
      cache.with_project(project_key)

      # Colliding ids overwrite in the shared endpoint-id map; latest merge is returned.
      assert cache.search("GET", "https://api.example.com/items")["id"] == "777"
      assert cache.show("777")["id"] == "777"
      assert "ignored_components" not in cache.show("777")

  def test_search_prefers_latest_merge_for_same_contract_with_different_ids(self):
    settings = _make_settings()
    project_key = ProjectKey.encode(606, 1).decode()
    openapi_endpoint = [{"id": "openapi-1", "method": "GET", "host": "api.example.com", "port": "443", "match_pattern": "/items"}]
    remote_endpoint = [{"id": "project-1", "method": "GET", "host": "api.example.com", "port": "443", "match_pattern": "/items"}]

    with patch.object(endpoint_cache_module, "remote_feature", return_value=True), patch.object(
      endpoint_cache_module.Settings, "instance", return_value=settings
    ), patch.object(
      endpoint_cache_module, "load_openapi_endpoints_from_file", return_value=openapi_endpoint
    ), patch.object(endpoint_cache_module.EndpointCache, "_fetch_project_endpoints", return_value=remote_endpoint):
      cache = endpoint_cache_module.EndpointCache()

      cache.with_openapi_specification("tmp/spec.yaml")
      cache.with_project(project_key)
      assert cache.search("GET", "https://api.example.com/items")["id"] == "project-1"

      cache.clear_cache()
      cache.with_project(project_key)
      cache.with_openapi_specification("tmp/spec.yaml")
      assert cache.search("GET", "https://api.example.com/items")["id"] == "openapi-1"
