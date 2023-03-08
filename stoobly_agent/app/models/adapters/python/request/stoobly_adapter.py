import pdb
import requests

from urllib.parse import parse_qs, urlparse

class StooblyRequestAdapter():

  def __init__(self, request: requests.Request):
    self.__request = request

  def adapt(self):
    parsed_url = urlparse(self.__request.url)

    return {
      'body': self.__request.data,
      'headers': self.adapt_headers(),
      'method': self.__request.method,
      'path': parsed_url.path,
      'query_params': self.adapt_query_params(parsed_url.query),
      'url': self.__request.url,
    }

  def adapt_query_params(self, query = None):
    if not query:
      parsed_url = urlparse(self.__request.url)
      query = parsed_url.query

    _query_params = parse_qs(query)

    query_params = []
    for k, v in _query_params.items():
      for param in v:
        query_params.append({
          'name': k,
          'value': param,
        })

    return query_params

  def adapt_headers(self):
    headers = []

    for k, v in self.__request.headers.items():
      headers.append({
        'name': k,
        'value': v
      })

    return headers