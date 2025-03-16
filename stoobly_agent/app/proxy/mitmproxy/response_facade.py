import pdb

from mitmproxy.http import Headers, Response as MitmproxyResponse
from mitmproxy.coretypes import multidict
from typing import Callable, List

from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.app.settings.rewrite_rule import ParameterRule, RewriteRule
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.logger import Logger, bcolors
from stoobly_agent.lib.utils import jmespath
from stoobly_agent.lib.utils.decode import decode

from .request_facade import MitmproxyRequestFacade
from .response_body_facade import MitmproxyResponseBodyFacade
from .response import Response

LOG_ID = 'Response'

class MitmproxyResponseFacade(Response):

    def __init__(self, response: MitmproxyResponse):
        self.response = response

        self.__body = MitmproxyResponseBodyFacade(response)
        self.__parameter_rules: List[ParameterRule] = []

    @property
    def code(self):
        return self.response.status_code

    @property
    def content_type(self):
        return self.headers.get('content-type')

    @property
    def headers(self):
        return self.__filter_custom_headers(self.response.headers)

    @property
    def body(self):
        return self.response.raw_content or ''

    @property
    def http_verison(self):
        return self.response.http_version

    def decode_body(self):
        # Decodes content (if Content-Encoding header is set)
        self.content = self.response.content

        # Update Content-Lenght header to decoded content length
        self.response.headers['content-length'] = str(len(self.content))

    def with_parameter_rules(self, rules: List[RewriteRule], request_facade: MitmproxyRequestFacade):
        if type(rules) == list:
            self.__parameter_rules = request_facade.select_parameter_rules(rules)
        return self 

    def rewrite(self):
        rewrites = self.__parameter_rules

        if len(rewrites) != 0:
            self.__rewrite_headers(rewrites)
            self.__rewrite_content(rewrites)
    
    def __apply_rewrites(self, params: dict, rewrites: List[ParameterRule], handler: Callable):
        if len(rewrites) == 0:
            return

        for rewrite in rewrites:
            jmespath.search(rewrite.name, params, {
                'replacements': [handler(rewrite) if handler else rewrite.value],
            })

    def __rewrite_handler(self, rewrite: ParameterRule) -> str:
        Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Rewriting{bcolors.ENDC} {rewrite.type.lower()} {rewrite.name} => {rewrite.value}")
        return rewrite.value

    def __rewrite_headers(self, rewrites: List[ParameterRule]):
        self.__apply_headers(rewrites, self.__rewrite_handler)

    def __rewrite_content(self, rewrites: List[ParameterRule]):
        self.__apply_content(rewrites, self.__rewrite_handler)

    def __apply_headers(self, rewrites: List[ParameterRule], handler: Callable):
        rewrites = list(filter(lambda rewrite: rewrite.type == request_component.RESPONSE_HEADER, rewrites))
        self.__apply_rewrites(self.response.headers, rewrites, handler)

    def __apply_content(self, rewrites: List[ParameterRule], handler: Callable):
        rewrites = list(filter(lambda rewrite: rewrite.type == request_component.RESPONSE_PARAM, rewrites))
        if len(rewrites) == 0:
            return

        content_type = self.content_type
        parsed_content = self.__body.get(content_type)

        if not self.__is_iterable(parsed_content):
            return 

        self.__apply_rewrites(parsed_content, rewrites, handler)
        self.__body.set(parsed_content, content_type)

    def __filter_custom_headers(self, response_headers: Headers):
        '''
        Remove custom headers
        '''
        _response_headers = Headers(**response_headers)

        headers = custom_headers.__dict__
        for key in headers:
            if key[0:2] == '__' and key[-2:] == '__':
                continue

            name = headers[key]

            if name not in response_headers:
                continue

            _response_headers.pop(name)

        return _response_headers

    def __is_iterable(self, v):
        return isinstance(v, dict) or isinstance(v, multidict.MultiDictView) or isinstance(v, list)