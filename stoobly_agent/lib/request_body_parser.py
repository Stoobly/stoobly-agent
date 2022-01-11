import json
import pdb
import urllib.parse

class RequestBodyParser:
    JSON = 'application/json'
    WWW_FORM_URLENCODED = 'application/x-www-form-urlencoded'

    @classmethod
    def parse(cls, content, content_type):
        if isinstance(content, bytes):
            content = content.decode('utf-8')

        params = {}

        if not content_type:
            content_type = ''

        content_type = content_type.lower()

        if content_type == cls.JSON:
            params = cls.__parse_json(content)
        elif content_type == cls.WWW_FORM_URLENCODED:
            params = cls.__parse_www_form_urlencoded(content)

        return params

    @classmethod
    def stringify(cls, content, content_type):
        content_type = content_type.lower()

        if content_type == cls.JSON:
            return cls.__stringify_json(content)
        elif content_type == cls.WWW_FORM_URLENCODED:
            return cls.__stringify_www_form_urlencoded(content)

        return content

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

