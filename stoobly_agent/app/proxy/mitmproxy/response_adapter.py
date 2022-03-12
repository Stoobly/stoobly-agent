from mitmproxy.net.http.response import Response as MitmproxyResponse 

from .response import Response

class MitmproxyResponseAdapter(Response):

    def __init__(self, response: MitmproxyResponse):
        self.response = response
        self.content = response.raw_content

        self.filter_rules = []
        self.rewrite_rules = []

    @property
    def code(self):
        return self.response.status_code

    @property
    def headers(self):
        return self.response.headers

    def decode_body(self):
        # Decodes content (if Content-Encoding header is set)
        self.content = self.response.content

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
    def filter(self, rules):
        if type(rules) == list:
            self.filter_rules = rules

        return self

    def rewrite(self, rules):
        if type(rules) == list:
            self.rewrite_rules = rules

        return self
