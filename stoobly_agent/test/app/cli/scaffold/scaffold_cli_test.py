import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.test.test_helper import reset


@pytest.fixture(scope='module', autouse=True)
def settings():
  return reset()


@pytest.fixture(scope='module')
def runner():
  return CliRunner()


class TestScaffoldAppCreateValidation:
  def test_copy_on_workflow_up_requires_docker_runtime(self, runner: CliRunner, tmp_path):
    docker_socket_path = tmp_path / 'docker.sock'
    docker_socket_path.touch()

    result = runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(tmp_path),
      '--copy-on-workflow-up',
      '--docker-socket-path', str(docker_socket_path),
      '--runtime', 'local',
      'test-app',
    ])

    assert result.exit_code == 1
    assert '--copy-on-workflow-up is only supported for docker runtime.' in result.output
