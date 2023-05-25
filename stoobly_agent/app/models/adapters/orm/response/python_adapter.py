import pdb

from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.lib.orm.response import Response

class PythonResponseAdapter():

  def __init__(self, response: Response):
    self.__response = response

  def adapt(self):
    return RawHttpResponseAdapter(self.__response.raw).to_response()