import requests

from http.cookies import SimpleCookie
from typing import TypedDict, Union

from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.api.schemas.request import Request
from stoobly_agent.lib.constants import custom_headers
from stoobly_agent.lib.intercept_handler.constants import modes

class ReplayRequestOptions(TypedDict):
  mode: Union[modes.MOCK, modes.RECORD, modes.TEST, None]
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

  Logger.instance().info(f"{method} {request.url}")
    
  return handler(
    request.url, 
    allow_redirects = True,
    cookies = cookies,
    data=request.body,
    headers=headers, 
    params=request.query_params,
    stream = True
  )

def __get_cookies(headers: Request.headers):
  return SimpleCookie(headers.get('Cookie'))