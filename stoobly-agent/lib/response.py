# Modeled after Net::HTTP::Response

class Response:
    def __init__(self):
        self._code = 0
        self._headers = {}
        self._body = ''

    @property
    def code(self):
        return self._code

    @property
    def header(self):
        return self._headers

    @property
    def body(self):
        return self._body
