import pdb

from mitmproxy.http import Request as MitmproxyRequest
from typing import Union

from ..replay.body_parser_service import decode_response, encode_response

class MitmproxyRequestBodyFacade:
    def __init__(self, request: MitmproxyRequest):
        self.__request = request

    def get(self, content_type: Union[bytes, str]):
        return decode_response(self.__request.content, content_type)

    def set(self, content, content_type: Union[bytes, str]):
        """
        Adjusting Content-Length header should be done by MitmproxyRequest
        """
        self.__request.content = encode_response(content, content_type).encode()