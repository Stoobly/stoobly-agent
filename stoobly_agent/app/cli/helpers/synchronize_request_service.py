from urllib.parse import parse_qs

from stoobly_agent.app.models.adapters.orm import OrmRequestAdapterFactory, OrmResponseAdapterFactory
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response, encode_response
from stoobly_agent.app.proxy.test.helpers.endpoint_facade import EndpointFacade
from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import RequestComponentNamesFacade
from stoobly_agent.app.proxy.test.matchers.contract import matches as contract_matches
from stoobly_agent.app.settings.constants import request_component, RequestComponent
from stoobly_agent.config.constants.lifecycle_hooks import ON_LENGTH_MATCH_ERROR, ON_PARAM_NAME_EXISTS_ERROR, ON_PARAM_NAME_MISSING_ERROR, ON_TYPE_MATCH_ERROR, ON_VALID_TYPE_ERROR
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse
from stoobly_agent.lib.orm.request import Request

from .request_synchronize_handler import RequestSynchronizeHandler

def synchronize_request(request: Request, endpoint: EndpointShowResponse, lifecycle_hooks = {}):
  facade = EndpointFacade(None, -1).with_show_response(endpoint)
  mitmproxy_request = OrmRequestAdapterFactory(request).mitmproxy_request()

  # Query Params
  query_param_names_facade = facade.query_param_names
  handler = RequestSynchronizeHandler(request_component.QUERY_PARAM, lifecycle_hooks)
  synchronize_component(mitmproxy_request.query, query_param_names_facade, handler)

  # Body
  headers = mitmproxy_request.headers
  body_params = decode_response(mitmproxy_request.content, headers.get('content-type'))
  body_param_names_facade = facade.body_param_names
  handler = RequestSynchronizeHandler(request_component.BODY_PARAM, lifecycle_hooks)
  synchronize_component(body_params, body_param_names_facade, handler)
  mitmproxy_request.content = encode_response(body_params)

  # Response
  python_response = OrmResponseAdapterFactory(request.response).python_response()
  headers = python_response.headers
  response_params = decode_response(python_response.content, headers.get('content-type'))
  response_param_names_facade = facade.response_param_names
  valid = validate_component(response_param_names_facade, response_params)[0]

  if not valid:
    __synchronize_response(endpoint)

def synchronize_component(component, facade: RequestComponentNamesFacade, handler: RequestSynchronizeHandler):
  lifecycle_hooks = __lifecycle_hooks(handler)
  context = __context(lifecycle_hooks)

  return contract_matches(context, facade, component)

def validate_component(facade: RequestComponentNamesFacade, component):
  context = __context({})

  return contract_matches(context, facade, component)

def __context(lifecycle_hooks):
  class TestContextMock():

    def __init__(self, lifecycle_hooks: dict):
      self.__lifecycle_hooks = lifecycle_hooks

    @property
    def lifecycle_hooks(self):
      return self.__lifecycle_hooks

    @lifecycle_hooks.setter
    def lifecycle_hooks(self, v):
      self.__lifecycle_hooks = v

  return TestContextMock(lifecycle_hooks)

def __lifecycle_hooks(handler: RequestSynchronizeHandler):
  hooks = {}

  hooks[ON_LENGTH_MATCH_ERROR] = handler.handle_length_match_error
  hooks[ON_PARAM_NAME_EXISTS_ERROR] = handler.handle_param_name_exists
  hooks[ON_PARAM_NAME_MISSING_ERROR] = handler.handle_param_name_missing
  hooks[ON_TYPE_MATCH_ERROR] = handler.handle_type_match_error
  hooks[ON_VALID_TYPE_ERROR] = handler.handle_valid_type_error

  return hooks

def __synchronize_response(endpoint: EndpointShowResponse):
  # For each request / scenario, replay and overwrite
  pass