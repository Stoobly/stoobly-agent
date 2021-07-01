import hashlib
import time
import pdb

class RequestString:
    ENCODING = 'utf-8'
    REQUEST_TYPE = 1
    CLRF = "\r\n"

    def __init__(self, proxy_request):
        self.request = proxy_request.request
        self.proxy_request = proxy_request

        self.lines = []

        self.request_line()
        self.headers()
        self.body()

        self.request_id = self.generate_request_id()
        self.control()

    def get(self):
        return self.CLRF.join(self.lines).encode(self.ENCODING)

    def control(self):
        current_time = self.current_time()
        self.lines.insert(0, "{} {} {}".format(self.REQUEST_TYPE, self.request_id, current_time))


    def request_line(self):
        self.lines.append("{} {} HTTP/1.1".format(self.request.method, self.proxy_request.url()))

    def headers(self):
        _headers = self.request.headers

        for name, val in _headers.items():
            line = ' '.join(["{}:".format(self.to_header_case(name)), val])
            self.lines.append(line)

    def body(self):
        self.lines.append("{}{}".format(self.CLRF, self.request.body))

    def to_header_case(self, header):
        toks = header.split('_')

        for index, tok in enumerate(toks):
            toks[index] = tok.lower().capitalize()

        return "-".join(toks)

    def generate_request_id(self):
        joined_lines = self.CLRF.join(self.lines)
        return hashlib.md5(joined_lines.encode(self.ENCODING)).hexdigest()

    def current_time(self):
        now = time.time()
        current_time = round(now * (pow(10, 9)))

        return current_time
