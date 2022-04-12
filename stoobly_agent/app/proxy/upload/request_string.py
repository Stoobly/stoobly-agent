import hashlib
import time
import pdb

from typing import Union

from .proxy_request import ProxyRequest

class RequestString:
    ENCODING = 'utf-8'
    REQUEST_TYPE = 1
    CLRF = "\r\n"

    __current_time = None

    def __init__(self, proxy_request: ProxyRequest):
        self.__current_time = self.__get_current_time()

        self.request = proxy_request.request
        self.proxy_request = proxy_request

        self.lines = []

        self.__request_line()
        self.__headers()
        self.__body()

        self.request_id = self.__generate_request_id()

    def get(self, **kwargs):
        if kwargs.get('control'):
            return self.CLRF.join([self.control()] + self.lines).encode(self.ENCODING)
        else:
            return self.CLRF.join(self.lines).encode(self.ENCODING)

    def control(self):
        return "{} {} {}".format(self.REQUEST_TYPE, self.request_id, self.__current_time)

    def __request_line(self):
        self.lines.append("{} {} HTTP/1.1".format(self.request.method, self.proxy_request.url()))

    def __headers(self):
        headers = self.request.headers

        for name, val in headers.items():
            line = ' '.join([
                "{}:".format(self.__to_header_case(self.__to_str(name))), 
                self.__to_str(val)
            ])
            self.lines.append(line)

    def __body(self):
        self.lines.append("{}{}".format(self.CLRF, self.request.body))

    def __to_header_case(self, header: str) -> str:
        toks = header.split('_')

        for index, tok in enumerate(toks):
            toks[index] = tok.lower().capitalize()

        return "-".join(toks)

    def __generate_request_id(self):
        joined_lines = self.CLRF.join(self.lines)
        return hashlib.md5(joined_lines.encode(self.ENCODING)).hexdigest()

    def __get_current_time(self):
        now = time.time()
        current_time = round(now * (pow(10, 9)))

        return current_time

    def __to_str(self, s: Union[bytes, str]):
        if isinstance(s, bytes):
            return s.decode('utf-8')
        return s
