import hashlib
import pdb
import re

from urllib.parse import urlparse

from .request import Request
from .request_body_parser import RequestBodyParser

class MitmproxyRequestAdapter(Request):

    ###
    #
    # @param request [ActionDispatch::Request]
    #
    # @return [Hash]
    #
    def __init__(self, request):
        self.request = request
        self.param_filters = []

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
        if len(self.param_filters) == 0:
            return self.request.headers
        else:
            return self.filter_params(self.request.headers)

    @property
    def body(self):
        content = self.request.content

        if len(self.param_filters) == 0:
            try:
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
            except:
                content = ''.join(map(chr, content))

            return content
        else:
            parsed_content = RequestBodyParser.parse(content, self.content_type)
            if type(parsed_content) == dict:
                if len(content) > 0:
                    pdb.set_trace()
                filtered_params = self.filter_params(parsed_content, self.content_type)
                return RequestBodyParser.stringify(filtered_params, self.content_type)
            else:
                return content

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

    ##
    #
    # @param filters [Array<string>]
    #
    def with_param_filters(self, filters):
        if type(filters) == list:
            self.param_filters = filters

        return self

    ##
    #
    # @param filters [Dict]
    #
    def filter_params(self, params, content_type = None):
        filtered_params = {}
        for param_name in params:
            for pattern in self.param_filters:
                val = params[param_name]

                # For body params, will be given of the form key => [param1, param2]
                if type(val) == list and len(val) == 1:
                    val = val[0]

                if not re.match(pattern, param_name):
                    filtered_params[param_name] = val
                else:
                    if type(val) == list:
                        filtered_params[param_name] = list(map(lambda v: self.hash_param(param_name, v, content_type), val))
                    else:
                        filtered_params[param_name] = self.hash_param(param_name, val, content_type)
        return filtered_params


    def hash_param(self, param_name, param, content_type = None):
        if type(param) == list:
            param = param[0]

        encoded_param = RequestBodyParser.stringify({param_name: param}, content_type)

        param_len = len(param)
        val = param_name + param[0:2] + str(param_len)
        h = hashlib.md5(val.encode()).hexdigest()
        encoded_hashed_param = RequestBodyParser.stringify({param_name: h}, content_type)

        len_diff = len(encoded_param) - len(encoded_hashed_param)
        if len_diff < 0:
            return h[0:(param_len + len_diff)]
        else:
            return h + ('_' * len_diff)

