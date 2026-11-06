import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID
from stoobly_agent.lib.api.keys.request_key import RequestKey
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.test.test_helper import reset


@pytest.fixture(scope='module')
def runner():
  return CliRunner()


@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()


class TestExport:

  @pytest.fixture(autouse=True, scope='class')
  def created_request(self, runner: CliRunner):
    result = runner.invoke(request, ['create', 'https://example.com/api/pets'])
    assert result.exit_code == 0
    return Request.last()

  def test_it_exports_gor_to_file(self, runner: CliRunner, created_request: Request, tmp_path):
    output_path = tmp_path / 'request.gor'
    result = runner.invoke(
      request,
      ['export', '--format', 'gor', '--output', str(output_path), created_request.key()],
    )
    assert result.exit_code == 0, result.output
    assert output_path.read_bytes() == JoinedRequestStringAdapter(created_request).adapt()

  def test_it_errors_when_request_missing(self, runner: CliRunner, tmp_path):
    output_path = tmp_path / 'missing.gor'
    missing_key = RequestKey.encode(LOCAL_PROJECT_ID, '00000000-0000-0000-0000-000000000000')
    result = runner.invoke(
      request,
      ['export', '--output', str(output_path), missing_key],
    )
    assert result.exit_code == 1
    assert 'Could not find request' in result.output
    assert not output_path.exists()

  def test_it_errors_when_response_missing(self, runner: CliRunner, tmp_path):
    create_result = runner.invoke(request, ['create', 'https://example.com/api/no-response'])
    assert create_result.exit_code == 0
    created = Request.last()
    created.response.delete()

    output_path = tmp_path / 'no-response.gor'
    result = runner.invoke(
      request,
      ['export', '--format', 'gor', '--output', str(output_path), created.key()],
    )
    assert result.exit_code == 1
    assert 'Request has no response' in result.output
    assert not output_path.exists()

  def test_it_errors_when_request_soft_deleted(self, runner: CliRunner, tmp_path):
    create_result = runner.invoke(request, ['create', 'https://example.com/api/trashed'])
    assert create_result.exit_code == 0
    created = Request.last()
    created.update({'is_deleted': True})

    output_path = tmp_path / 'trashed.gor'
    result = runner.invoke(
      request,
      ['export', '--format', 'gor', '--output', str(output_path), created.key()],
    )
    assert result.exit_code == 1
    assert 'Could not find request' in result.output
    assert not output_path.exists()
