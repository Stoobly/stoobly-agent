import pdb
import pytest

from stoobly_agent.app.proxy.replay.body_parser_service import decode_response, encode_response

@pytest.fixture
def multipart_string():
  return b"--ce560532019a77d83195f9e9873e16a1\r\nContent-Disposition: form-data; name=\"author\"\r\n\r\nJohn Smith\r\n--ce560532019a77d83195f9e9873e16a1\r\nContent-Disposition: form-data; name=\"file\"; filename=\"example2.txt\"\r\nContent-Type: text/plain\r\nExpires: 0\r\n\r\nHello World\r\n--ce560532019a77d83195f9e9873e16a1--\r\n"

@pytest.fixture
def content_type():
  return "multipart/form-data; boundary=ce560532019a77d83195f9e9873e16a1"

class TestMultipart():

  def test_decodes_response(self, multipart_string: bytes, content_type: str):
    multidict = decode_response(multipart_string, content_type)

    assert multidict.get('author') == 'John Smith'
    assert multidict.get('file') == 'Hello World'

  def test_encodes_response(self, content_type: str):
    expected_params = { 'author': 'John Smith', 'file': 'Hello World'}
    multipart_string = encode_response(expected_params, content_type)

    multidict = decode_response(multipart_string, content_type)
    for key in expected_params:
      assert multidict.get(key) == expected_params[key]
