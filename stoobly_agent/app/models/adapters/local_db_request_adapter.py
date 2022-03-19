import pdb
import requests

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow, HTTPRequest as MitmproxyRequest

from stoobly_agent.app.proxy.mock.hashed_request_decorator import HashedRequestDecorator
from stoobly_agent.app.proxy.mitmproxy.request_adapter import MitmproxyRequestAdapter

from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.types.request_create_params import RequestCreateParams
from stoobly_agent.lib.api.interfaces.requests_index_query_params import RequestsIndexQueryParams
from stoobly_agent.lib.api.interfaces.requests_index_response import RequestsIndexResponse
from stoobly_agent.lib.api.interfaces.request_show_response import RequestShowResponse

from .types.request_create_params import RequestCreateParams

class LocalDBRequestAdapter():
  __orm = None

  def __init__(self, orm: Request.__class__):
    self.__orm = orm

  def create(self, **params: RequestCreateParams) -> RequestShowResponse:
    flow: MitmproxyHTTPFlow = params['flow']
    request: MitmproxyRequest = flow.request
    hashed_request = HashedRequestDecorator(MitmproxyRequestAdapter(request))

    body_params: RequestCreateParams = {
      'body_params_hash': hashed_request.body_params_hash(),
      'body_text_hash': hashed_request.body_text_hash(),
      'headers_hash': hashed_request.headers_hash(),
      'host': request.host,
      'method': request.method,
      'path': request.path,
      'port': request.port,
      'query_params_hash': hashed_request.query_params_hash(),
      'scheme': request.scheme,
    }

    pdb.set_trace()
    request_record = self.__orm.create(
      raw=params.get('requests'),
      **body_params
    )

    return request_record.to_dict()

  def show(self, project_id: str, request_id: str, **query_params) -> RequestShowResponse:
    request = self.__orm.find_by(
      request_id=request_id,
      **query_params
    )

    return request.to_dict()

  def response(self, **query_params) -> requests.Response:
    request = self.__orm.find_by(query_params)
    _response = request.response 

    # Do parsing
    
    response = requests.Response()
    return response

  def index(self, project_id: int, query_params: RequestsIndexQueryParams) -> RequestsIndexResponse:
    page = query_params.get('page') or 0
    size = query_params.get('size') or 20

    requests = self.__orm.where(
      scenario_id=query_params.get('scenario_id')
    )

    total = requests.count()
    
    requests = requests.offset(page).limit(size).get()

    return {
      'list': requests.to_dict(),
      'total': total,
    }

