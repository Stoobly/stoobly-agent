from typing import TypedDict

class Header(TypedDict):
  name: bytes
  value: bytes

class Request(TypedDict):
  body: bytes
  headers: dict
  method: str
  status: bytes
  status_code: int
  url: bytes

class RequestParseHandler():
  __request_shell: Request = None

  def __init__(self, request_shell: dict = {}):
    self.__request_shell = request_shell
    self.__request_shell['headers'] = {}
    self.__request_shell['status_code'] = None
    self.__request_shell['method'] = None
    self.__request_shell['body'] = b''

  def on_body(self, body: bytes):
    self.__request_shell['body'] = body

  def on_header(self, name: bytes, value: bytes):
    self.__request_shell['headers'][name] = value

  def on_status(self, status: bytes):
    self.__request_shell['status'] = status

  def on_url(self, url: bytes):
    self.__request_shell['url'] = url