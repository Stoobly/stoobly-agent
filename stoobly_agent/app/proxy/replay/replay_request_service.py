import os
import pdb
import requests

from http.cookies import SimpleCookie
from typing import Callable, TypedDict, Union
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.proxy.replay.trace_context import TraceContext

from stoobly_agent.config.constants import alias_resolve_strategy, custom_headers, request_origin, test_filter, test_strategy
from stoobly_agent.config.mitmproxy import MitmproxyConfig
from stoobly_agent.lib.api.api import Api
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.config.constants import mode

class ReplayRequestOptions(TypedDict):
  alias_resolve_strategy: alias_resolve_strategy.AliasResolveStrategy
  group_by: str
  host: str
  lifecycle_hooks_script_path: str
  mode: Union[mode.MOCK, mode.RECORD, mode.TEST, None]
  before_replay: Union[Callable[[ReplayContext], None], None]
  after_replay: Union[Callable[[ReplayContext], Union[requests.Response, None]], None]
  project_key: Union[str, None]
  report_key: Union[str, None] 
  request_origin: Union[request_origin.CLI, None] 
  scenario_key: Union[str, None] 
  scheme: str
  test_filter: test_filter.TestFilter
  test_strategy: Union[test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY]
  trace_context: TraceContext

def replay_with_trace(context: ReplayContext, trace_context: TraceContext, options: ReplayRequestOptions):
  trace_context.alias_resolve_strategy = options.get('alias_resolve_strategy')
  return trace_context.with_replay_context(context, lambda context: replay(context, options))

def replay(context: ReplayContext, options: ReplayRequestOptions) -> requests.Response:
  if 'before_replay' in options and callable(options['after_replay']):
    options['before_replay'](context)

  request = context.request
  headers = request.headers

  if options.get('host'):
    request.host = options['host']
    headers['host'] = options['host']

  if options.get('scheme'):
    request.scheme = options['scheme']

  if 'alias_resolve_strategy' in options:
    headers[custom_headers.ALIAS_RESOLVE_STRATEGY] = options['alias_resolve_strategy']

  if 'lifecycle_hooks_script_path' in options:
    __handle_lifecycle_hooks_script_path(options['lifecycle_hooks_script_path'], headers) 

  if 'mode' in options:
    __handle_mode_option(options['mode'], request, headers)

  if 'project_key' in options:
    headers[custom_headers.PROJECT_KEY] = options['project_key']

  if 'report_key' in options:
    headers[custom_headers.REPORT_KEY] = options['report_key']

  if 'request_origin' in options:
    headers[custom_headers.REQUEST_ORIGIN] = options['request_origin']

  if 'scenario_key' in options:
    headers[custom_headers.SCENARIO_KEY] = options['scenario_key']

  if 'test_filter' in options:
    headers[custom_headers.TEST_FILTER] = options['test_filter']

  if 'test_strategy' in options:
    headers[custom_headers.TEST_STRATEGY] = options['test_strategy']

  method = request.method
  handler = getattr(requests, method.lower())
  cookies = __get_cookies(request.headers)

  # Set proxy env vars to ensure request gets sent to proxy
  res: requests.Response = Api().with_proxy(lambda: handler(
    request.url, 
    allow_redirects = True,
    cookies = cookies,
    data=request.body,
    headers=headers, 
    #params=request.query_params, # Do not send query params, they should be a part of the URL
    stream = True,
    verify = not MitmproxyConfig.instance().get('ssl_insecure')
  ))

  if 'after_replay' in options and callable(options['after_replay']):
    context.with_response(res)
    res = options['after_replay'](context) or res

  return res

def __handle_lifecycle_hooks_script_path(script_path, headers):
  if not script_path:
    return

  if not os.path.isabs(script_path):
    script_path = os.path.join(os.path.abspath('.'), script_path)

  headers[custom_headers.LIFECYCLE_HOOKS_SCRIPT_PATH] = script_path

def __handle_mode_option(_mode, request: Request, headers):
  headers[custom_headers.PROXY_MODE] = _mode

  if _mode == mode.MOCK or _mode == mode.TEST:
    # If mocking or testing, we already know which request to get response from 
    headers[custom_headers.MOCK_REQUEST_ID] = str(request.id)
  elif _mode == mode.RECORD:
    # If recording, then it's actually a replay and record
    headers[custom_headers.PROXY_MODE] = mode.REPLAY
    headers[custom_headers.RESPONSE_PROXY_MODE] = mode.RECORD

def __get_cookies(headers: Request.headers):
  return SimpleCookie(headers.get('Cookie'))