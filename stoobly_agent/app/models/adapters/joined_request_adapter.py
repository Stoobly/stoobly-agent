import pdb

from stoobly_agent.app.proxy.upload.joined_request import JoinedRequest
from stoobly_agent.app.proxy.upload.request_string import CLRF as RequestStringCLRF, RequestString
from stoobly_agent.app.proxy.upload.response_string import CLRF as ResponseStringCLRF, ResponseString

class JoinedRequestAdapter():

  def __init__(self, joined_request_string: str, payloads_delimitter):
    self.__split_joined_request_string = joined_request_string.split(payloads_delimitter)

  def build_request_string(self):
    request_string = RequestString(None)

    request_string_toks = self.__split_joined_request_string[0].split(RequestStringCLRF)
    request_string.set(RequestStringCLRF.join(request_string_toks[1:]))
    request_string.control = request_string_toks[0]

    return request_string

  def build_response_string(self):
    response_string = ResponseString(None, None)

    delimitter = ResponseStringCLRF.decode()
    response_string_toks = self.__split_joined_request_string[1].split(delimitter)
    response_string.set(delimitter.join(response_string_toks[1:]))
    response_string.control = response_string_toks[0]

    return response_string

  def adapt(self) -> JoinedRequest:
    joined_request = JoinedRequest()

    joined_request.request_string = self.build_request_string()
    joined_request.response_string = self.build_response_string()
    return joined_request