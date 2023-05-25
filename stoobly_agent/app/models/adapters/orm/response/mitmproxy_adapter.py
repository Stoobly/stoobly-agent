import pdb

from stoobly_agent.app.models.adapters.python.response import MitmproxyResponseAdapter as PythonResponseMitmproxyResponseAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.lib.orm.response import Response

class MitmproxyResponseAdapter():

  def __init__(self, response: Response):
    self.__response = response

  def adapt(self):
    python_response = RawHttpResponseAdapter(self.__response.raw).to_response()
    return PythonResponseMitmproxyResponseAdapter(python_response).adapt()