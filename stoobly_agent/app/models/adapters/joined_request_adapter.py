import pdb

from typing import Union

from stoobly_agent.app.proxy.record.joined_request import JoinedRequest, REQUEST_DELIMITTER
from stoobly_agent.app.proxy.record.request_string import CLRF as RequestStringCLRF, RequestString
from stoobly_agent.app.proxy.record.response_string import CLRF as ResponseStringCLRF, ResponseString

class JoinedRequestAdapter():

  def __init__(self, joined_request_string: Union[bytes, str], payloads_delimitter: Union[bytes, str] = None):
    payloads_delimitter = REQUEST_DELIMITTER if not payloads_delimitter else payloads_delimitter

    if isinstance(joined_request_string, str):
      joined_request_string = joined_request_string.encode()

    if isinstance(payloads_delimitter, str):
      payloads_delimitter = payloads_delimitter.encode()
      
    self.__split_joined_request_string = joined_request_string.split(payloads_delimitter)
    if len(self.__split_joined_request_string) != 2:
      self.__split_joined_request_string = joined_request_string.split(payloads_delimitter.replace(b"\n", b"\r\n"))

    if len(self.__split_joined_request_string) != 2:
      raise ValueError(f"Could not split by {payloads_delimitter}")

    self.__raw_request_string = None
    self.__raw_response_string = None

  @property
  def raw_request_string(self):
    return self.__raw_request_string

  @raw_request_string.setter
  def raw_request_string(self, v):
    self.__raw_request_string = v

  @property
  def raw_response_string(self):
    return self.__raw_response_string

  @raw_response_string.setter
  def raw_response_string(self, v):
    self.__raw_response_string = v

  def build_request_string(self):
    request_string = RequestString(None)

    delimitter = RequestStringCLRF.encode()
    request_string_toks = self.__split_joined_request_string[0].split(delimitter)
    request_string.set(self.raw_request_string or delimitter.join(request_string_toks[1:]))
    request_string.control = request_string_toks[0]

    return request_string

  def build_response_string(self):
    response_string = ResponseString(None, None)

    delimitter = ResponseStringCLRF
    response_string_toks = self.__split_joined_request_string[1].split(delimitter)
    response_string.set(self.raw_response_string or delimitter.join(response_string_toks[1:]))
    response_string.control = response_string_toks[0]

    return response_string

  def adapt(self) -> JoinedRequest:
    joined_request = JoinedRequest()

    joined_request.request_string = self.build_request_string()
    joined_request.response_string = self.build_response_string()
    return joined_request