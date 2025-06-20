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
      
    self.__split_joined_request_string = self.raw_request_split(joined_request_string, payloads_delimitter) 

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

    delimitter = RequestStringCLRF
    request_string_toks = self.repaired_string_toks(self.__split_joined_request_string[0], delimitter)
    request_string.set(self.raw_request_string or delimitter.join(request_string_toks[1:]))
    request_string.control = request_string_toks[0]

    return request_string

  def build_response_string(self):
    response_string = ResponseString(None, None)

    delimitter = ResponseStringCLRF
    response_string_toks = self.repaired_string_toks(self.__split_joined_request_string[1], delimitter)
    response_string.set(self.raw_response_string or delimitter.join(response_string_toks[1:]))
    response_string.control = response_string_toks[0]

    return response_string

  def adapt(self) -> JoinedRequest:
    joined_request = JoinedRequest()

    joined_request.request_string = self.build_request_string()
    joined_request.response_string = self.build_response_string()
    return joined_request

  # If all CRLF characters have been replaced with LF e.g. visual studio code
  # Then try to repair the raw string, see https://github.com/Stoobly/stoobly-agent/issues/415
  @staticmethod
  def repaired_string_toks(raw_string: bytes, delimitter: bytes):
    toks = raw_string.split(delimitter)

    if len(toks) == 1:
      lf = b"\n"
      toks = raw_string.split(lf)

      # See for request: https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html
      # See for response: https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html 
      i = 0
      for line in toks:
        i += 1

        # On two lf characters, then the following lines are the body
        if line == b'':
          break

      toks = toks[:i] + [lf.join(toks[i:])]

    if len(toks) == 1:
      raise ValueError(f"Could not split request by {delimitter}")

    return toks

  @staticmethod
  def raw_request_split(raw_string: bytes, payloads_delimitter = REQUEST_DELIMITTER):
    toks = raw_string.split(payloads_delimitter)
    if len(toks) != 2:
      toks = raw_string.split(payloads_delimitter.replace(b"\n", b"\r\n"))
    return toks