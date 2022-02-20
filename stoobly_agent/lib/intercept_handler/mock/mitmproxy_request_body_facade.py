import json
import pdb
import urllib.parse

from mitmproxy.net.http.request import Request as MitmproxyRequest

class MitmproxyRequestBodyFacade:
    JSON = 'application/json'
    WWW_FORM_URLENCODED = 'application/x-www-form-urlencoded'
    MULTIPART_FORM = 'multipart/form-data'

    def __init__(self, request: MitmproxyRequest):
        self.__request = request

    def get(self, content_type):
        params = {}
        content_type = content_type.lower()

        if content_type == self.JSON:
            content = self.__request.content

            if isinstance(content, bytes):
                content = content.decode('utf-8')

            if not content_type:
                content_type = ''

            params = self.__parse_json(content)
        elif content_type == self.WWW_FORM_URLENCODED:
            params = self.__request.urlencoded_form
        elif self.MULTIPART_FORM in content_type:
            params = self.__request.multipart_form

        return params

    def set(self, content, content_type):
        if not content_type:
            return content
            
        content_type = content_type.lower()

        if content_type == self.JSON:
            self.__request.set_content(self.__stringify_json(content))
        elif content_type == self.WWW_FORM_URLENCODED:
            self.__request.urlencoded_form = content
        elif self.MULTIPART_FORM in content_type:
            self.__request.multipart_form = content.items()
            # Fix bug where mitmproxy sets headers["content-type"] = 'multipart/form-data' without the boundary
            self.__request.headers['content-type'] = content_type

    @staticmethod
    def __parse_json(content):
        try:
            return json.loads(content)
        except:
            return {}

    @staticmethod
    def __parse_www_form_urlencoded(content):
        try:
            return urllib.parse.parse_qs(content)
        except:
            return {}

    @staticmethod
    def __stringify_json(content):
        try:
            return json.dump(content)
        except:
            return content

    @staticmethod
    def __stringify_www_form_urlencoded(content):
        try:
            return urllib.parse.urlencode(content)
        except:
            return content

