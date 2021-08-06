import json
import mimetypes
import os
import pathlib
import pdb
import re
import yaml

from http.server import HTTPServer, BaseHTTPRequestHandler
from mergedeep import merge
from urllib.parse import urlparse, parse_qs

from .app.configs_controller import ConfigsController
from .app.proxy_controller import ProxyController
from .app.statuses_controller import StatusesController

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

    CONFIGS_PATH = '/api/v1/admin/configs'
    PROXY_PATH = '/proxy'
    STATUSES_PATH = '/api/v1/admin/statuses'
    STATUS_PATH = re.compile(f"{STATUSES_PATH}/.*[^/]$")

    @property
    def public_dir(self):
        return os.path.join(self.ROOT_DIR, 'public')

    ### Method handlers

    def do_OPTIONS(self):
        self.render(
            plain = 'OK',
            status = 200
        )

    def do_GET(self):
        self.preprocess()

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

        if not self.route('PUT'):
            self.render(
                plain = 'NOT FOUND',
                status = 404
            )

    ### Helpers

    def enable_cors(self):
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PATCH, PUT, DELETE')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'CONTENT-TYPE, X-DO-PROXY, X-SERVICE-URL, X-REQUEST-PATH')
        self.send_header('Access-Control-Max-Age', '7200')

    def preprocess(self):
        self.uri = urlparse(self.path)

        self.fullpath = self.path
        self.path = self.uri.path
        self.params = {}
        self.parse_query_params()

    def route(self, method):
        for endpoint_handler in self.ROUTES[method]:
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
        merge(self.params, parse_qs(self.uri.query))

    def parse_body(self):
        if not self.headers.get('Content-Length'):
            body = self.rfile.read()
        else:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

        if not self.headers['Content-Type']:
            return body

        if self.headers['Content-Type'].lower() == 'application/json':
            return json.loads(body)
        else:
            return body

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
        path = kwargs['file']

        if not os.path.exists(path):
            return self.send_response(404)
        else:
            self.send_response(kwargs.get('status') or 200)

        self.enable_cors()
        mimetype = mimetypes.guess_type(path)[0]
        self.send_header('Content-Type', mimetype or 'text/plain')
        self.render_headers(kwargs.get('headers'))
        self.end_headers()

        fp = open(path, 'rb')
        self.wfile.write(fp.read())
        fp.close()

    def render_json(self, kwargs):
        self.send_response(kwargs.get('status') or 200)

        self.enable_cors()
        self.send_header('Content-Type', 'application/json')
        self.render_headers(kwargs.get('headers'))
        self.end_headers()

        json_string = json.dumps(kwargs['json'])
        self.wfile.write(json_string.encode())

    def render_plain(self, kwargs):
        self.send_response(kwargs.get('status') or 200)

        self.enable_cors()
        self.send_header('Content-Type', 'text/plain')
        self.render_headers(kwargs.get('headers'))
        self.end_headers()

        if isinstance(kwargs['plain'], str):
            self.wfile.write(kwargs['plain'].encode())
        else:
            self.wfile.write(kwargs['plain'])

    def render_data(self, kwargs):
        self.send_response(kwargs.get('status') or 200)

        #self.enable_cors()
        self.render_headers(kwargs.get('headers'))
        self.end_headers()

        if isinstance(kwargs['data'], str):
            self.wfile.write(kwargs['data'].encode())
        else:
            self.wfile.write(kwargs['data'])

    def render_headers(self, headers):
        if headers:
            for key, val in headers.items():
                self.send_header(key, val)

    ### Routes

    ROUTES = {
        'GET': [
            [CONFIGS_PATH, ConfigsController.instance().get_configs],
            ['/'.join([CONFIGS_PATH, 'modes']), ConfigsController.instance().get_configs_modes],
            ['/'.join([CONFIGS_PATH, 'policies']), ConfigsController.instance().get_configs_policies],
            ['/'.join([PROXY_PATH, 'get']), ProxyController.instance().do_GET],
            [STATUS_PATH, StatusesController.instance().get_status],
        ],
        'PUT': [
            [CONFIGS_PATH, ConfigsController.instance().put_configs],
            ['/'.join([PROXY_PATH, 'put']), ProxyController.instance().do_PUT],
            [STATUS_PATH, StatusesController.instance().put_status],
        ]
    }

def run(host, port):
    httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
    httpd.serve_forever()
