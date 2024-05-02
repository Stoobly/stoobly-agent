from typing import List

from .types.proxy_settings import UrlRule as IUrlRule

class UrlRule:

  def __init__(self, url_rule: IUrlRule):
    self.update(url_rule)

  @property
  def hostname(self):
    return self.__hostname

  @property 
  def modes(self):
    return self.__modes

  @property
  def path(self):
    return self.__path

  @property
  def port(self):
    return self.__port

  @property
  def scheme(self):
    return self.__scheme

  def update(self, url_rule: IUrlRule):
    self.__url_rule = url_rule
    self.__hostname = self.__url_rule.get('hostname')
    self.__modes = self.__url_rule.get('modes')
    self.__path = self.__url_rule.get('path')
    self.__port = self.__url_rule.get('port')
    self.__scheme = self.__url_rule.get('scheme')

  def to_dict(self):
    return {
      'hostname': self.__hostname,
      'modes': self.__modes,
      'path': self.__path,
      'port': self.__port,
      'scheme': self.__scheme,
    }