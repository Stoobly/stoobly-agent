import requests

from http.cookies import SimpleCookie

from stoobly_agent.config.constants import headers
from stoobly_agent.config.mitmproxy import MitmproxyConfig
from stoobly_agent.lib.logger import Logger

class ProxyController:
    _instance = None

    def __init__(self):
        if self._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.data = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def do_DELETE(self, context):
        self.__proxy(context, requests.delete)

    def do_GET(self, context):
        self.__proxy(context, requests.get)

    def do_HEAD(self, context):
        self.__proxy(context, requests.head)

    def do_OPTIONS(self, context):
        self.__proxy(context, requests.options)

    def do_PATCH(self, context):
        self.__proxy(context, requests.patch)

    def do_POST(self, context):
        self.__proxy(context, requests.post)

    def do_PUT(self, context):
        self.__proxy(context, requests.put)

    def __proxy(self, context, method):
        url = self.__get_url(context)

        if url:
            _headers = self.__get_headers(context)
            _cookies =  self.__get_cookies(context)
            _body = self.__get_body(context)
            _params = context.params

            Logger.instance().debug('Request Headers')
            Logger.instance().debug(_headers)
            Logger.instance().debug('Cookies')
            Logger.instance().debug(_cookies)
            Logger.instance().debug('Body')
            Logger.instance().debug(_body)
            Logger.instance().debug('Query Params')
            Logger.instance().debug(_params)

            res = method(
                url,
                allow_redirects = True,
                cookies = _cookies,
                data = _body,
                headers = _headers,
                params = _params,
                stream = True,
                verify = not MitmproxyConfig.instance().get('ssl_insecure')
            )

            Logger.instance().debug('Response Headers')
            Logger.instance().debug(res.headers)

            context.render(
                headers = res.headers,
                data = res.raw.data,
                status = res.status_code,
            )

    def __get_headers(self, context):
        request_headers = dict(context.headers)

        headers_white_list = []

        if headers.PROXY_HEADERS.title() in request_headers:
            headers_white_list = request_headers[headers.PROXY_HEADERS.title()].split(',')

        white_listed_headers = {}
        for name, value in request_headers.items():
            if name in headers_white_list:
                white_listed_headers[name] = value

        return white_listed_headers

    def __get_url(self, context):
        service_url = context.headers.get(headers.SERVICE_URL)

        if not service_url:
            context.render(
                plain = f"Invalid {headers.SERVICE_URL} header {service_url}",
                status = 400
            )
            return None

        request_path = context.headers.get(headers.REQUEST_PATH)

        if not request_path:
            context.render(
                plain = f"Invalid {headers.REQUEST_PATH} header {service_url}",
                status = 400
            )
            return None

        return f"{service_url}{request_path}"

    def __get_cookies(self, context):
        return SimpleCookie(context.headers.get('Cookie'))

    def __get_body(self, context):
        content_length = context.headers.get('Content-Length')
        if content_length:
            return context.rfile.read(content_length)


