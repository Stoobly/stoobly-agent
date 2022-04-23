import pdb
import requests

from http.cookies import SimpleCookie
from typing import TypedDict, Union

from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.logger import Logger
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.config.constants import mode

class ReplayRequestOptions(TypedDict):
  mode: Union[mode.MOCK, mode.RECORD, mode.TEST, None]
  project_key: str
  report_key: str
  scenario_key: str

def replay(request: Request, **kwargs: ReplayRequestOptions) -> requests.Response:
  method = request.method
  handler = getattr(requests, method.lower())
  cookies = __get_cookies(request.headers)

  headers = request.headers

  # Set headers to identify request
  if 'mode' in kwargs:
    headers[custom_headers.PROXY_MODE] = kwargs['mode'] 

  if 'project_key' in kwargs:
    headers[custom_headers.PROJECT_KEY] = kwargs['project_key']

  if 'report_key' in kwargs:
    headers[custom_headers.REPORT_KEY] = kwargs['report_key']

  if 'scenario_key' in kwargs:
    headers[custom_headers.SCENARIO_KEY] = kwargs['scenario_key']

  if 'test_origin' in kwargs:
    headers[custom_headers.TEST_ORIGIN] = kwargs['test_origin']

  if 'test_strategy' in kwargs:
    headers[custom_headers.TEST_STRATEGY] = kwargs['test_strategy']

  Logger.instance().info(f"{method} {request.url}")

  # Do not send query params, they should be a part of the URL
    
  return handler(
    request.url, 
    allow_redirects = True,
    cookies = cookies,
    data=request.body,
    headers=headers, 
    #params=request.query_params,
    stream = True
  )

def __get_cookies(headers: Request.headers):
  return SimpleCookie(headers.get('Cookie'))