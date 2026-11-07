from unittest.mock import MagicMock

from stoobly_agent.app.cli.scaffold.docker.workflow.reverse_proxy_decorator import ReverseProxyDecorator


class TestReverseProxyDecorator:
  def test_includes_public_and_fixtures_paths(self):
    workflow_builder = MagicMock()
    workflow_builder.config.upstream_hostname = 'example.com'
    workflow_builder.config.hostname = 'example.com'
    workflow_builder.config.scheme = 'http'
    workflow_builder.config.port = 80
    workflow_builder.config.upstream_scheme = 'http'
    workflow_builder.config.upstream_port = 80
    workflow_builder.config.openapi_specification = False
    workflow_builder.proxy = 'proxy'
    workflow_builder.services = {'proxy': {'image': 'stoobly'}}

    service_builder = MagicMock()
    service_builder.config = workflow_builder.config
    workflow_builder.service_builder = service_builder

    decorator = ReverseProxyDecorator(workflow_builder)
    decorator.decorate()

    command = workflow_builder.services['proxy']['command']
    assert '--public-dir-path' in command
    assert 'public' in command
    assert '--response-fixtures-path' in command
    assert 'fixtures.yml' in command
