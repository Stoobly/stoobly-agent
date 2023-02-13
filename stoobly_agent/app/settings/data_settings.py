import os
import pdb

from stoobly_agent.config.constants import env_vars

from .data_rules import DataRules
from .types.proxy_settings import DataSettings as IDataSettings

class DataSettings:
  __data_settings = None

  def __init__(self, data_settings: IDataSettings):
    self.__data_settings = data_settings or {}
    self.__data_rules_map = {k: DataRules(v) for k, v in self.__data_settings.items()}

  def data_rules(self, project_id: str) -> DataRules:
    if not self.__data_rules_map.get(project_id):
      self.__data_rules_map[project_id] = DataRules({})
    return self.__data_rules_map[project_id]

  def to_dict(self):
    return {k: v.to_dict() for k, v in self.__data_rules_map.items()}