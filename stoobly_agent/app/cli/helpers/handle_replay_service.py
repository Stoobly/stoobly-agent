import pdb
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.cli.helpers.handle_test_service import print_request
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response
from stoobly_agent.lib.logger import Logger, bcolors
from stoobly_agent.lib.utils import jmespath

def print_request_query(context: ReplayContext, query: str):
  response = context.response
  content = response.content
  content_type = response.headers.get('content-type')

  decoded_response = decode_response(content, content_type)
  if not isinstance(decoded_response, dict) and not isinstance(decoded_response, list):
    Logger.instance().error(
      f"{bcolors.FAIL}Could not query request, expected responsed to be of type {dict} or {list}, got {decoded_response.__class__} {bcolors.ENDC}"
    )
    print_request(context)
  else:
    print(jmespath.search(query, decoded_response))