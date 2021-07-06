# Rails request object
# https://guides.rubyonrails.org/action_controller_overview.html#the-request-object
class Request:
    def __init__(self):
        self._method = ''
        self._url = ''
        self._path = ''
        self._base_url = ''
        self._headers = {}
        self._body = ''
        self._query = {}
        self._content_type = ''

    @property
    def method(self):
        return self._method

    @property
    def url(self):
        return self._url

    @property
    def base_url(self):
        return self._base_url

    @property
    def path(self):
        return self._path

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body

    @property
    def query(self):
        return self._query

    @property
    def content_type(self):
        return self._content_type

