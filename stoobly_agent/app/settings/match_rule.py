from .types.proxy_settings import MatchRule as IMatchRule

class MatchRule:

  def __init__(self, match_rule: IMatchRule):
    self.__match_rule = match_rule

    self.__components = self.__match_rule.get('components') or []
    self.__methods = self.__match_rule.get('methods') or []
    self.__modes = self.__match_rule.get('modes') or []
    self.__pattern = self.__match_rule.get('pattern')

  @property 
  def components(self):
    return self.__components

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
      'components': self.__components,
      'methods': self.__methods,
      'modes': self.__modes,
      'pattern': self.__pattern,
    }