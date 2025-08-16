import os
import pdb
import threading

from http.server import HTTPServer
from urllib.parse import urlparse

from stoobly_agent.config.constants import env_vars
from stoobly_agent.lib.logger import Logger

from .application_http_request_handler import ApplicationHTTPRequestHandler

LOG_ID = 'UI'

def start_server(host, port):
    httpd = HTTPServer((host, port), ApplicationHTTPRequestHandler)
    httpd.serve_forever()

def run(url):
    Logger.instance(LOG_ID).info(f"Server listening at {url}\n")

    parsed_url = urlparse(url)
    thread = threading.Thread(target=start_server, args=(parsed_url.hostname, parsed_url.port))
    thread.start()
    return url