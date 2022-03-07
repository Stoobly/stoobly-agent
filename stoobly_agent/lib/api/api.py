import os
import pdb
import requests

from stoobly_agent.proxy import get_proxy_url
from stoobly_agent.lib.constants.env_vars import HTTP_PROXY, HTTPS_PROXY

class Api():

    def without_proxy(self, handler):
      current = self.set_proxy('')

      res = handler()

      for key, val in current.items():
        os.environ[key] = val

      return res

    def with_proxy(self, handler):
      proxy_url = get_proxy_url()
      current = self.set_proxy(proxy_url)

      res = handler()

      for key, val in current.items():
        os.environ[key] = val

      return res

    def set_proxy(self, val):
      current = {}

      current[HTTP_PROXY] = os.environ[HTTP_PROXY]
      os.environ[HTTP_PROXY] = ''

      current[HTTPS_PROXY] = os.environ[HTTPS_PROXY]
      os.environ[HTTPS_PROXY] = ''

      current[HTTP_PROXY.lower()] = os.environ[HTTP_PROXY.lower()]
      os.environ[HTTP_PROXY.lower()] = ''

      current[HTTPS_PROXY.lower()] = os.environ[HTTPS_PROXY.lower()]
      os.environ[HTTPS_PROXY.lower()] = ''

      return current

    def get(self, url, **kwargs):
      handler = lambda: requests.get(url, **kwargs)
      return self.without_proxy(handler)

    def post(self, url, **kwargs):
      handler = lambda: requests.post(url, **kwargs)
      return self.without_proxy(handler)
