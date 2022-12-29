import re
import time
import pdb

from .response_string_control import ResponseStringControl

CLRF = b"\r\n"

class ResponseString:
    ENCODING = 'utf-8'
    RESPONSE_TYPE = 2

    __current_time = None

    def __init__(self, response, request_id):
        self.__current_time = self.__get_current_time()

        self.response = response
        self.lines = []
        self.latency = 0
        self.request_id = request_id

        if response:
            self.__response_line()
            self.__headers()
            self.__body()

    def get(self, **kwargs):
        if kwargs.get('control'):
            return CLRF.join([self.control] + self.lines)
        else:
            return CLRF.join(self.lines)

    def set(self, s: bytes):
        if not isinstance(s, bytes):
            s = s.encode(self.ENCODING)

        self.lines = s.split(CLRF)

    ###
    #
    # 1 - response type
    # 2 - request id
    # 3 - timestamp in nano seconds
    # 4 - response latency in nano seconds
    #
    @property
    def control(self):
        control = ResponseStringControl()
        control.id = self.request_id
        control.timestamp = self.__current_time
        control.latency = self.latency

        return control.serialize().encode(self.ENCODING)

    @control.setter
    def control(self, c):
        control = ResponseStringControl(c)
        self.request_id = control.id
        self.__current_time = control.timestamp
        self.latency = control.latency

    def with_latency(self, latency):
        self.latency = latency
        return self

    def with_request_id(self, request_id):
        self.request_id = request_id
        return self

    def __response_line(self):
        line = "HTTP/1.1 {}".format(self.response.code)
        self.lines.append(line.encode(self.ENCODING))

    def __headers(self):
        headers = self.response.headers

        for name, val in headers.items():
            line = "{}: {}".format(self.__to_header_case(name), val)
            self.lines.append(line.encode(self.ENCODING))

    def __body(self):
        body = self.response.body

        if not body:
            self.lines.append(CLRF)
        elif isinstance(body, bytes):
            self.lines.append(CLRF + body)
        else:
            raise Exception('Unsupported body type')

    def __to_header_case(self, header):
        toks = re.split('_|-', header)
        if len(toks) == 1:
            return header

        for index, tok in enumerate(toks):
            toks[index] = tok.lower().capitalize()
        return "-".join(toks)

    def __get_current_time(self):
        now = time.time()
        current_time = round(now * (pow(10, 6)))
        return current_time
