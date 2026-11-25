from stoobly_agent.app.models.adapters.snapshot import SnapshotAdapterFactory
from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER

REQ_TS_NS = 1795066190943834368
RES_TS_NS = 1795066190944042000


def _entry():
  return {
    'method': 'GET',
    'url': 'https://example.com/api',
    'http_version': '1.1',
    'timestamp': REQ_TS_NS,
    'headers': 'Host: example.com',
    'response': {
      'status': 200,
      'latency': 42,
      'http_version': '1.1',
      'timestamp': RES_TS_NS,
      'headers': 'Content-Length: 0',
    },
  }


class TestSnapshotAdapterFactory:
  def test_joined_request(self):
    joined = SnapshotAdapterFactory(_entry(), uuid='req-id').joined_request()
    assert REQUEST_DELIMITTER in joined
    assert joined.startswith(f'1 req-id {REQ_TS_NS}\r\n'.encode())
    assert f'2 req-id {RES_TS_NS} 42\r\n'.encode() in joined
    assert b'GET https://example.com/api HTTP/1.1\r\n' in joined
    assert b'HTTP/1.1 200\r\n' in joined

  def test_request_raw(self):
    raw = SnapshotAdapterFactory(_entry(), uuid='req-id').request().raw_request()
    assert raw.startswith(f'1 req-id {REQ_TS_NS}\r\n'.encode())
    assert b'Host: example.com\r\n' in raw

  def test_response_raw(self):
    raw = SnapshotAdapterFactory(_entry(), uuid='req-id').response().raw_response()
    assert raw.startswith(f'2 req-id {RES_TS_NS} 42\r\n'.encode())
    assert b'Content-Length: 0\r\n' in raw
