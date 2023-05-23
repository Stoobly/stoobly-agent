import time

from .proxy_request import ProxyRequest
from .request_string import RequestString
from .response_string import ResponseString

ENCODING = 'utf-8'
REQUEST_DELIMITTER = '\n🐵🙈🙉\n'.encode(ENCODING)

class JoinedRequest:
    __request_string = None
    __response_string = None

    def __init__(self, proxy_request: ProxyRequest = None):
        self.timestamp = time.time()
        self.proxy_request = proxy_request

        if proxy_request:
            self.__request_string = RequestString(proxy_request)

    @property
    def request_string(self):
        return self.__request_string

    @request_string.setter
    def request_string(self, s: str):
        self.__request_string = s

    @property
    def response_string(self):
        return self.__response_string

    @response_string.setter
    def response_string(self, s: str):
        self.__response_string = s

    def with_response(self, response):
        now = time.time()

        self.__response_string = ResponseString(response, self.__request_string.request_id)

        # milliseconds
        latency = round((now - self.timestamp) * (10 ** 6))
        self.__response_string.with_latency(latency)

        return self

    def build(self):
        if not self.response_string:
            raise Exception('Missing response')

        request_string = self.__request_string.get(control=True)
        response_string = self.__response_string.get(control=True)

        joined = REQUEST_DELIMITTER.join([request_string, response_string])
        return joined
