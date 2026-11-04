from io import BytesIO

from stoobly_agent.app.proxy.constants import custom_response_codes
from stoobly_agent.app.proxy.utils.response_handler import CORS_HEADERS

class CustomNotFoundResponseBuilder():
  __response = None

  def __init__(self):
    # Lazy import for runtime usage
    from requests import Response
    self.__response = Response()

  def build(self):
    self.__response.status_code = custom_response_codes.NOT_FOUND
    self.__response.raw = BytesIO('Request not found. To troubleshoot see https://docs.stoobly.com/guides/how-to-mock-apis/troubleshooting'.encode()) 
    self.__response.headers = {
      **CORS_HEADERS,
      'Content-Type': 'text/plain',
    }
    return self.__response