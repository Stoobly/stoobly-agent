import json
import pdb
import urllib.parse

class RequestBodyParser:
    JSON = 'application/json'
    WWW_FORM_URLENCODED = 'application/x-www-form-urlencoded'

    ###
    #
    # @param request [ActionDispatch::Request]
    #
    # @return [Hash]
    #
    @classmethod
    def parse(cls, request):
        content = request.body

        if isinstance(content, bytes):
            content = content.decode('utf-8')

        params = {}

        content_type = request.content_type
        if not content_type:
            content_type = ''

        content_type = content_type.lower()

        if content_type == cls.JSON:
            params = cls.__parse_json(content)
        elif content_type == cls.WWW_FORM_URLENCODED:
            params = cls.__parse_www_form_urlencoded(content)

        return params

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
