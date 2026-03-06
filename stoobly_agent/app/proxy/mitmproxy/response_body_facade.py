import pdb

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from mitmproxy.http import Response as MitmproxyResponse

from ..replay.body_parser_service import decode_response, encode_response

class MitmproxyResponseBodyFacade:
    def __init__(self, response: 'MitmproxyResponse'):
        self.__response = response

    def get(self, content_type: Union[bytes, str]):
        return decode_response(self.__response.content, content_type)

    def set(self, content, content_type: Union[bytes, str]):
        """
        Adjusting Content-Length header should be done by MitmproxyResponse
        """
        self.__response.content = encode_response(content, content_type).encode()