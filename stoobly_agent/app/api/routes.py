import re

from stoobly_agent.app.api.bodies_controller import BodiesController
from stoobly_agent.app.api.headers_controller import HeadersController
from stoobly_agent.app.api.query_params_controller import QueryParamsController
from stoobly_agent.app.api.replayed_responses_controller import ReplayedResponsesController
from stoobly_agent.app.api.requests_controller import RequestsController
from stoobly_agent.app.api.responses_controller import ResponsesController
from stoobly_agent.app.api.response_headers_controller import ResponseHeadersController
from stoobly_agent.app.api.scenarios_controller import ScenariosController

from .configs_controller import ConfigsController
from .proxy_controller import ProxyController
from .replayed_response_headers_controller import ReplayedResponseHeadersController
from .statuses_controller import StatusesController

CONFIGS_PATH = '/configs'
PROXY_PATH = '/proxy'
REQUESTS_PATH = '/requests'
SCENARIOS_PATH = '/scenarios'
STATUSES_PATH = '/statuses'

BODIES_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+/bodies")
BODY_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+/bodies/[^/]+")
HEADERS_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+/headers")
HEADER_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+/headers/[^/]+")
RESPONSE_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+/responses/[^/]+")
RESPONSES_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+/responses")
QUERY_PARAMS_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+/query_params")
QUERY_PARAM_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+/query_params/[^/]+")
REPLAYED_RESPONSES_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+/replayed_responses")
REPLAYED_RESPONSE_PATH = re.compile(f"{REPLAYED_RESPONSES_PATH.pattern}/[^/]+")
REPLAYED_RESPONSE_HEADERS_PATH = re.compile(f"{REPLAYED_RESPONSES_PATH.pattern}/[^/]+/headers")
RESPONSE_HEADERS_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+/response_headers")
RESPONSE_HEADER_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+/response_headers/[^/]+")
REQUEST_PATH = re.compile(f"{REQUESTS_PATH}/[^/]+")
SCENARIO_PATH = re.compile(f"{SCENARIOS_PATH}/[^/]+")
STATUS_PATH = re.compile(f"{STATUSES_PATH}/[^/]+")

ROUTES = {
  'DELETE': [
    [HEADERS_PATH, HeadersController.instance().destroy],
    [QUERY_PARAMS_PATH, QueryParamsController.instance().destroy],
    [RESPONSE_HEADERS_PATH, ResponseHeadersController.instance().destroy],
    [REQUEST_PATH, RequestsController.instance().destroy],
    [SCENARIO_PATH, ScenariosController.instance().destroy],
  ],
  'GET': [
      [CONFIGS_PATH, ConfigsController.instance().show],
      ['/'.join([CONFIGS_PATH, 'summary']), ConfigsController.instance().summary],
      ['/'.join([CONFIGS_PATH, 'policies']), ConfigsController.instance().policies],
      ['/'.join([PROXY_PATH, 'get']), ProxyController.instance().do_GET],
      [re.compile('/'.join([BODIES_PATH.pattern, 'mock'])), BodiesController.instance().mock],
      [HEADERS_PATH, HeadersController.instance().index],
      [QUERY_PARAMS_PATH, QueryParamsController.instance().index],
      [REPLAYED_RESPONSE_HEADERS_PATH, ReplayedResponseHeadersController().index],
      [re.compile('/'.join([REPLAYED_RESPONSE_PATH.pattern, 'mock'])), ReplayedResponsesController().mock],
      [REPLAYED_RESPONSES_PATH, ReplayedResponsesController().index],
      [re.compile('/'.join([RESPONSES_PATH.pattern, 'mock'])), ResponsesController.instance().mock],
      [RESPONSES_PATH, ResponsesController.instance().show],
      [RESPONSE_HEADERS_PATH, ResponseHeadersController.instance().index],
      [REQUESTS_PATH, RequestsController.instance().index],
      [re.compile('/'.join([REQUEST_PATH.pattern, 'replay'])), RequestsController.instance().replay],
      [re.compile('/'.join([REQUEST_PATH.pattern, 'download$'])), RequestsController.instance().download],
      [REQUEST_PATH, RequestsController.instance().get],
      [SCENARIOS_PATH, ScenariosController.instance().index],
      [re.compile('/'.join([SCENARIO_PATH.pattern, 'download$'])), ScenariosController.instance().download],
      [STATUSES_PATH, StatusesController.instance().index],
      [SCENARIO_PATH, ScenariosController.instance().get],
  ],
  'POST': [
      ['/'.join([PROXY_PATH, 'post']), ProxyController.instance().do_POST],
      [HEADERS_PATH, HeadersController.instance().create],
      [QUERY_PARAMS_PATH, QueryParamsController.instance().create],
      [RESPONSE_HEADERS_PATH, ResponseHeadersController.instance().create],
      [REQUESTS_PATH, RequestsController.instance().create],
      [re.compile('/'.join([REQUEST_PATH.pattern, 'push$'])), RequestsController.instance().push],
      [SCENARIOS_PATH, ScenariosController.instance().create],
  ],
  'PUT': [
      [CONFIGS_PATH, ConfigsController.instance().update],
      ['/'.join([PROXY_PATH, 'put']), ProxyController.instance().do_PUT],
      [BODY_PATH, BodiesController.instance().update],
      [HEADER_PATH, HeadersController.instance().update],
      [QUERY_PARAM_PATH, QueryParamsController.instance().update],
      [RESPONSE_PATH, ResponsesController.instance().update],
      [RESPONSE_HEADER_PATH, ResponseHeadersController.instance().update],
      [re.compile('/'.join([REPLAYED_RESPONSE_PATH.pattern, 'activate'])), ReplayedResponsesController().activate],
      ['/'.join([REQUESTS_PATH, 'send']), RequestsController.instance().send],
      [REQUEST_PATH, RequestsController.instance().update],
      [STATUS_PATH, StatusesController.instance().update],
      [SCENARIO_PATH, ScenariosController.instance().update],
  ]
}