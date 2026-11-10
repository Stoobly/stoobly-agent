import base64

from stoobly_agent.app.proxy.test.helpers.expected_response_codec import (
  FORMAT_BASE64,
  FORMAT_JSON,
  FORMAT_TEXT,
  decode_expected_response,
  encode_expected_response,
)


class TestExpectedResponseCodec:
  def test_encodes_json(self):
    envelope = encode_expected_response({'a': 1})
    assert envelope == {'format': FORMAT_JSON, 'data': {'a': 1}}
    assert decode_expected_response(envelope) == {'a': 1}

  def test_encodes_text(self):
    envelope = encode_expected_response('hello')
    assert envelope == {'format': FORMAT_TEXT, 'data': 'hello'}
    assert decode_expected_response(envelope) == 'hello'

  def test_encodes_utf8_bytes_as_text(self):
    envelope = encode_expected_response(b'hello')
    assert envelope == {'format': FORMAT_TEXT, 'data': 'hello'}
    assert decode_expected_response(envelope) == 'hello'

  def test_encodes_binary_bytes_as_base64(self):
    raw = b'\xff\xfe\xfd'
    envelope = encode_expected_response(raw)
    assert envelope['format'] == FORMAT_BASE64
    assert envelope['data'] == base64.b64encode(raw).decode('ascii')
    assert decode_expected_response(envelope) == raw

  def test_encodes_none_as_empty_text(self):
    envelope = encode_expected_response(None)
    assert envelope == {'format': FORMAT_TEXT, 'data': ''}
    assert decode_expected_response(envelope) == ''
