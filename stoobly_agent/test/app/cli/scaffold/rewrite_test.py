from types import SimpleNamespace

from stoobly_agent.app.cli.scaffold.rewrite import apply_upstream_url_rewrite
import stoobly_agent.app.cli.scaffold.rewrite as rewrite_module


def _settings_with_project_id(project_id: str = "project-id"):
  return SimpleNamespace(
    proxy=SimpleNamespace(
      intercept=SimpleNamespace(
        project_key=f"org/{project_id}"
      )
    )
  )


def _service_config(**overrides):
  config = SimpleNamespace(
    url="https://api.example.test",
    local=False,
    hostname="api.example.test",
    port=443,
    scheme="https",
    upstream_hostname="upstream.example.test",
    upstream_port=8443,
    upstream_scheme="https",
  )

  for key, value in overrides.items():
    setattr(config, key, value)

  return config


def test_apply_upstream_url_rewrite_skips_when_service_url_missing(monkeypatch):
  called = []
  monkeypatch.setattr(rewrite_module.Settings, "instance", lambda: _settings_with_project_id())
  monkeypatch.setattr(rewrite_module, "set_rewrite_rule", lambda *args, **kwargs: called.append((args, kwargs)))

  service_config = _service_config(url=None)
  apply_upstream_url_rewrite(service_config)

  assert called == []


def test_apply_upstream_url_rewrite_applies_when_upstream_differs(monkeypatch):
  called = []
  monkeypatch.setattr(rewrite_module.Settings, "instance", lambda: _settings_with_project_id())
  monkeypatch.setattr(rewrite_module, "set_rewrite_rule", lambda *args, **kwargs: called.append((args, kwargs)))

  service_config = _service_config()
  apply_upstream_url_rewrite(service_config)

  assert len(called) == 1


def test_apply_upstream_url_rewrite_skips_when_upstream_matches_service(monkeypatch):
  called = []
  monkeypatch.setattr(rewrite_module.Settings, "instance", lambda: _settings_with_project_id())
  monkeypatch.setattr(rewrite_module, "set_rewrite_rule", lambda *args, **kwargs: called.append((args, kwargs)))

  service_config = _service_config(
    upstream_hostname="api.example.test",
    upstream_port=443,
    upstream_scheme="https",
  )
  apply_upstream_url_rewrite(service_config)

  assert called == []
