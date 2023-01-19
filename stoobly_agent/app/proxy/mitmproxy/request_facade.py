import pdb
import re

from mitmproxy.http import Headers, Request as MitmproxyRequest
from mitmproxy.coretypes import multidict
from typing import Callable, List, Union
from urllib.parse import urlparse

from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.app.settings.rewrite_rule import RewriteRule, ParameterRule
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.logger import Logger, bcolors
from stoobly_agent.lib.utils import jmespath

from .request_body_facade import MitmproxyRequestBodyFacade
from .request import Request

class MitmproxyRequestFacade(Request):

    ###
    #
    # @param request [ActionDispatch::Request]
    #
    # @return [Hash]
    #
    def __init__(self, request: MitmproxyRequest):
        self.request = request
        self.__redact_rules: List[ParameterRule] = []
        self.__rewrite_rules: List[ParameterRule] = []

        self.__body = MitmproxyRequestBodyFacade(request)

    @property
    def url(self):
        return self.request.url

    @property
    def path(self):
        uri = urlparse(self.request.path)
        return uri.path

    @property
    def base_url(self):
        return f"{self.request.scheme}://{self.request.host}:{self.request.port}"

    @property
    def method(self):
        return self.request.method

    @property
    def headers(self):
        return self.__filter_custom_headers(self.request.headers)

    @property
    def body(self):
        content = self.request.raw_content

        try:
            if isinstance(content, bytes):
                content = content.decode('utf-8')
        except:
            content = ''.join(map(chr, content))

        return content

    @property
    def parsed_body(self):
        return self.__body.get(self.content_type)

    @property
    def query(self):
        return self.request.query

    @property
    def query_string(self):
        from urllib.parse import urlencode
        return urlencode(self.query)

    @property
    def content_type(self):
        return self.headers.get('content-type')

    @property
    def host(self):
        return self.request.host

    @property
    def port(self):
        return self.request.port

    @property
    def redact_rules(self) -> List[ParameterRule]:
        return self.__redact_rules
    
    @property
    def rewrite_rules(self) -> List[ParameterRule]:
        return self.__rewrite_rules

    def with_rewrite_rules(self, rules: List[RewriteRule]):
        if type(rules) == list:
            self.__rewrite_rules = self.select_parameter_rules(rules)
        return self 

    def with_redact_rules(self, rules: List[RewriteRule]):
        if type(rules) == list:
            self.__redact_rules = self.select_parameter_rules(rules)
        return self

    def redact(self):
        redacts = self.__redact_rules
        if len(redacts) != 0:
            self.__redact_headers(redacts)
            self.__redact_query(redacts)
            self.__redact_content(redacts)

    def rewrite(self):
        rewrites = self.__rewrite_rules
        if len(rewrites) != 0:
            self.__rewrite_headers(rewrites)
            self.__rewrite_query(rewrites)
            self.__rewrite_content(rewrites)

    def select_parameter_rules(self, rules: List[RewriteRule]) -> List[ParameterRule]:
        # Find all the rules that match request url and method
        _rules = list(filter(self.__is_parameter_rule_selected, rules or []))
        
        if len(_rules) == 0:
            return []

        parameter_rules = list(map(lambda rule: rule.parameter_rules, _rules))

        return [item for sublist in parameter_rules for item in sublist] # flatten list

    def __is_parameter_rule_selected(self, rewrite_rule: RewriteRule):
        pattern = rewrite_rule.pattern

        try:
            url_matches = re.match(pattern, self.url)
        except re.error as e:
            Logger.instance().error(f"RegExp error '{e}' for {pattern}")
            return False

        method = self.method.upper()
        method_matches = method in rewrite_rule.methods
        return url_matches and method_matches
    
    def __apply_rewrites(self, params: dict, rewrites: List[ParameterRule], handler: Callable):
        if len(rewrites) == 0:
            return

        for rewrite in rewrites:
            jmespath.search(rewrite.name, params, {
                'replacements': [handler(rewrite) if handler else rewrite.value]
            })

    def __rewrite_handler(self, rewrite: ParameterRule) -> str:
        Logger.instance().debug(f"{bcolors.OKCYAN}Rewriting{bcolors.ENDC} {rewrite.name} => {rewrite.value}")
        return rewrite.value

    def __rewrite_headers(self, rewrites: List[ParameterRule]):
        self.__apply_headers(rewrites, self.__rewrite_handler)

    def __rewrite_query(self, rewrites: List[ParameterRule]):
        self.__apply_queries(rewrites, self.__rewrite_handler)

    def __rewrite_content(self, rewrites: List[ParameterRule]):
        self.__apply_content(rewrites, self.__rewrite_handler)

    def __redact_handler(self, rewrite: ParameterRule) -> str:
        Logger.instance().debug(f"{bcolors.OKCYAN}Redacting{bcolors.ENDC} {rewrite.name}")
        return '[REDACTED]'

    def __redact_headers(self, redacts: List[ParameterRule]):
        self.__apply_headers(redacts, self.__redact_handler)

    def __redact_query(self, redacts: List[ParameterRule]):
        self.__apply_queries(redacts, self.__redact_handler)

    def __redact_content(self, redacts: List[ParameterRule]):
        self.__apply_content(redacts, self.__redact_handler)

    def __apply_headers(self, rewrites: List[ParameterRule], handler: Callable):
        rewrites = list(filter(lambda rewrite: rewrite.type == request_component.HEADER, rewrites))
        self.__apply_rewrites(self.request.headers, rewrites, handler)

    def __apply_queries(self, rewrites: List[ParameterRule], handler: Callable):
        rewrites = list(filter(lambda rewrite: rewrite.type == request_component.QUERY_PARAM, rewrites))
        self.__apply_rewrites(self.request.query, rewrites, handler)

    def __apply_content(self, rewrites: List[ParameterRule], handler: Callable):
        parsed_content = self.__body.get(self.content_type)

        if isinstance(parsed_content, dict) or isinstance(parsed_content, multidict.MultiDictView):
            rewrites = list(filter(lambda rewrite: rewrite.type == request_component.BODY_PARAM, rewrites))
            self.__apply_rewrites(parsed_content, rewrites, handler)

            self.__body.set(parsed_content, self.content_type)

    def __filter_custom_headers(self, request_headers: Headers):
        '''
        Remove custom headers
        '''
        _request_headers = Headers(**request_headers)

        headers = custom_headers.__dict__
        for key in headers:
            if key[0:2] == '__' and key[-2:] == '__':
                continue

            name = headers[key]

            if name not in request_headers:
                continue

            _request_headers.pop(name)

        return _request_headers