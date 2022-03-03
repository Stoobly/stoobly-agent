import os
import pdb
import requests

from stoobly_agent.proxy import get_proxy_url
from stoobly_agent.lib.constants.env_vars import HTTP_PROXY, HTTPS_PROXY

class Api():

    def without_proxy(self, handler):
      disabled = {}

      disabled[HTTP_PROXY] = os.environ[HTTP_PROXY]
      os.environ[HTTP_PROXY] = ''

      disabled[HTTPS_PROXY] = os.environ[HTTPS_PROXY]
      os.environ[HTTPS_PROXY] = ''

      disabled[HTTP_PROXY.lower()] = os.environ[HTTP_PROXY.lower()]
      os.environ[HTTP_PROXY.lower()] = ''

      disabled[HTTPS_PROXY.lower()] = os.environ[HTTPS_PROXY.lower()]
      os.environ[HTTPS_PROXY.lower()] = ''

      res = handler()

      for key, val in disabled.items():
        os.environ[key] = val

      return res

    def get(self, url, **kwargs):
      handler = lambda: requests.get(url, **kwargs)
      return self.without_proxy(handler)

    def post(self, url, **kwargs):
      handler = lambda: requests.post(url, **kwargs)
      return self.without_proxy(handler)
