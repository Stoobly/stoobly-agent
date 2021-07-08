import re
import time
import pdb

class ResponseString:
    ENCODING = 'utf-8'
    RESPONSE_TYPE = 2
    CLRF = b"\r\n"

    def __init__(self, response, request_id):
        self.response = response
        self.lines = []
        self.latency = 0
        self.request_id = request_id

        self.response_line()
        self.headers()
        self.body()

    ###
    #
    # 1 - response type
    # 2 - request id
    # 3 - timestamp in nano seconds
    # 4 - response latency in nano seconds
    #
    def control(self):
        current_time = self.current_time()

        line = "{} {} {} {}".format(self.RESPONSE_TYPE, self.request_id, current_time, self.latency)
        self.lines.insert(0, line.encode(self.ENCODING))

    def response_line(self):
        line = "HTTP/1.1 {}".format(self.response.code)
        self.lines.append(line.encode(self.ENCODING))

    def headers(self):
        headers = self.response.headers

        for name, val in headers.items():
            line = "{}: {}".format(self.to_header_case(name), val)
            self.lines.append(line.encode(self.ENCODING))

    def body(self):
        body = self.response.body

        if not body:
            self.lines.append(self.CLRF)
        elif isinstance(body, bytes):
            self.lines.append(self.CLRF + body)
        else:
            raise Exception('Unsupported body type')

    def with_latency(self, latency):
        self.latency = latency

    def get(self):
        self.control()
        return self.CLRF.join(self.lines)

    def to_header_case(self, header):
        toks = re.split('_|-', header)
        if len(toks) == 1:
            return header

        for index, tok in enumerate(toks):
            toks[index] = tok.lower().capitalize()
        return "-".join(toks)

    def current_time(self):
        now = time.time()
        current_time = round(now * (pow(10, 6)))
        return current_time
