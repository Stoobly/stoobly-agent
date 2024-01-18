from io import BytesIO
import json
from requests import Response

from stoobly_agent.app.proxy.constants import custom_response_codes

class IgnoreComponentsResponseBuilder():
  __response = None

  def __init__(self):
    self.__response = Response()

  def build(self, ignored_components: list = []):
    content = json.dumps(ignored_components)
    self.__response.raw = BytesIO(content.encode()) 
    self.__response.status_code = custom_response_codes.IGNORE_COMPONENTS
    return self.__response