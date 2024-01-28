import copy
import pdb

from dataclasses import dataclass
from typing import List
from urllib.parse import urlencode
from urllib.parse import urlparse

from stoobly_agent.app.models.adapters.orm import (
  OrmRequestAdapterFactory,
  OrmResponseAdapterFactory,
)
from stoobly_agent.app.models.factories.resource.local_db.request_adapter import (
  LocalDBRequestAdapter,
)
from stoobly_agent.app.proxy.replay.body_parser_service import (
  decode_response,
  encode_response,
)
from stoobly_agent.app.proxy.test.context import TestContext
from stoobly_agent.app.proxy.test.helpers.endpoint_facade import EndpointFacade
from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import (
  RequestComponentNamesFacade,
)
from stoobly_agent.app.proxy.test.matchers.contract import matches as contract_matches
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.config.constants.lifecycle_hooks import (
  ON_LENGTH_MATCH_ERROR,
  ON_PARAM_NAME_EXISTS_ERROR,
  ON_PARAM_NAME_MISSING_ERROR,
  ON_TYPE_MATCH_ERROR,
  ON_VALID_TYPE_ERROR,
)
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse
from stoobly_agent.lib.api.interfaces.requests import RequestShowResponse
from stoobly_agent.lib.orm.request import Request

from .request_synchronize_handler import RequestSynchronizeHandler

@dataclass
class SynchronizeRequestService():
  local_db_request_adapter: LocalDBRequestAdapter

  def synchronize_request(self, request: Request, endpoint: EndpointShowResponse, lifecycle_hooks = {}):
    facade = EndpointFacade(None, -1).with_show_response(endpoint)
    mitmproxy_request = OrmRequestAdapterFactory(request).mitmproxy_request()

    # Query Params
    query_param_names_facade = facade.query_param_names
    handler = RequestSynchronizeHandler(request_component.QUERY_PARAM, lifecycle_hooks)
    query_params = mitmproxy_request.query
    result = self.synchronize_component(query_params, query_param_names_facade, handler)
    success = result[0]
    if success:
      self.__remove_bad_params(query_params)
      updated_url = self.__encode_query_params(request.url, request.path, query_params)
      params: RequestShowResponse = {}
      params['url'] = updated_url

      self.local_db_request_adapter.update(request.id, **params)

    # Body
    headers = mitmproxy_request.headers
    body_params = decode_response(mitmproxy_request.content, headers.get('content-type'))
    endpoint_body_params = endpoint.get('body_param_names')

    if body_params or endpoint_body_params:
      body_param_names_facade = facade.body_param_names
      handler = RequestSynchronizeHandler(request_component.BODY_PARAM, lifecycle_hooks)
      result = self.synchronize_component(body_params, body_param_names_facade, handler)

      success = result[0]
      if success:
        encoded_response = encode_response(body_params, headers.get('content-type'))
        params: RequestShowResponse = {}
        params['body'] = encoded_response

        self.local_db_request_adapter.update(request.id, **params)

    # Response
    python_response = OrmResponseAdapterFactory(request.response).python_response()
    headers = python_response.headers
    response_params = decode_response(python_response.content, headers.get('content-type'))
    response_param_names_facade = facade.response_param_names
    valid = self.validate_component(response_param_names_facade, response_params)[0]

    if not valid:
      self.__synchronize_response(endpoint)

  def synchronize_component(self, component, facade: RequestComponentNamesFacade, handler: RequestSynchronizeHandler):
    lifecycle_hooks = self.__lifecycle_hooks(handler)
    context = self.__context(lifecycle_hooks)

    return contract_matches(context, facade, component, strict=True)

  def validate_component(self, facade: RequestComponentNamesFacade, component):
    context = self.__context({})

    return contract_matches(context, facade, component)

  class TestContextMock(TestContext):
    def __init__(self, lifecycle_hooks: dict):
      self.__lifecycle_hooks = lifecycle_hooks

    @property
    def lifecycle_hooks(self):
      return self.__lifecycle_hooks

    @lifecycle_hooks.setter
    def lifecycle_hooks(self, v):
      self.__lifecycle_hooks = v

  def __context(self, lifecycle_hooks) -> TestContextMock:
    return self.TestContextMock(lifecycle_hooks)

  def __lifecycle_hooks(self, handler: RequestSynchronizeHandler):
    hooks = {}

    hooks[ON_LENGTH_MATCH_ERROR] = handler.handle_length_match_error
    hooks[ON_PARAM_NAME_EXISTS_ERROR] = handler.handle_param_name_exists
    hooks[ON_PARAM_NAME_MISSING_ERROR] = handler.handle_param_name_missing
    hooks[ON_TYPE_MATCH_ERROR] = handler.handle_type_match_error
    hooks[ON_VALID_TYPE_ERROR] = handler.handle_valid_type_error

    return hooks

  def __synchronize_response(self, endpoint: EndpointShowResponse):
    # For each request / scenario, replay and overwrite
    pass

  def __encode_query_params(self, original_url: str, path: str, query_params) -> str:
    query_tuples = []
    for key in query_params:
      for value in query_params.get_all(key):
        if not isinstance(value, list):
          query_tuples.append((key, value))
        else:
          for v in value:
            query_tuples.append((key, v))

    parsed_url = urlparse(original_url)
    url = parsed_url._replace(path=path, query=urlencode(query_tuples))
    return url.geturl()

  def __remove_bad_params(self, query_params) -> None:
    query_params_clone = copy.deepcopy(query_params)
    for key in query_params_clone:
      for value in query_params_clone.get_all(key):
        if value == 'None':
          del query_params[key]

  def __find_required_params(self, endpoint: EndpointShowResponse, param_name: str) -> List:
    result = []

    params = endpoint.get(param_name)
    if not params:
      return result

    for param in params:
      if param['is_required'] == True:
        result.append(param)

    return result

