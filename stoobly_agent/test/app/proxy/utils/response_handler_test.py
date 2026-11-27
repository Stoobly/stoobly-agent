from types import SimpleNamespace

import requests
from mitmproxy.http import Request as MitmproxyRequest
from urllib3._collections import HTTPHeaderDict

from stoobly_agent.app.proxy.utils.response_handler import (
  apply_response,
  disable_transfer_encoding_chunked,
)


def _requests_response(status: int, body: bytes, headers: dict) -> requests.Response:
  response = requests.Response()
  response.status_code = status
  response._content = body
  response.headers = HTTPHeaderDict(headers)
  return response


def _flow():
  request = MitmproxyRequest.make('GET', 'http://example.test/sse')
  return SimpleNamespace(request=request, response=None)


class TestDisableTransferEncodingChunked:

  def test_strips_chunked_and_sets_content_length(self):
    from mitmproxy.http import Response as MitmproxyResponse

    response = MitmproxyResponse.make(
      200,
      b'data: hello\n\n',
      {
        'Content-Type': 'text/event-stream',
        'Transfer-Encoding': 'chunked',
      },
    )

    disable_transfer_encoding_chunked(response)

    assert 'Transfer-Encoding' not in response.headers
    assert response.headers['Content-Length'] == str(len(b'data: hello\n\n'))

  def test_keeps_non_chunked_transfer_encoding(self):
    from mitmproxy.http import Response as MitmproxyResponse

    response = MitmproxyResponse.make(
      200,
      b'body',
      {'Transfer-Encoding': 'gzip, chunked'},
    )

    disable_transfer_encoding_chunked(response)

    assert response.headers.get_all('Transfer-Encoding') == ['gzip']
    assert response.headers['Content-Length'] == '4'


class TestApplyResponse:

  def test_strips_transfer_encoding_chunked_on_egress(self):
    flow = _flow()
    res = _requests_response(
      200,
      b'data: hello\n\n',
      {
        'Content-Type': 'text/event-stream',
        'Transfer-Encoding': 'chunked',
        'Content-Length': str(len(b'data: hello\n\n')),
      },
    )

    apply_response(flow, res)

    assert 'Transfer-Encoding' not in flow.response.headers
    assert flow.response.headers['Content-Length'] == str(len(b'data: hello\n\n'))
    assert flow.response.content == b'data: hello\n\n'
