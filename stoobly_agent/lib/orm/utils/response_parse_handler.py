from typing import TypedDict

class Header(TypedDict):
  name: bytes
  value: bytes

class Response(TypedDict):
  body: bytes
  headers: dict
  status: bytes
  status_code: int
  url: bytes

class ResponseParseHandler():
  __response_shell: Response = None

  def __init__(self, response_shell: dict = {}):
    self.__response_shell = response_shell
    self.__response_shell['headers'] = {}

  def on_body(self, body: bytes):
    self.__response_shell['body'] = body

  def on_header(self, name: bytes, value: bytes):
    self.__response_shell['headers'][name] = value

  def on_status(self, status: bytes):
    self.__response_shell['status'] = status

  def on_url(self, url: bytes):
    self.__response_shell['url'] = url