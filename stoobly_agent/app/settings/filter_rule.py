from typing import List

from .types.proxy_settings import FilterRule as IFilterRule

class FilterRule:

  def __init__(self, filter_rule: IFilterRule):
    self.__filter_rule = filter_rule

    self.__action = self.__filter_rule.get('action')
    self.__methods = self.__filter_rule.get('methods') or []
    self.__modes = self.__filter_rule.get('modes') or []
    self.__pattern = self.__filter_rule.get('pattern')


  @property 
  def action(self):
    return self.__action

  @property 
  def methods(self):
    return self.__methods

  @property
  def modes(self):
    return self.__modes

  @property
  def pattern(self):
    return self.__pattern

  def to_dict(self):
    return {
      'action': self.__action,
      'methods': self.__methods,
      'modes': self.__modes,
      'pattern': self.__pattern,
    }