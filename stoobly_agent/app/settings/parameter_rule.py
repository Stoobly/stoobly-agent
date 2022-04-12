from typing import List

from .types.proxy_settings import ParameterRule as IParameterRule

class ParameterRule:

  def __init__(self, filter_rule: IParameterRule):
    self.__filter_rule = filter_rule

    self.__modes = self.__filter_rule.get('modes')
    self.__name = self.__filter_rule.get('name')
    self.__value = self.__filter_rule.get('value')
    self.__type = self.__filter_rule.get('type')

  @property 
  def modes(self):
    return self.__modes

  @property
  def name(self):
    return self.__name

  @property
  def value(self):
    return self.__value

  @property
  def type(self):
    return self.__type

  def to_dict(self):
    return {
      'modes': self.__modes,
      'name': self.__name,
      'value': self.__value,
      'type': self.__type,
    }