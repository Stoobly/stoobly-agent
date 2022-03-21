import re
import time
import pdb

class ResponseString:
    ENCODING = 'utf-8'
    RESPONSE_TYPE = 2
    CLRF = b"\r\n"

    __current_time = None

    def __init__(self, response, request_id):
        self.__current_time = self.__get_current_time()

        self.response = response
        self.lines = []
        self.latency = 0
        self.request_id = request_id

        self.__response_line()
        self.__headers()
        self.__body()

    def get(self, **kwargs):
        if kwargs.get('control'):
            return self.CLRF.join([self.control()] + self.lines)
        else:
            return self.CLRF.join(self.lines)

    ###
    #
    # 1 - response type
    # 2 - request id
    # 3 - timestamp in nano seconds
    # 4 - response latency in nano seconds
    #
    def control(self):
        line = "{} {} {} {}".format(self.RESPONSE_TYPE, self.request_id, self.__current_time, self.latency)
        return line.encode(self.ENCODING)

    def with_latency(self, latency):
        self.latency = latency

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
            self.lines.append(self.CLRF)
        elif isinstance(body, bytes):
            self.lines.append(self.CLRF + body)
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
