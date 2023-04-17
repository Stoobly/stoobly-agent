from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow, Request as MitmproxyRequest
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.mock.hashed_request_decorator import HashedRequestDecorator

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
      'path': request_facade.path,
      'port': request.port,
      'query': request_facade.query_string,
      'query_params_hash': hashed_request.query_params_hash(),
      'scheme': request.scheme,
    }

  def create(self, **columns):
    pass

  def update(self):
    pass

  def __http_version(self, http_version: str):
    if not isinstance(http_version, str):
      return http_version
    _version = http_version.split('/')[1]
    return float(_version)