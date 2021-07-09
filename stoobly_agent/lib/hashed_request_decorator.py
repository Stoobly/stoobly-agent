import hashlib
import pdb

from urllib.parse import parse_qs

from .logger import Logger
from .request_body_parser import RequestBodyParser

class HashedRequestDecorator:

    LOG_ID = 'lib.hashed_request_decorator'

    COMPONENT_TYPES = {
        'HEADER': 1,
        'PATH_SEGMENT': 2,
        'QUERY_PARAM': 3,
        'BODY_PARAM': 4,
        'RESPONSE': 5
    }

    def __init__(self, request):
        self.request = request

        self.ignored_headers = {}
        self.ignored_query_params = {}
        self.ignored_body_params = {}

    ###
    #
    # self.param ignored_components [Array<Hash>] e.g. [{"name":"script-name","type":1}]
    #
    def with_ignored_components(self, ignored_components):
        for ignored_component in ignored_components:
            component_name = ignored_component['name']
            component_type = ignored_component['type']

            if component_type == self.COMPONENT_TYPES['HEADER']:
                self.ignored_headers[component_name] = True
            elif component_type == self.COMPONENT_TYPES['QUERY_PARAM']:
                self.ignored_query_params[component_name] = True
            elif component_type == self.COMPONENT_TYPES['BODY_PARAM']:
                self.ignored_body_params[component_name] = True

        return self

    def query_params_hash(self):
        serialized_params = []

        params = self.request.query.items()

        Logger.instance().debug(f"{self.LOG_ID}.query_params_hash:{params}")

        for key, value in params:
            if key in self.ignored_query_params:
                continue

            if isinstance(value, list):
                for param in value:
                    param_hash = hashlib.md5(self.__serialize_param(key, param)).hexdigest()
                    serialized_params.append(param_hash)
            else:
                param_hash = hashlib.md5(self.__serialize_param(key, value)).hexdigest()
                serialized_params.append(param_hash)

        if len(serialized_params) == 0:
            return ''

        serialized_params.sort()

        return hashlib.md5('.'.join(serialized_params).encode('utf-8')).hexdigest()

    def body_params_hash(self):
        serialized_params = []

        params = RequestBodyParser.parse(self.request)

        Logger.instance().debug(f"{self.LOG_ID}.body_params_hash:{params}")

        for key, value in params.items():
            if key in self.ignored_body_params:
                continue

            if isinstance(value, list):
                for param in value:
                    param_hash = hashlib.md5(self.__serialize_param(key, param)).hexdigest()
                    serialized_params.append(param_hash)
            else:
                param_hash = hashlib.md5(self.__serialize_param(key, value)).hexdigest()
                serialized_params.append(param_hash)

        if len(serialized_params) == 0:
            return ''

        serialized_params.sort()

        return hashlib.md5('.'.join(serialized_params).encode('utf-8')).hexdigest()

    def body_text_hash(self):
        text = self.request.body

        if len(text) == 0:
            return text

        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def __serialize_param(self, key, val):
        return f"{key}.{str(val)}".encode('utf-8')
