from typing import List

from .types.proxy_settings import FirewallRule as IFirewallRule

class FirewallRule:

  def __init__(self, firewall_rule: IFirewallRule):
    self.__firewall_rule = firewall_rule

    self.__action = self.__firewall_rule.get('action')
    self.__methods = self.__firewall_rule.get('methods') or []
    self.__modes = self.__firewall_rule.get('modes') or []
    self.__pattern = self.__firewall_rule.get('pattern')


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