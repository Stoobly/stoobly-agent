import pdb

from mitmproxy.net.http.request import Request as MitmproxyRequest
from typing import Union

from ..replay.body_parser_service import JSON, MULTIPART_FORM, normalize_header, parse_json, serialize_json, WWW_FORM_URLENCODED

class MitmproxyRequestBodyFacade:
    def __init__(self, request: MitmproxyRequest):
        self.__request = request

    def get(self, content_type: Union[bytes, str]):
        content_type = normalize_header(content_type)

        params = {}
        if content_type == JSON:
            content = self.__request.content

            if isinstance(content, bytes):
                content = content.decode('utf-8')

            if not content_type:
                content_type = ''

            params = parse_json(content)
        elif content_type == WWW_FORM_URLENCODED:
            params = self.__request.urlencoded_form
        elif content_type == MULTIPART_FORM:
            params = self.__request.multipart_form

        return params

    def set(self, content, content_type: Union[bytes, str]):
        """
        Adjusting Content-Length header should be done by MitmproxyRequest
        """
        content_type = normalize_header(content_type)

        if content_type == JSON:
            self.__request.set_content(serialize_json(content))
        elif content_type == WWW_FORM_URLENCODED:
            self.__request.urlencoded_form = content
        elif content_type == MULTIPART_FORM:
            self.__request.multipart_form = content.items()
            # Fix bug where mitmproxy sets headers["content-type"] = 'multipart/form-data' without the boundary
            self.__request.headers['content-type'] = content_type