import json
import pdb
import requests
import sys

from typing import List, TypedDict, Union

from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.cli.types.output import ReplayOutput
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response, is_traversable
from stoobly_agent.lib.logger import Logger, bcolors
from stoobly_agent.lib.utils import jmespath

BODY_FORMAT = 'body'
DEFAULT_FORMAT = 'default'
JSON_FORMAT = 'json'

class ReplaySession(TypedDict):
  buffer: bool
  contexts: List[ReplayContext] 
  format: Union[BODY_FORMAT, DEFAULT_FORMAT, JSON_FORMAT, None]
  scenario_id: int
  total: int

def handle_before_replay(context: ReplayContext, session: ReplaySession):
  format = session.get('format') or DEFAULT_FORMAT

  if format == DEFAULT_FORMAT:
    request = context.request

    # If request is not the first of a sequence, print extra new line
    sequence = context.sequence
    if sequence and sequence > 1:
      print()

    print(f"{bcolors.OKCYAN}{request.method} {request.url}{bcolors.ENDC}")

def handle_after_replay(context: ReplayContext, session: ReplaySession):
  if not 'contexts' in session:
    session['contexts'] = []

  if not 'total' in session:
    session['total'] = 0

  if not session.get('buffer'):
    print(format_request(context))
  else:
    session['contexts'].append(context)

  session['total'] += 1

def format_request(context: ReplayContext, format = None):
  format_handler = __default_format_handler 
  
  if format == JSON_FORMAT:
    format_handler = __json_format_handler
  elif format == BODY_FORMAT:
    format_handler = __body_format_handler

  return format_handler(context)

def print_request_query(context: ReplayContext, query: str):
  response = context.response
  content = __content(response)
  content_type = response.headers.get('content-type')

  decoded_response = decode_response(content, content_type)
  if not is_traversable(decoded_response):
    print(
      f"{bcolors.FAIL}Could not query request, expected responsed to be of type {dict} or {list}, got {decoded_response.__class__} {bcolors.ENDC}",
      file=sys.stderr
    )
    print(format_request(context), file=sys.stderr)
  else:
    print(jmespath.search(query, decoded_response))

def print_session(session: ReplaySession):
  if len(session['contexts']) == 0:
    return 

  format = session.get('format') or DEFAULT_FORMAT

  outputs = []

  for replay_context in session['contexts']:
    outputs.append(format_request(replay_context, format))

  if format == JSON_FORMAT:
    if session.get('scenario_id'):
      print(json.dumps(outputs))
    else:
      print(json.dumps(outputs[0]))
  else:
    print("\n\n".join(outputs))

def __default_format_handler(context: ReplayContext, additional=''):
  response = context.response
  content = __content(response)

  output = ''
  output += content

  seconds = context.end_time - context.start_time
  ms = round(seconds * 1000)
  output += f"\nCompleted {response.status_code} in {ms}ms{additional}"

  return output

def __body_format_handler(context: ReplayContext):
  response = context.response
  content = __content(response)
  return content

def __json_format_handler(context: ReplayContext):
  request = context.request
  response = context.response

  content = __content(response)
  headers = dict(response.headers)
  method = request.method
  url = request.url

  seconds = context.end_time - context.start_time
  ms = round(seconds * 1000)
  output: ReplayOutput = {'content': content, 'headers': headers, 'latency': ms, 'method': method, 'url': url}

  return output

def __content(res: requests.Response):
  content = res.content
  return content.decode(json.detect_encoding(content))