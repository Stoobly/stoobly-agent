import time
import uuid
import pdb

from typing import Union

from stoobly_agent.lib.utils.decode import decode

from .proxy_request import ProxyRequest
from .request_string_control import RequestStringControl

CLRF = b"\r\n"

class RequestString:
    ENCODING = 'utf-8'

    __current_time = None
    request_id = None

    def __init__(self, proxy_request: ProxyRequest):
        self.__current_time = self.__get_current_time()

        self.lines = []

        if proxy_request:
            self.request = proxy_request.request
            self.proxy_request = proxy_request

            self.__request_line()
            self.__headers()
            self.__body()

            self.request_id = proxy_request.id

        self.request_id = self.request_id or self.__generate_request_id()

    def get(self, **kwargs):
        if kwargs.get('control'):
            return CLRF.join([self.control] + self.lines)
        else:
            return CLRF.join(self.lines)

    def set(self, s: bytes):
        self.lines = s.split(CLRF)

    @property
    def control(self):
        control = RequestStringControl()
        control.id = self.request_id
        control.timestamp = self.__current_time
        return control.serialize().encode(self.ENCODING)

    @control.setter
    def control(self, c: str):
        control = RequestStringControl(c)
        self.request_id = control.id
        self.__current_time = control.timestamp

    def __request_line(self):
        line = "{} {} HTTP/1.1".format(self.request.method, self.proxy_request.url())
        self.lines.append(line.encode(self.ENCODING))

    def __headers(self):
        headers = self.request.headers

        for name, val in headers.items():
            if 'content-encoding' in headers:
                # self.request.body will decode content-encoding
                # to maintain internal consistency, remove this header since it will be decoded
                print(self.request.body)
                pass

            line = ' '.join([
                "{}:".format(self.__to_header_case(self.__to_str(name))), 
                self.__to_str(val)
            ])
            self.lines.append(line.encode(self.ENCODING))

    def __body(self):
        self.lines.append(CLRF + self.request.body)

    def __to_header_case(self, header: str) -> str:
        toks = header.split('_')

        for index, tok in enumerate(toks):
            toks[index] = tok.lower().title()

        return "-".join(toks)

    def __generate_request_id(self):
        return str(uuid.uuid4())

    def __get_current_time(self):
        now = time.time()
        current_time = round(now * (pow(10, 9)))

        return current_time

    def __to_str(self, s: Union[bytes, str]):
        return decode(s)
