from mitmproxy.http import Request as MitmproxyRequest, Response as MitmproxyResponse
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.mock.hashed_request_decorator import HashedRequestDecorator
from stoobly_agent.app.proxy.mock.request_hasher import RequestHasher

class ORMRequestBuilder():
  def columns_from_mitmproxy_request(self, request: MitmproxyRequest):
    request_facade = MitmproxyRequestFacade(request)
    hashed_request = HashedRequestDecorator(request_facade)

    return {
      'body_params_hash': hashed_request.body_params_hash(),
      'body_text_hash': hashed_request.body_text_hash(),
      'headers_hash': hashed_request.headers_hash(),
      'host': request.host,
      'http_version':self.__http_version(request.http_version),
      'method': request.method,
      'password': request_facade.password,
      'path': request_facade.path,
      'port': request.port,
      'query': request_facade.query_string,
      'query_params_hash': hashed_request.query_params_hash(),
      'scheme': request.scheme,
      'user': request_facade.username,
    }

  def columns_from_mitmproxy_response(self, response: MitmproxyResponse):
    return {
      'response_hash': RequestHasher.instance().hash_text(response.content),
      'response_headers_hash': RequestHasher.instance().hash_params(response.headers)
    }

  def __http_version(self, http_version: str):
    if not isinstance(http_version, str):
      return http_version
    _version = http_version.split('/')[1]
    return float(_version)