from ast import Call
import hashlib
import pdb
import re

from mitmproxy.net.http.request import Request as MitmproxyRequest
from mitmproxy.coretypes import multidict
from typing import Callable, List, Union
from urllib.parse import urlparse

from stoobly_agent.lib.settings import Component, FilterRule, Rewrite, RewriteRule, Rule

from .request_body_facade import MitmproxyRequestBodyFacade
from .request import Request

class MitmproxyRequestAdapter(Request):

    ###
    #
    # @param request [ActionDispatch::Request]
    #
    # @return [Hash]
    #
    def __init__(self, request: MitmproxyRequest):
        self.request = request
        self.filter_rules: List[FilterRule] = []
        self.rewrite_rules: List[RewriteRule] = []

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
        return self.request.headers

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
    def content_type(self):
        for key, value in self.headers.items():
            if key.lower() == 'content-type':
                return value
        return ''

    @property
    def host(self):
        return self.request.host

    @property
    def port(self):
        return self.request.port

    @property
    def relevant_filter_rules(self) -> List[FilterRule]:
        method = self.method
        url = self.url

        filter_matches = lambda filter_rule: re.match(filter_rule.get('pattern'), url) and filter_rule.get('method') == method
        return list(filter(filter_matches, self.filter_rules or []))
    
    @property
    def relevant_rewrites(self) -> List[RewriteRule]:
        method = self.method
        url = self.url

        rewrite_matches = lambda rewrite_rule: re.match(rewrite_rule.get('pattern'), url) and rewrite_rule.get('method') == method
        rewrite_rules = list(filter(rewrite_matches, self.rewrite_rules or []))

        if len(rewrite_rules) == 0:
            return []

        rewrite_list = map(lambda rewrite_rule: rewrite_rule.get('rewrites'), rewrite_rules)
        return [item for sublist in rewrite_list for item in sublist] # flatten filters_list
    
    def filter(self, filter_rules: List[FilterRule]):
        self.filter_rules = filter_rules

        relevant_filter_rules = self.relevant_filter_rules
        if len(relevant_filter_rules) == 0:
            return self

        filters_list = map(lambda filter_rule: filter_rule.get('filters'), relevant_filter_rules)
        filters = [item for sublist in filters_list for item in sublist] # flatten filters_list

        self.request.headers = self.__filter_headers(filters)
        self.__filter_content(filters)

    def rewrite(self, rules: List[RewriteRule]):
        if type(rules) == list:
            self.rewrite_rules = rules

        rewrites = self.relevant_rewrites
        if len(rewrites) != 0:
            self.__rewrite_headers(rewrites)
            self.__rewrite_content(rewrites)

    def __rewrite_headers(self, rewrites: List[Rewrite]):
        self.request.headers = self.__apply_headers(rewrites, self.__rewrite_handler)

    def __rewrite_content(self, rewrites: List[Rewrite]):
        self.__apply_content(rewrites, self.__rewrite_handler)

    def __filter_headers(self, filters: List[Rewrite]):
        self.request.headers = self.__apply_headers(filters, self.__filter_handler)

    def __filter_content(self, filters: List[Rewrite]):
        self.__apply_content(filters, self.__filter_handler)

    def __apply_headers(self, rewrites: List[Rewrite], handler: Callable):
        rewrites = list(filter(lambda f: f['type'] == Component['Header'], rewrites))
        return self.__apply_filters(self.request.headers, rewrites, handler)

    def __apply_content(self, rewrites: List[Rewrite], handler: Callable):
        parsed_content = self.__body.get(self.content_type)

        if isinstance(parsed_content, dict) or isinstance(parsed_content, multidict.MultiDictView):
            rewrites = list(filter(lambda f: f['type'] == Component['BodyParam'], rewrites))
            rewritten_params = self.__apply_filters(parsed_content, rewrites, handler)

            self.__body.set(rewritten_params, self.content_type)

    ##
    #
    # @param filters [Dict]
    #
    def __apply_filters(self, params, rewrites: List[Rewrite], handler: Callable):
        if len(rewrites) == 0:
            return params

        rewritten_params = {}

        for param_name in params:
            for rewrite in rewrites:
                val = params[param_name]

                # For body params, will be given of the form key => [param1, param2]
                if type(val) == list and len(val) == 1:
                    val = val[0]

                # Convert to bytes
                rewritten_params[param_name] = handler(rewrite, param_name, val)

        return rewritten_params

    def __filter_applies(self, rewrite: Rewrite, param_name):
        if isinstance(param_name, bytes):
            param_name = param_name.decode('utf-8')
        return re.match(rewrite['name'], param_name)

    def __filter_handler(self, rewrite: Rewrite, param_name, val: Union[bytes, str]) -> bytes:
        # If the rule does not apply, set the param
        if not self.__filter_applies(rewrite, param_name):
            return val.encode() if isinstance(val, str) else val
        else:
            return '[FILTERED]'.encode()

    def __rewrite_handler(self, rewrite: Rewrite, param_name, val: Union[bytes, str]) -> bytes:
        if not self.__filter_applies(rewrite, param_name):
            return val.encode() if isinstance(val, str) else val
        else:
            return (rewrite['value'] or '').encode()