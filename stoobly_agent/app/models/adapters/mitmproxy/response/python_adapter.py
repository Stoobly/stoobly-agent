from io import BytesIO

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Response
    from mitmproxy.http import Response as MitmproxyResponse

class PythonResponseAdapter():

  def __init__(self, response: 'MitmproxyResponse'):
    self.__response = response

  def adapt(self) -> 'Response':
    # Lazy import for runtime usage
    import requests
    response = requests.Response()
    response.status_code = self.__response.status_code
    response.headers = self.__response.headers

    from urllib3 import HTTPResponse
    response.raw = HTTPResponse(
      body=BytesIO(self.__response.raw_content),
      decode_content=False,
      headers=self.__response.headers,
      preload_content=False
    )

    return response