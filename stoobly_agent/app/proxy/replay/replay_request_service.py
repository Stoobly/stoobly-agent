import pdb
import requests

from http.cookies import SimpleCookie
from typing import Callable, TypedDict, Union
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.replay.trace_context import TraceContext

from stoobly_agent.config.constants import custom_headers, request_origin, test_strategy
from stoobly_agent.lib.logger import bcolors, Logger
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.config.constants import mode

class ReplayRequestOptions(TypedDict):
  mode: Union[mode.MOCK, mode.RECORD, mode.TEST, None]
  on_response: Union[Callable[[ReplayContext], Union[requests.Response, None]], None]
  project_key: Union[str, None]
  quiet: bool
  report_key: Union[str, None] 
  request_origin: Union[request_origin.CLI, None] 
  scenario_key: Union[str, None] 
  test_strategy: Union[test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY]
  trace_context: TraceContext

def replay_with_trace(context: ReplayContext, trace_context: TraceContext, options: ReplayRequestOptions):
  return trace_context.with_replay_context(context, lambda context: replay(context, options))

def replay(context: ReplayContext, options: ReplayRequestOptions) -> requests.Response:
  __log(context)

  request = context.request
  headers = request.headers

  if 'mode' in options:
    __handle_mode_option(request, headers, options['mode'])

  if 'project_key' in options:
    headers[custom_headers.PROJECT_KEY] = options['project_key']

  if 'report_key' in options:
    headers[custom_headers.REPORT_KEY] = options['report_key']

  if 'request_origin' in options:
    headers[custom_headers.REQUEST_ORIGIN] = options['request_origin']

  if 'scenario_key' in options:
    headers[custom_headers.SCENARIO_KEY] = options['scenario_key']

  if 'test_strategy' in options:
    headers[custom_headers.TEST_STRATEGY] = options['test_strategy']

  method = request.method
  handler = getattr(requests, method.lower())
  cookies = __get_cookies(request.headers)

  # Do not send query params, they should be a part of the URL
  res: requests.Response = handler(
    request.url, 
    allow_redirects = True,
    cookies = cookies,
    data=request.body,
    headers=headers, 
    #params=request.query_params,
    stream = True
  )

  if 'on_response' in options and callable(options['on_response']):
    context.with_response(res)
    res = options['on_response'](context) or res

  return res

def __handle_mode_option(request: Request, headers, _mode):
  headers[custom_headers.PROXY_MODE] = _mode

  # If mocking or testing, we already know which request to get response from 
  if _mode == mode.MOCK or _mode == mode.TEST:
    headers[custom_headers.MOCK_REQUEST_ID] = str(request.id)

def __log(context: ReplayContext):
  request = context.request

  # If request is not the first of a sequence, print extra new line
  sequence = context.sequence
  if sequence and sequence > 1:
    print()

  Logger.instance().info(f"{bcolors.OKCYAN}{request.method} {request.url}{bcolors.ENDC}")

def __get_cookies(headers: Request.headers):
  return SimpleCookie(headers.get('Cookie'))