import pdb
import requests

from stoobly_agent.app.models.types import ReplayedResponseIndexQueryParams
from stoobly_agent.lib.api.interfaces.requests import RequestShowResponse
from stoobly_agent.lib.orm.replayed_response import ReplayedResponse
from stoobly_agent.lib.orm.transformers.orm_to_requests_response_transformer import ORMToRequestsResponseTransformer
from stoobly_agent.lib.orm.transformers.orm_to_stoobly_request_transformer import ORMToStooblyRequestTransformer
from stoobly_agent.lib.orm.utils.response_parse_handler import Response

class LocalDBReplayedResponseAdapter():
  __replayed_response_orm = None

  def __init__(self, replayed_response_orm: ReplayedResponse.__class__ = ReplayedResponse):
    self.__replayed_response_orm = replayed_response_orm

  def create(self, **body_params):
    replayed_response = ReplayedResponse.create(**body_params)
    return self.__transform_replayed_response(replayed_response)

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

  def activate(self, replayed_response_id: int):
    replayed_response: ReplayedResponse = self.__replayed_response_orm.find(replayed_response_id)

    if not replayed_response:
      return None

    request = replayed_response.request
    response = request.response

    _replayed_response = ReplayedResponse.create(
      latency=request.latency,
      raw=response.raw,
      request_id=request.id,
      status=request.status,
    )
    _replayed_response.created_at = request.created_at
    _replayed_response.save()

    request.created_at = replayed_response.created_at
    request.latency = replayed_response.latency
    request.status = replayed_response.status
    request.save()

    response.created_at = replayed_response.created_at
    response.raw = replayed_response.raw
    response.save()

    replayed_response.delete()

    return self.__transform_replayed_response(_replayed_response)
    
  def __transform_replayed_response(self, replayed_response: ReplayedResponse):
    res = replayed_response.to_dict()
    res.pop('raw')
    return res