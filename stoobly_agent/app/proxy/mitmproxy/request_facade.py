import json
import pdb
import re

from mitmproxy.http import Headers, Request as MitmproxyRequest
from mitmproxy.coretypes import multidict
from typing import Callable, List
from urllib.parse import urlparse

from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.app.settings.rewrite_rule import ParameterRule, RewriteRule, UrlRule 
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.logger import Logger, bcolors
from stoobly_agent.lib.utils import jmespath
from stoobly_agent.lib.utils.decode import decode

from .request_body_facade import MitmproxyRequestBodyFacade
from .request import Request

LOG_ID = 'Request'

class MitmproxyRequestFacade(Request):

    ###
    #
    # @param request [ActionDispatch::Request]
    #
    # @return [Hash]
    #
    def __init__(self, request: MitmproxyRequest):
        self.__url_rules: List[UrlRule] = []
        self.__parameter_rules: List[ParameterRule] = []

        self.request = request
        self.uri = urlparse(self.request.url)
        self.__body = MitmproxyRequestBodyFacade(request)

    @property
    def http_version(self):
        return self.request.http_version

    @property
    def url(self):
        uri = self.uri._replace(path=self.uri.path.rstrip('/'))
        return uri.geturl()

    @property
    def password(self):
        return self.uri.password

    @property
    def username(self):
        return self.uri.username

    @property
    def path(self):
        return self.uri.path

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
        content = self.request.raw_content or ''

        return decode(content)

    @property
    def parsed_body(self):
        return self.__body.get(self.content_type)

    @property
    def query(self):
        return self.request.query

    @property
    def query_string(self):
        from urllib.parse import quote

        params = []
        for k in self.query.keys():
            for v in self.query.get_all(k):
                params.append(f"{quote(k)}={quote(v)}")
        
        return '&'.join(params)

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
    def url_rules(self) -> List[ParameterRule]:
        return self.__url_rules
    
    @property
    def parameter_rules(self) -> List[ParameterRule]:
        return self.__parameter_rules

    @property
    def scheme(self):
        return self.request.scheme

    def with_parameter_rules(self, rules: List[RewriteRule]):
        if type(rules) == list:
            self.__parameter_rules = self.select_parameter_rules(rules)
        return self 

    def with_url_rules(self, rules: List[RewriteRule]):
        if type(rules) == list:
            self.__url_rules = self.select_url_rules(rules)
        return self

    def rewrite(self):
        rewrites = self.__parameter_rules

        if len(rewrites) != 0:
            self.__rewrite_headers(rewrites)
            self.__rewrite_query(rewrites)
            self.__rewrite_content(rewrites)

        rewrites = self.__url_rules

        if len(rewrites):
            self.__rewrite_url(rewrites)
            Logger.instance(LOG_ID).debug(f"{bcolors.OKBLUE} Rewritten URL{bcolors.ENDC} {self.url}")

    # Find all the rules that match request url and method
    def select_rewrite_rules(self, rules: List[RewriteRule]) -> List[RewriteRule]:
        return list(filter(self.__is_rewrite_rule_selected, rules or []))

    def select_parameter_rules(self, rules: List[RewriteRule]) -> List[ParameterRule]:
        _rules = self.select_rewrite_rules(rules)
        
        if len(_rules) == 0:
            return []

        parameter_rules = list(map(lambda rule: rule.parameter_rules, _rules))

        return [item for sublist in parameter_rules for item in sublist] # flatten list

    def select_url_rules(self, rules: List[RewriteRule]) -> List[UrlRule]:
        _rules = self.select_rewrite_rules(rules)

        if len(_rules) == 0:
            return []

        url_rules = list(map(lambda rule: rule.url_rules, _rules))

        return [item for sublist in url_rules for item in sublist] # flatten list

    def __is_rewrite_rule_selected(self, rewrite_rule: RewriteRule):
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
                'replacements': [handler(rewrite) if handler else rewrite.value],
            })

    def __rewrite_handler(self, rewrite: ParameterRule) -> str:
        Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Rewriting{bcolors.ENDC} {rewrite.type.lower()} {rewrite.name} => {rewrite.value}")
        return rewrite.value

    def __rewrite_url(self, rewrites: List[UrlRule]):
        for rewrite in rewrites:
            if rewrite.hostname:
                self.request.host = rewrite.hostname
            
            if rewrite.port:
                self.request.port = int(rewrite.port)

            if rewrite.scheme:
                self.request.scheme = rewrite.scheme.lower()

            if rewrite.path:
                path = rewrite.path
                if path[0] != '/':
                    path = '/' + path

                if self.uri.query:
                    self.request.path = f"{path}?{self.uri.query}"
                else:
                    self.request.path = path

        self.uri = urlparse(self.request.url)

    def __rewrite_headers(self, rewrites: List[ParameterRule]):
        self.__apply_headers(rewrites, self.__rewrite_handler)

    def __rewrite_query(self, rewrites: List[ParameterRule]):
        self.__apply_queries(rewrites, self.__rewrite_handler)

    def __rewrite_content(self, rewrites: List[ParameterRule]):
        self.__apply_content(rewrites, self.__rewrite_handler)

    def __apply_headers(self, rewrites: List[ParameterRule], handler: Callable):
        rewrites = list(filter(lambda rewrite: rewrite.type == request_component.HEADER, rewrites))
        self.__apply_rewrites(self.request.headers, rewrites, handler)

    def __apply_queries(self, rewrites: List[ParameterRule], handler: Callable):
        rewrites = list(filter(lambda rewrite: rewrite.type == request_component.QUERY_PARAM, rewrites))
        self.__apply_rewrites(self.request.query, rewrites, handler)

    def __apply_content(self, rewrites: List[ParameterRule], handler: Callable):
        rewrites = list(filter(lambda rewrite: rewrite.type == request_component.BODY_PARAM, rewrites))
        if len(rewrites) == 0:
            return

        content_type = self.content_type
        parsed_content = self.__body.get(content_type)

        if not isinstance(parsed_content, dict) and not isinstance(parsed_content, multidict.MultiDictView):
            content_type = 'application/json'
            self.request.headers['content-type'] = content_type
            parsed_content = {}

        self.__apply_rewrites(parsed_content, rewrites, handler)
        self.__body.set(parsed_content, content_type)

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