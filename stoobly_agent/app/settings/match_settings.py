import pdb

from typing import List

from .match_rule import MatchRule

from .types.proxy_settings import MatchSettings as IMatchSettings

class MatchSettings:
  __match_settings = None

  def __init__(self, match_settings: IMatchSettings):
    self.__match_settings = match_settings or {}

    self.__match_rules_map = {
      k: list(map(lambda rule: MatchRule(rule), v)) for k, v in self.__match_settings.items()
    }

  def match_rules(self, project_id: str) -> List[MatchRule]:
    return self.__match_rules_map.get(project_id) or []

  def set_match_rules(self, project_id: str, v: List[MatchRule]):
    self.__match_rules_map[project_id] = v

  def to_dict(self):
    return {k: list(map(lambda rule: rule.to_dict(), v)) for k, v in self.__match_rules_map.items()}