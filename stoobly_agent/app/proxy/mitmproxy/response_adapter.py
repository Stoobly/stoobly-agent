from mitmproxy.http import Response as MitmproxyResponse

from stoobly_agent.app.settings.rewrite_rule import RewriteRule 

from .response import Response

class MitmproxyResponseAdapter(Response):

    def __init__(self, response: MitmproxyResponse):
        self.response = response
        self.content = response.raw_content

        self.rewrite_rules = []
        self.rewrite_rules = []

    @property
    def code(self):
        return self.response.status_code

    @property
    def headers(self):
        return self.response.headers

    @property
    def body(self):
        content = self.content

        if not content:
            return b''

        return content

    def decode_body(self):
        # Decodes content (if Content-Encoding header is set)
        self.content = self.response.content

        # Update Content-Lenght header to decoded content length
        self.response.headers['content-length'] = str(len(self.content))

    
    def with_redact_rules(self, rules: RewriteRule):
        if type(rules) == list:
            self.rewrite_rules = rules

        return self

    def with_rewrite_rules(self, rules: RewriteRule):
        if type(rules) == list:
            self.rewrite_rules = rules

        return self

    # TODO
    def redact(self):
        pass
    
    # TODO
    def rewrite(self):
        pass
