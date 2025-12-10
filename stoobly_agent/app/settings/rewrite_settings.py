import os

from typing import List

from stoobly_agent.config.constants import env_vars

from .rewrite_rule import RewriteRule
from .types.proxy_settings import RewriteSettings as IRewriteSettings

class RewriteSettings:
  __rewrite_settings = None

  def __init__(self, rewrite_settings: IRewriteSettings):
    self.__rewrite_settings = rewrite_settings or {}

    self.__rewrite_rules_map = {k: list(map(lambda rule: RewriteRule(rule), v)) for k, v in self.__rewrite_settings.items()}

  def rewrite_rules(self, project_id: str) -> List[RewriteRule]:
    return self.__rewrite_rules_map.get(project_id) or []

  def set_rewrite_rules(self, project_id: str, v: List[RewriteRule]):
    self.__rewrite_rules_map[project_id] = v

  def to_dict(self):
    return {k: list(map(lambda rule: rule.to_dict(), v)) for k, v in self.__rewrite_rules_map.items()}