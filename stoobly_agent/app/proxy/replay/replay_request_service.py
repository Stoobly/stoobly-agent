import os
import pdb
import requests

from http.cookies import SimpleCookie
from time import time
from typing import Callable, TypedDict, Union

from stoobly_agent.app.cli.ca_cert_installer import CACertInstaller
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.models.adapters.python import PythonResponseAdapterFactory
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.models.replayed_response_model import ReplayedResponseModel
from stoobly_agent.app.proxy.replay.trace_context import TraceContext
from stoobly_agent.app.proxy.simulate_intercept_service import simulate_intercept
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import alias_resolve_strategy, custom_headers, request_origin, test_filter, test_strategy
from stoobly_agent.config.mitmproxy import MitmproxyConfig
from stoobly_agent.config.constants import mock_policy, mode
from stoobly_agent.lib.orm.replayed_response import ReplayedResponse

class ReplayRequestOptions(TypedDict):
  alias_resolve_strategy: alias_resolve_strategy.AliasResolveStrategy
  group_by: str
  host: str
  lifecycle_hooks_script_path: str
  mode: Union[mode.MOCK, mode.RECORD, mode.TEST, None]
  before_replay: Union[Callable[[ReplayContext], None], None]
  after_replay: Union[Callable[[ReplayContext], Union[requests.Response, None]], None]
  project_key: Union[str, None]
  proxies: dict
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
  if 'before_replay' in options and callable(options['before_replay']):
    options['before_replay'](context)

  request = context.request
  headers = request.headers
  method = request.method

  if options.get('host'):
    request.host = options['host']
    headers['host'] = options['host']

  if options.get('scheme'):
    request.scheme = options['scheme']

  if options.get('alias_resolve_strategy'):
    headers[custom_headers.ALIAS_RESOLVE_STRATEGY] = options['alias_resolve_strategy']

  if options.get('lifecycle_hooks_script_path'):
    __handle_lifecycle_hooks_script_path(options['lifecycle_hooks_script_path'], headers) 

  if options.get('mode'):
    __handle_mode_option(options['mode'], request, headers)

  if options.get('project_key'):
    headers[custom_headers.PROJECT_KEY] = options['project_key']

  if options.get('report_key'):
    headers[custom_headers.REPORT_KEY] = options['report_key']

  if options.get('request_origin'):
    headers[custom_headers.REQUEST_ORIGIN] = options['request_origin']

  if options.get('scenario_key'):
    headers[custom_headers.SCENARIO_KEY] = options['scenario_key']

  if options.get('test_filter'):
    headers[custom_headers.TEST_FILTER] = options['test_filter']

  if options.get('test_strategy'):
    headers[custom_headers.TEST_STRATEGY] = options['test_strategy']

  request_config = {
    'allow_redirects': True,
    'stream': True,
    'verify': not MitmproxyConfig.instance().get('ssl_insecure')
  }
  request_dict = {
    'data': request.body,
    'headers': headers, 
    #'params': request.query_params, # Do not send query params, they should be a part of the URL
  }

  now = time()
  res: requests.Response = None
  if not options.get('proxy'):
    headers[custom_headers.REQUEST_ORIGIN] = request_origin.CLI
    request = requests.Request(**{
      **request_dict,
      'method': method,
      'url': request.url,
    })

    res = simulate_intercept(request, **request_config)
  else:
    settings = Settings.instance()
    handler = getattr(requests, method.lower())

    res = handler(
      request.url, 
      **{
        **request_config,
        **request_dict,
        'proxies': {
          'http': settings.proxy.url,
          'https': settings.proxy.url,
        },
        'verify': CACertInstaller().mitm_crt_absolute_path if request_config['verify'] else False,
      }
    )
  received_at = time()
  latency = int((received_at - now) * 1000)

  if options['mode'] == mode.REPLAY:
    if options.get('save') or options.get('overwrite'):
      replayed_response = __create_replayed_response(context.request.id, res, latency)

      if options.get('overwrite'):
        __overwrite_response(replayed_response.get('id'))

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
    if request.id:
      headers[custom_headers.MOCK_REQUEST_ID] = str(request.id)

    headers[custom_headers.MOCK_POLICY] = mock_policy.ALL
  elif _mode == mode.RECORD:
    # If recording, then it's actually a replay and record
    headers[custom_headers.PROXY_MODE] = mode.REPLAY
    headers[custom_headers.RESPONSE_PROXY_MODE] = mode.RECORD

def __create_replayed_response(request_id: int, res: requests.Response, latency: int):   
  replayed_response_model = ReplayedResponseModel(Settings.instance())
  raw = PythonResponseAdapterFactory(res).raw_response()
  return replayed_response_model.create(
    latency = latency,
    raw = raw,
    request_id = request_id,
    status = res.status_code,
  )

def __overwrite_response(replayed_response_id):
  replayed_response_model = ReplayedResponseModel(Settings.instance())
  return replayed_response_model.activate(replayed_response_id)