from typing import List

from .filter_rule import FilterRule

from .types.proxy_settings import FilterSettings as IFilterSettings

class FilterSettings:
  __filter_settings = None

  def __init__(self, filter_settings: IFilterSettings):
    self.__filter_settings = filter_settings or {}

    self.__filter_rules_map = {
      k: list(map(lambda rule: FilterRule(rule), v)) for k, v in self.__filter_settings.items()
    }

  def filter_rules(self, project_id: str) -> List[FilterRule]:
    return self.__filter_rules_map.get(project_id) or []

  def set_filter_rules(self, project_id: str, v: List[FilterRule]):
    self.__filter_rules_map[project_id] = v

  def to_dict(self):
    return {k: list(map(lambda rule: rule.to_dict(), v)) for k, v in self.__filter_rules_map.items()}