import requests
import urllib
import pdb

from ..logger import Logger
from .stoobly_api import StooblyApi

LOG_ID = 'UsersResource'

class UsersResource(StooblyApi):
  USERS_ENDPOINT = 'users'

  def profile(self, query_params = {}) -> requests.Response:
    url = f"{self.service_url}/{self.USERS_ENDPOINT}/profile"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)