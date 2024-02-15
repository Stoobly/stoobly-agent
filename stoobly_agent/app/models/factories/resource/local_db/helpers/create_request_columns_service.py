import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.app.proxy.record.joined_request import JoinedRequest
from stoobly_agent.lib.orm.types.request_columns import RequestColumns
from stoobly_agent.lib.orm.types.response_columns import ResponseColumns

from ..orm_request_builder import ORMRequestBuilder

def build_request_columns(flow: MitmproxyHTTPFlow, joined_request: JoinedRequest, **params):
  builder = ORMRequestBuilder()
  request_columns = builder.columns_from_mitmproxy_request(flow.request)
  response_columns = builder.columns_from_mitmproxy_response(flow.response)

  request_columns: RequestColumns = {
    **request_columns,
    **response_columns,
    'control': joined_request.request_string.control,
    'latency': joined_request.response_string.latency,
    'raw': joined_request.request_string.get(),
    'status': flow.response.status_code, 
  }

  return { 
    **request_columns, 
    **params, 
    **{ 'uuid': params.get('uuid') or joined_request.request_string.request_id.strip() } 
  }

def build_response_columns(flow: MitmproxyHTTPFlow, joined_request: JoinedRequest):
  response_columns: ResponseColumns = {
    'control': joined_request.response_string.control,
    'http_version': __http_version(flow.response.http_version),
    'raw': joined_request.response_string.get(),
  }

  return response_columns

def __http_version(http_version: str):
  if not isinstance(http_version, str):
    return http_version
  _version = http_version.split('/')[1]
  return float(_version)