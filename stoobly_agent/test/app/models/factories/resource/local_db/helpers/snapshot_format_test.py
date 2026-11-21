import os

import pytest

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_slug import (
  build_request_slug,
  parse_request_relative_path,
  sanitize_scenario_filename,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_format import (
  FORMAT_NONE,
  FORMAT_V1,
  FORMAT_V2,
  detect_snapshot_format,
  resolve_write_format,
)
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True)
def settings():
  return reset()


class TestRequestSlug:
  def test_method_and_path(self):
    assert build_request_slug('GET', '/api/users/1') == 'GET-api-users-1'

  def test_root_path(self):
    assert build_request_slug('POST', '/') == 'POST'

  def test_relative_path_parse(self):
    assert parse_request_relative_path('GET-api-users/abc.http') == ('GET-api-users', 'abc')

  def test_sanitize_scenario_name(self):
    assert sanitize_scenario_filename('My Scenario!') == 'My-Scenario'


class TestSnapshotFormatDetect:
  def test_none_defaults_write_to_v2(self):
    data_dir = DataDir.instance()
    assert detect_snapshot_format(data_dir) == FORMAT_NONE
    assert resolve_write_format(data_dir) == FORMAT_V2

  def test_detects_v2_http(self):
    data_dir = DataDir.instance()
    requests_dir = data_dir.snapshots_requests_dir_path
    slug_dir = os.path.join(requests_dir, 'GET-api')
    os.makedirs(slug_dir, exist_ok=True)
    with open(os.path.join(slug_dir, '11111111-1111-1111-1111-111111111111.http'), 'wb') as fp:
      fp.write(b'x')

    assert detect_snapshot_format(data_dir) == FORMAT_V2

  def test_detects_v1_shard(self):
    data_dir = DataDir.instance()
    requests_dir = data_dir.snapshots_requests_dir_path
    shard = os.path.join(requests_dir, 'ab')
    os.makedirs(shard, exist_ok=True)
    with open(os.path.join(shard, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'), 'wb') as fp:
      fp.write(b'x')

    assert detect_snapshot_format(data_dir) == FORMAT_V1
    assert resolve_write_format(data_dir) == FORMAT_V1
