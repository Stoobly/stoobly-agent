from typing import List

from .types.proxy_settings import FirewallRule as IFirewallRule

class FirewallRule:

  def __init__(self, firewall_rule: IFirewallRule):
    self.__firewall_rule = firewall_rule

    self.__action = self.__firewall_rule.get('action')
    self.__modes = self.__firewall_rule.get('modes')
    self.__pattern = self.__firewall_rule.get('pattern')


  @property 
  def action(self):
    return self.__action

  @property
  def modes(self):
    return self.__modes

  @property
  def pattern(self):
    return self.__pattern

  def to_dict(self):
    return {
      'action': self.__action,
      'modes': self.__modes,
      'pattern': self.__pattern,
    }