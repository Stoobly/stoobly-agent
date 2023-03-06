from io import BytesIO
import requests

from mitmproxy.http import Response as MitmproxyResponse
from urllib3 import HTTPResponse

class PythonResponseAdapter():

  def __init__(self, response: MitmproxyResponse):
    self.__response = response

  def adapt(self) -> requests.Response:
    response = requests.Response()
    response.status_code = self.__response.status_code
    response.headers = self.__response.headers

    response.raw = HTTPResponse(
      body=BytesIO(self.__response.raw_content),
      decode_content=False,
      headers=self.__response.headers,
      preload_content=False
    )

    return response