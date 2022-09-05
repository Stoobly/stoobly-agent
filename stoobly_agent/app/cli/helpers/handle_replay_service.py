import json
import pdb

from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.cli.types.output import ReplayOutput
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response, is_traversable
from stoobly_agent.lib.logger import Logger, bcolors
from stoobly_agent.lib.utils import jmespath

DEFAULT_FORMAT = 'default'
JSON_FORMAT = 'json'

def handle_before_replay(context: ReplayContext, format = None):
  format = format or DEFAULT_FORMAT

  if format == DEFAULT_FORMAT:
    request = context.request

    # If request is not the first of a sequence, print extra new line
    sequence = context.sequence
    if sequence and sequence > 1:
      print()

    print(f"{bcolors.OKCYAN}{request.method} {request.url}{bcolors.ENDC}")

def print_request(context: ReplayContext, format = None):
  format_handler = default_format_handler 
  
  if format == JSON_FORMAT:
    format_handler = json_format_handler

  format_handler(context)

def print_request_query(context: ReplayContext, query: str):
  response = context.response
  content = response.content
  content_type = response.headers.get('content-type')

  decoded_response = decode_response(content, content_type)
  if not is_traversable(decoded_response):
    Logger.instance().error(
      f"{bcolors.FAIL}Could not query request, expected responsed to be of type {dict} or {list}, got {decoded_response.__class__} {bcolors.ENDC}"
    )
    print_request(context)
  else:
    print(jmespath.search(query, decoded_response))

def default_format_handler(context: ReplayContext, additional=''):
  response = context.response
  
  try:
    print(response.content.decode())
  except UnicodeDecodeError as e:
    print(response.content)

  seconds = context.end_time - context.start_time
  ms = round(seconds * 1000)
  print(f"Completed {response.status_code} in {ms}ms{additional}")

def json_format_handler(context: ReplayContext):
  response = context.response
  headers = dict(response.headers)
  content = response.content.decode()

  output: ReplayOutput = {'headers': headers, 'content': content}
  print(json.dumps(output))