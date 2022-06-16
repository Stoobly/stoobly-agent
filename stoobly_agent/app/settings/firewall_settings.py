import pdb

from typing import List

from .firewall_rule import FirewallRule

from .types.proxy_settings import FirewallSettings as IFirewallSettings

class FirewallSettings:
  __firewall_settings = None

  def __init__(self, firewall_settings: IFirewallSettings):
    self.__firewall_settings = firewall_settings or {}

    self.__firewall_rules_map = {
      k: list(map(lambda rule: FirewallRule(rule), v)) for k, v in self.__firewall_settings.items()
    }

  def firewall_rules(self, project_id: str) -> List[FirewallRule]:
    return self.__firewall_rules_map.get(project_id) or []

  def to_dict(self):
    return {k: list(map(lambda rule: rule.to_dict(), v)) for k, v in self.__firewall_rules_map.items()}