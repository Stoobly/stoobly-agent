import base64
import pdb

from .response import  Response

class MitmproxyResponseAdapter(Response):

    def __init__(self, response):
        self.response = response
        self.content = response.raw_content
        self.param_filters = []

    @property
    def code(self):
        return self.response.status_code

    @property
    def headers(self):
        return self.response.headers

    def decode_body(self):
        # Decodes content (if Content-Encoding header is set)
        self.content = response.content

        # Update Content-Lenght header to decoded content length
        self.response.headers['content-length'] = str(len(self.content))

    @property
    def body(self):
        content = self.content

        if not content:
            return b''

        return content

    ###
    #
    # @param filters [Array<string>]
    #
    def with_param_filters(self, filters):
        if type(filters) == list:
            self.param_filters = filters

        return self
