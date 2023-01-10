import json
import mimetypes
import os
import pdb
import requests

from http.server import BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def render(self, **kwargs):
        if kwargs.get('file') != None:
            self.render_file(kwargs)
        elif kwargs.get('json') != None:
            self.render_json(kwargs)
        elif kwargs.get('plain') != None:
            self.render_plain(kwargs)
        elif kwargs.get('data') != None:
            self.render_data(kwargs)

    def render_file(self, kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {}

        path = kwargs['file']

        if not os.path.exists(path):
            kwargs['status'] = 404

        mimetype = mimetypes.guess_type(path)[0]
        kwargs['headers']['Content-Type'] = mimetype or 'text/plain'

        fp = open(path, 'rb')
        kwargs['data'] = fp.read()
        self.render_data(kwargs)

    def render_json(self, kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['Content-Type'] = 'application/json'
        kwargs['data'] = json.dumps(kwargs['json'])
        self.render_data(kwargs)

    def render_plain(self, kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['Content-Type'] = 'text/plain'
        kwargs['data'] = kwargs['plain']
        self.render_data(kwargs)

    def render_data(self, kwargs):
        self.send_response(kwargs.get('status') or 200)

        body = b''
        if isinstance(kwargs['data'], str):
            body = kwargs['data'].encode()
        else:
            body = kwargs['data']

        # Send headers
        headers = self.filter_headers(kwargs.get('headers'), {
            'TRANSFER-ENCODING': 'CHUNKED',
        })
        headers['Content-Length'] = len(body)

        self.enable_cors(headers)
        self.render_headers(headers)
        self.end_headers()

        # Send body
        self.wfile.write(body)

    def pass_on(self, res: requests.Request):
        self.render(
            headers = res.headers,
            data = res.raw.data,
            status = res.status_code,
        )

    def bad_request(self, message = ''):
        self.render(
            plain = message,
            status = 400
        )

    def not_found(self, message = ''):
        self.render(
            plain = message,
            status = 404
        )

    def internal_error(self, message = ''):
        self.render(
            plain = message,
            status = 500
        )

    def filter_headers(self, headers, blacklist = {}):
        if not headers:
            return {}

        new_blacklist = {}
        for key, val in blacklist.items():
            new_blacklist[key.upper()] = val

        new_headers = headers.copy()
        for key, val in headers.items():
            if key.upper() in new_blacklist:
                if not new_blacklist[key.upper()]:
                    del new_headers[key.upper()]
                elif val.upper() == new_blacklist[key.upper()]:
                    del new_headers[key.upper()]

        return new_headers


    def render_headers(self, headers):
        if headers:
            for key, val in headers.items():
                self.send_header(key, val)

    def required_params(self, params: dict, required_params: list):
        if not isinstance(params, dict):
            self.not_found(f"Body is empty")
            return False

        for param in required_params:
            if param not in params:
                self.bad_request(f"Missing param {param}")
                return False

        return True

    def enable_cors(self):
        pass