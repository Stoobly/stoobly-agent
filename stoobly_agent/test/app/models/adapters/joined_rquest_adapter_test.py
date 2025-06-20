import pytest

from stoobly_agent.app.models.adapters.joined_request_adapter import RequestStringCLRF, JoinedRequestAdapter

class TestJoindRequestStringAdapter():

  @pytest.fixture(scope='class', autouse=True)
  def corrupted_raw_string(self):
    toks = [
      b"control",
      b"header1",
      b"header2",
      b'',
      b'body1',
      b'body2'
    ]
    return b"\n".join(toks)

  @pytest.fixture(scope='class', autouse=True)
  def repaired_toks(self, corrupted_raw_string: bytes):
    # [b'control', b'header1', b'header2', b'', b'body1\nbody2']
    return JoinedRequestAdapter.repaired_string_toks(corrupted_raw_string, RequestStringCLRF)

  def test_control(self, repaired_toks: list):
    assert repaired_toks[0] == b'control'

  def test_header1(self, repaired_toks: list):
    assert repaired_toks[1] == b'header1'

  def test_header2(self, repaired_toks: list):
    assert repaired_toks[2] == b'header2'

  def test_clrf(self, repaired_toks: list):
    assert repaired_toks[3] == b''

  def test_body(self, repaired_toks: list):
    assert repaired_toks[4] == b'body1\nbody2'
    