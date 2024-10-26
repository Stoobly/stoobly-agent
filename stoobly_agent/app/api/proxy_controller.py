import requests

from http.cookies import SimpleCookie
from urllib3.exceptions import InsecureRequestWarning

from stoobly_agent.config.constants import headers
from stoobly_agent.config.mitmproxy import MitmproxyConfig
from stoobly_agent.lib.logger import Logger

LOG_ID = 'ProxyController'

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
            _verify = not MitmproxyConfig.instance().get('ssl_insecure')

            Logger.instance(LOG_ID).debug('Request Headers')
            Logger.instance(LOG_ID).debug(_headers)
            Logger.instance(LOG_ID).debug('Cookies')
            Logger.instance(LOG_ID).debug(_cookies)
            Logger.instance(LOG_ID).debug('Body')
            Logger.instance(LOG_ID).debug(_body)
            Logger.instance(LOG_ID).debug('Query Params')
            Logger.instance(LOG_ID).debug(_params)

            body = None
            headers = {}
            status = 0

            if not _verify:
                # Suppress only the single warning from urllib3 needed.
                requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

            try:
                res = method(
                    url,
                    allow_redirects = True,
                    cookies = _cookies,
                    data = _body,
                    headers = _headers,
                    params = _params,
                    stream = True,
                    verify = _verify
                )
                
                body = res.raw.data
                headers = res.headers
                status = res.status_code
            except requests.exceptions.ConnectTimeout:
                body = b'Gateway Timeout'
                status = 504
            except requests.exceptions.SSLError as e:
                body = str(e).encode()
                status = 502
            except requests.exceptions.ConnectionError:
                body = b'Bad Gateway'
                status = 502
            except Exception:
                body = b'Unknown Error'
                status = 0

            Logger.instance(LOG_ID).debug('Response Headers')
            Logger.instance(LOG_ID).debug(res.headers)

            context.render(
                headers = headers,
                data = body,
                status = status,
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


