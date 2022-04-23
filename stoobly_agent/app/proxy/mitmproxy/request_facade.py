import cgi
import pdb
import re

from mitmproxy.net.http.request import Request as MitmproxyRequest
from mitmproxy.coretypes import multidict
from typing import Callable, List, Union
from urllib.parse import urlparse

from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.app.settings.filter_rule import FilterRule, ParameterRule

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
        value = self.headers.get('content-type')
        if not value:
            return ''

        return cgi.parse_header(value)[0]

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

    def with_rewrite_rules(self, rules: List[FilterRule]):
        if type(rules) == list:
            self.__rewrite_rules = self.select_parameter_rules(rules)
        return self 

    def with_redact_rules(self, rules: List[FilterRule]):
        if type(rules) == list:
            self.__redact_rules = self.select_parameter_rules(rules)
        return self

    def redact(self):
        redacts = self.__redact_rules
        if len(redacts) != 0:
            self.__redact_headers(redacts)
            self.__redact_content(redacts)

    def rewrite(self):
        rewrites = self.__rewrite_rules
        if len(rewrites) != 0:
            self.__rewrite_headers(rewrites)
            self.__rewrite_content(rewrites)

    def select_parameter_rules(self, redact_rules: List[FilterRule]) -> List[ParameterRule]:
        # Find all the rules that match request url and method
        rules = list(filter(self.__is_parameter_rule_selected, redact_rules or []))
        
        if len(rules) == 0:
            return []

        parameter_rules = list(map(lambda rule: rule.parameter_rules, rules))

        return [item for sublist in parameter_rules for item in sublist] # flatten filters_list

    def __is_parameter_rule_selected(self, redact_rule: FilterRule):
        url_matches = re.match(redact_rule.pattern, self.url)
        method_matches = self.method in redact_rule.methods
        return url_matches and method_matches

    
    def __apply_filters(self, params: dict, rewrites: List[ParameterRule], handler: Callable):
        if len(rewrites) == 0:
            return params

        for param_name in params:
            for rewrite in rewrites:
                val = params[param_name]

                # For body params, will be given of the form key => [param1, param2]
                if type(val) == list and len(val) == 1:
                    val = val[0]

                # Convert to bytes
                params[param_name] = handler(rewrite, param_name, val)

    def __rewrite_headers(self, rewrites: List[ParameterRule]):
        self.__apply_headers(rewrites, self.__rewrite_handler)

    def __rewrite_content(self, rewrites: List[ParameterRule]):
        self.__apply_content(rewrites, self.__rewrite_handler)

    def __redact_headers(self, filters: List[ParameterRule]):
        self.__apply_headers(filters, self.__redact_handler)

    def __redact_content(self, filters: List[ParameterRule]):
        self.__apply_content(filters, self.__redact_handler)

    def __apply_headers(self, rewrites: List[ParameterRule], handler: Callable):
        rewrites = list(filter(lambda rewrite: rewrite.type == request_component.HEADER, rewrites))
        return self.__apply_filters(self.request.headers, rewrites, handler)

    def __apply_content(self, rewrites: List[ParameterRule], handler: Callable):
        parsed_content = self.__body.get(self.content_type)

        if isinstance(parsed_content, dict) or isinstance(parsed_content, multidict.MultiDictView):
            rewrites = list(filter(lambda rewrite: rewrite.type == request_component.BODY_PARAM, rewrites))
            rewritten_params = self.__apply_filters(parsed_content, rewrites, handler)

            self.__body.set(rewritten_params, self.content_type)

    def __redact_applies(self, rewrite: ParameterRule, param_name):
        if isinstance(param_name, bytes):
            param_name = param_name.decode('utf-8')
        return re.match(rewrite.name, param_name)

    def __redact_handler(self, rewrite: ParameterRule, param_name, val: Union[bytes, str]) -> bytes:
        # If the rule does not apply, set the param
        if not self.__redact_applies(rewrite, param_name):
            return val.encode() if isinstance(val, str) else val
        else:
            return '[REDACTED]'.encode()

    def __rewrite_handler(self, rewrite: ParameterRule, param_name, val: Union[bytes, str]) -> bytes:
        if not self.__redact_applies(rewrite, param_name):
            return val.encode() if isinstance(val, str) else val
        else:
            return (rewrite.value or '').encode()