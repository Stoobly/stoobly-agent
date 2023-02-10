import pdb
import requests

from stoobly_agent.lib.api.interfaces.requests import RequestShowResponse
from stoobly_agent.lib.orm.replayed_response import ReplayedResponse
from stoobly_agent.lib.orm.transformers.orm_to_requests_response_transformer import ORMToRequestsResponseTransformer
from stoobly_agent.lib.orm.transformers.orm_to_stoobly_request_transformer import ORMToStooblyRequestTransformer
from stoobly_agent.lib.orm.utils.response_parse_handler import Response

from ..types.replayed_response import ReplayedResponseIndexQueryParams

class LocalDBReplayedResponseAdapter():
  __replayed_response_orm = None

  def __init__(self, replayed_response_orm: ReplayedResponse.__class__ = ReplayedResponse):
    self.__replayed_response_orm = replayed_response_orm

  def index(self, **query_params: ReplayedResponseIndexQueryParams):
    request_id = int(query_params.get('request_id')) if query_params.get('request_id') else None
    page = int(query_params.get('page') or 0)
    size = int(query_params.get('size') or 20)
    sort_by = query_params.get('sort_by') or 'id'
    sort_order = query_params.get('sort_order') or 'desc'

    replayed_responses = self.__replayed_response_orm.where('request_id', request_id)

    total = replayed_responses.count()
    replayed_responses = replayed_responses.offset(page * size).limit(size).order_by(sort_by, sort_order).get()

    return {
      'list': list(map(lambda replayed_response: self.__transform_replayed_response(replayed_response), replayed_responses)),
      'total': total,
    }

  def destroy(self, replayed_response_id: int):
    replayed_response = self.__replayed_response_orm.find(replayed_response_id)

    if not replayed_response:
      return None

    replayed_response.delete()

  def mock(self, replayed_response_id: int) -> requests.Response:
    replayed_response = self.__replayed_response_orm.find(replayed_response_id)

    if not replayed_response:
      return None

    return ORMToRequestsResponseTransformer(replayed_response).transform()

  def raw(self, replayed_response_id: int) -> bytes:
    replayed_response = self.__replayed_response_orm.find(replayed_response_id)

    if not replayed_response:
      return None

    return replayed_response.raw

  def record(self, replayed_response_id: int) -> RequestShowResponse:
    replayed_response: ReplayedResponse = self.__replayed_response_orm.find(replayed_response_id)

    if not replayed_response:
      return None

    request = replayed_response.request

    new_request = request.replicate()
    new_request.status = replayed_response.status
    new_request.latency = replayed_response.latency
    new_request.save()

    replayed_response_dict = replayed_response.to_dict()
    replayed_response_dict['request_id'] = new_request.id
    replayed_response_dict.pop('status')
    replayed_response_dict.pop('latency')
    Response.create(replayed_response_dict)

    return ORMToStooblyRequestTransformer(new_request, {}).transform()
    
  def __transform_replayed_response(self, replayed_response: ReplayedResponse):
    res = replayed_response.to_dict()
    res.pop('raw')
    return res