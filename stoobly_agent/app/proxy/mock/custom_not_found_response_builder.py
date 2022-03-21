from io import BytesIO
from requests import Response

from stoobly_agent.app.proxy.constants import custom_response_codes

class CustomNotFoundResponseBuilder():
  __response = None

  def __init__(self):
    self.__response = Response()

  def build(self):
    self.__response.status_code = custom_response_codes.NOT_FOUND
    self.__response.raw = BytesIO('Request not found'.encode()) 
    return self.__response