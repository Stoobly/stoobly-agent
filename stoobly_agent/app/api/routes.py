import re

from stoobly_agent.app.api.bodies_controller import BodiesController
from stoobly_agent.app.api.headers_controller import HeadersController
from stoobly_agent.app.api.query_params_controller import QueryParamsController
from stoobly_agent.app.api.requests_controller import RequestsController
from stoobly_agent.app.api.responses_controller import ResponsesController
from stoobly_agent.app.api.response_headers_controller import ResponseHeadersController

from .configs_controller import ConfigsController
from .proxy_controller import ProxyController
from .statuses_controller import StatusesController

CONFIGS_PATH = '/api/v1/admin/configs'
PROXY_PATH = '/proxy'
REQUESTS_PATH = '/requests'
STATUSES_PATH = '/api/v1/admin/statuses'

BODIES_PATH = re.compile(f"{REQUESTS_PATH}/.*[^/]/bodies/mock")
HEADERS_PATH = re.compile(f"{REQUESTS_PATH}/.*[^/]/headers")
RESPONSES_PATH = re.compile(f"{REQUESTS_PATH}/.*[^/]/responses/mock")
QUERY_PARAMS_PATH = re.compile(f"{REQUESTS_PATH}/.*[^/]/query_params")
RESPONSE_HEADERS_PATH = re.compile(f"{REQUESTS_PATH}/.*[^/]/response_headers")
REQUEST_PATH = re.compile(f"{REQUESTS_PATH}/.*[^/]")
STATUS_PATH = re.compile(f"{STATUSES_PATH}/.*[^/]$")

ROUTES = {
  'DELETE': [
    [REQUEST_PATH, RequestsController.instance().destroy],
  ],
  'GET': [
      [CONFIGS_PATH, ConfigsController.instance().show],
      ['/'.join([CONFIGS_PATH, 'summary']), ConfigsController.instance().summary],
      ['/'.join([CONFIGS_PATH, 'policies']), ConfigsController.instance().policies],
      ['/'.join([PROXY_PATH, 'get']), ProxyController.instance().do_GET],
      [BODIES_PATH, BodiesController.instance().mock],
      [HEADERS_PATH, HeadersController.instance().index],
      [QUERY_PARAMS_PATH, QueryParamsController.instance().index],
      [RESPONSES_PATH, ResponsesController.instance().mock],
      [RESPONSE_HEADERS_PATH, ResponseHeadersController.instance().index],
      [REQUESTS_PATH, RequestsController.instance().index],
      [REQUEST_PATH, RequestsController.instance().get],
      [STATUS_PATH, StatusesController.instance().get_status],
  ],
  'POST': [
      ['/'.join([PROXY_PATH, 'post']), ProxyController.instance().do_POST],
      [REQUESTS_PATH, RequestsController.instance().create],
      [re.compile('/'.join([REQUEST_PATH.pattern, 'upload'])), RequestsController.instance().upload],
  ],
  'PUT': [
      [CONFIGS_PATH, ConfigsController.instance().update],
      ['/'.join([PROXY_PATH, 'put']), ProxyController.instance().do_PUT],
      [REQUEST_PATH, RequestsController.instance().update],
      [STATUS_PATH, StatusesController.instance().put_status],
  ]
}