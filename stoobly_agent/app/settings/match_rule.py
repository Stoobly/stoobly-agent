from .types.proxy_settings import MatchRule as IMatchRule

class MatchRule:

  def __init__(self, firewall_rule: IMatchRule):
    self.__firewall_rule = firewall_rule

    self.__components = self.__firewall_rule.get('components')
    self.__modes = self.__firewall_rule.get('modes')
    self.__pattern = self.__firewall_rule.get('pattern')


  @property 
  def components(self):
    return self.__components

  @property
  def modes(self):
    return self.__modes

  @property
  def pattern(self):
    return self.__pattern

  def to_dict(self):
    return {
      'components': self.__components,
      'modes': self.__modes,
      'pattern': self.__pattern,
    }