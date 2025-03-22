from stoobly_agent.app.proxy.context import InterceptContext
from stoobly_agent.config.constants.custom_headers import MOCK_REQUEST_ID

def handle_before_response(context: InterceptContext):
  print(context.flow.response.headers[MOCK_REQUEST_ID], end='')