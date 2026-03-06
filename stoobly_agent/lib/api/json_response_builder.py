from io import BytesIO

class JSONResponseBuilder():

  def __init__(self):
    # Lazy import for runtime usage
    from requests import Response
    self.__response = Response()
    self.__response.headers['Content-Type'] = 'application/json'

  def with_body(self, body: bytes):
    self.__response.raw = BytesIO(body)

  def with_status_code(self, status_code: int):
    self.__response.status_code = status_code