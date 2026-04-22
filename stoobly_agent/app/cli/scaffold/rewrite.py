from stoobly_agent.app.cli.helpers.set_rewrite_rule_service import set_rewrite_rule
from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_TEST_TYPE
from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import method, mode
from stoobly_agent.lib.api.keys.project_key import ProjectKey

def apply_upstream_url_rewrite(service_config: ServiceConfig) -> None:
  """
  If effective upstream hostname, port, or scheme differs from the service's public
  hostname, port, or scheme, persist a replay-mode URL rewrite rule mapping the service URL to upstream.
  """
  if not service_config.url:
    return

  upstream_hostname = service_config.upstream_hostname
  upstream_port = service_config.upstream_port
  upstream_scheme = service_config.upstream_scheme

  if (
    upstream_hostname != service_config.hostname
    or upstream_port != service_config.port
    or upstream_scheme != service_config.scheme
  ):
    settings: Settings = Settings.instance()
    project_key = ProjectKey(settings.proxy.intercept.project_key)
    set_rewrite_rule(
      project_key.id,
      pattern=f'{service_config.url}/?.*?',
      method=[method.GET, method.PATCH, method.POST, method.PUT, method.DELETE, method.OPTIONS],
      mode=[mode.REPLAY],
      hostname=upstream_hostname,
      port=upstream_port,
      scheme=upstream_scheme,
    )


