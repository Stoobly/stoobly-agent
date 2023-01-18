import hashlib
import pdb

from stoobly_agent.lib.logger import bcolors, Logger

from ..mitmproxy.request_facade import MitmproxyRequestFacade
from .request_hasher import RequestHasher

COMPONENT_TYPES = {
    'HEADER': 1,
    'PATH_SEGMENT': 2,
    'QUERY_PARAM': 3,
    'BODY_PARAM': 4,
    'RESPONSE': 5
}

class HashedRequestDecorator:

    LOG_ID = 'lib.hashed_request_decorator'

    def __init__(self, request: MitmproxyRequestFacade):
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
            component_type = ignored_component['type']
            component_query = ignored_component['name']
            if 'query' in ignored_component:
                component_query = ignored_component['query']

            if component_type == COMPONENT_TYPES['HEADER']:
                self.ignored_headers[component_query] = ignored_component 
            elif component_type == COMPONENT_TYPES['QUERY_PARAM']:
                self.ignored_query_params[component_query] = ignored_component 
            elif component_type == COMPONENT_TYPES['BODY_PARAM']:
                self.ignored_body_params[component_query] = ignored_component

        return self

    def headers_hash(self, with_ignored = False):
        headers = self.request.headers

        ignored_headers = {} if with_ignored else self.ignored_headers

        Logger.instance().debug(f"{bcolors.OKCYAN}Hashing headers...{bcolors.ENDC}")
        Logger.instance().debug(f"{bcolors.OKBLUE}Ignoring{bcolors.ENDC} {ignored_headers}")
        serialized_params = self.__serialize_params(headers, ignored_headers)

        return self.__hash_serialized_params(serialized_params)

    def query_params_hash_with_ignored(self):
        return self.query_params_hash(True)

    def query_params_hash(self, with_ignored = False):
        query_params = self.request.query

        params = self.__deflatten_multi_dict(query_params)
        ignored_params = {} if with_ignored else self.ignored_query_params

        Logger.instance().debug(f"{bcolors.OKCYAN}Hashing query params...{bcolors.ENDC}")
        Logger.instance().debug(f"{bcolors.OKBLUE}Ignoring{bcolors.ENDC} {ignored_params}")
        serialized_params = self.__serialize_params(params, ignored_params)

        return self.__hash_serialized_params(serialized_params)

    def body_params_hash_with_ignored(self):
        return self.body_params_hash(True)

    def body_params_hash(self, with_ignored = False):
        params = self.request.parsed_body
        ignored_params = {} if with_ignored else self.ignored_body_params

        Logger.instance().debug(f"{bcolors.OKCYAN}Hashing body params...{bcolors.ENDC}")
        Logger.instance().debug(f"{bcolors.OKBLUE}Ignoring{bcolors.ENDC} {ignored_params}")

        return RequestHasher.instance().hash_params(params, ignored_params)

    def body_text_hash(self):
        text = self.request.body

        if len(text) == 0:
            return text

        return self.__hash(text)

    def __hash_serialized_params(self, serialized_params):
        if len(serialized_params) == 0:
            return ''

        serialized_params.sort()
        return self.__hash('.'.join(serialized_params))

    def __hash(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def __serialize_param(self, key, val):
        if isinstance(key, bytes):
            key = key.decode('utf-8')

        if isinstance(val, bytes):
            val = val.decode('utf-8')
        else:
            val = str(val)
            
        return f"{key}.{val}".encode('utf-8')

    def __serialize_params(self, params, ignored_params = {}):
        serialized_params = []

        for key, value in params.items():
            if key in ignored_params:
                continue

            if isinstance(value, list):
                for param in value:
                    param_hash = hashlib.md5(self.__serialize_param(key, param)).hexdigest()

                    Logger.instance().debug(f"{self.LOG_ID}.serialized_query_params_hash:{key} -> {param} ({param_hash})")

                    serialized_params.append(param_hash)
            else:
                param_hash = hashlib.md5(self.__serialize_param(key, value)).hexdigest()

                Logger.instance().debug(f"{self.LOG_ID}.serialized_query_params_hash:{key} -> {value} ({param_hash})")

                serialized_params.append(param_hash)

        return serialized_params

    def __deflatten_multi_dict(self, multi_dict):
        params = {}
        for name, value in multi_dict.items(multi=True):
            if name not in params:
                params[name] = value
            else:
                if not isinstance(params[name], list):
                   params[name] = [params[name]]

                params[name].append(value)
        return params
