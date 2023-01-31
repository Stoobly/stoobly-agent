import os
import pdb
import re

from mergedeep import merge
from mitmproxy.coretypes.multidict import MultiDict
from urllib.parse import urlparse, parse_qs

from stoobly_agent.app.proxy.replay.body_parser_service import decode_response
from stoobly_agent.config.constants import headers

from .routes import ROUTES
from .simple_http_request_handler import SimpleHTTPRequestHandler

class ApplicationHTTPRequestHandler(SimpleHTTPRequestHandler):
    ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')

    @property
    def public_dir(self):
        return os.path.join(self.ROOT_DIR, 'public')

    ### Method handlers

    def do_OPTIONS(self):
        self.render(
            plain = 'OK',
            status = 200
        )

    def do_POST(self):
        self.preprocess()

        self.body = self.parse_body()
        if isinstance(self.body, dict) or isinstance(self.body, MultiDict):
            merge(self.params, self.body) 
        
        if not self.route('POST'):
            self.render(
                plain = 'NOT FOUND',
                status = 404
            )

    def do_GET(self):
        self.preprocess()

        merge(self.params, self.parse_query_params())

        if not self.route('GET'):
            path = os.path.join(self.public_dir, self.path[1:] if self.path != '/' else 'index.html')
            if not os.path.exists(path):
                path = os.path.join(self.public_dir, 'index.html')

            self.render(
                file = path,
                status = 200
            )

    def do_PUT(self):
        self.preprocess()

        self.body = self.parse_body()
        if isinstance(self.body, dict) or isinstance(self.body, MultiDict):
            merge(self.params, self.body) 

        if not self.route('PUT'):
            self.render(
                plain = 'NOT FOUND',
                status = 404
            )

    def do_DELETE(self):
        self.preprocess()

        if not self.route('DELETE'):
            self.render(
                plain = 'NOT FOUND',
                status = 404
            )

    ### Helpers

    # Override
    def enable_cors(self, _headers = {}):
        header = 'Access-Control-Allow-Origin'
        self.send_header(header, _headers.get(header) or '*')

        if self.command == 'OPTIONS':
            header = 'Access-Control-Allow-Methods'
            self.send_header(header, _headers.get(header) or 'GET, OPTIONS, POST, PATCH, PUT, DELETE')

            header = 'Access-Control-Allow-Headers'
            allowed_headers = _headers.get(header) or ', '.join([
                'Content-Type',
                headers.ACCESS_TOKEN.title(),
                headers.CLIENT.title(),
                headers.DO_PROXY.title(),
                headers.EXPIRY.title(),
                headers.PROXY_HEADERS.title(),
                headers.REQUEST_PATH.title(),
                headers.SERVICE_URL.title(),
                headers.TOKEN_TYPE.title(),
                headers.UID.title(),
            ])
            self.send_header(header, allowed_headers)

            header = 'Access-Control-Max-Age'
            self.send_header(header, _headers.get(header) or '7200')

    def preprocess(self):
        self.uri = urlparse(self.path)

        self.fullpath = self.path
        self.path = self.uri.path
        self.params = {}
        self.body = ''

    def route(self, method):
        for endpoint_handler in ROUTES[method]:
            path = endpoint_handler[0]

            matches = isinstance(path, str) and self.path == path
            matches = matches or not isinstance(path, str) and re.match(path, self.path)

            if matches:
                handler = endpoint_handler[1]
                handler(self)
                return True

        return False

    def parse_path_params(self, path_params_map):
        path = self.uri.path
        path_segments = path.split('/')

        if len(path_segments) == 0:
            return

        if path_segments[0] == '':
            path_segments.pop(0)

        for path_param in path_params_map:
            index = path_params_map[path_param]

            try:
                self.params[path_param] = path_segments[index]
            except:
                pass

    def parse_query_params(self):
        query_params = parse_qs(self.uri.query)

        for key, value in query_params.items():
            if len(value) == 1:
                query_params[key] = value[0]

        return query_params

    def parse_body(self):
        if not self.headers.get('Content-Length'):
            body = self.rfile.read()
        else:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

        if not self.headers['Content-Type']:
            return body

        return decode_response(body, self.headers['Content-Type'])