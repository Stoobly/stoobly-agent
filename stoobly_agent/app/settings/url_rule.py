from typing import List

from .types.proxy_settings import UrlRule as IUrlRule

class UrlRule:

  def __init__(self, url_rule: IUrlRule):
    self.update(url_rule)

  @property
  def host(self):
    return self.__host

  @property 
  def modes(self):
    return self.__modes

  @property
  def port(self):
    return self.__port

  def update(self, url_rule: IUrlRule):
    self.__url_rule = url_rule
    self.__host = self.__url_rule.get('host')
    self.__modes = self.__url_rule.get('modes')
    self.__port = self.__url_rule.get('port')

  def to_dict(self):
    return {
      'host': self.__host,
      'modes': self.__modes,
      'port': self.__port,
    }