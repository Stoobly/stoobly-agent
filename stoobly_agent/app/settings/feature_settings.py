import os
import pdb

from stoobly_agent.config.constants import env_vars

from .types import FeatureSettings as IFeatureSettings

class FeatureSettings:

  def __init__(self, feature_settings: IFeatureSettings):
    self.__feature_settings = feature_settings or {}
    self.__dev_tools = self.__feature_settings.get('dev_tools')
    self.__exec = self.__feature_settings.get('exec')
    self.__remote = self.__feature_settings.get('remote')

  @property
  def dev_tools(self) -> bool:
    return self.__dev_tools or False

  @property
  def exec(self) -> bool:
    return self.__exec or False

  @property
  def remote(self) -> bool:
    if os.environ.get(env_vars.AGENT_REMOTE_ENABLED):
        return True 
    return self.__remote or False

  @dev_tools.setter
  def api_url(self, v):
    self.__dev_tools = v

  @exec.setter
  def exec(self, v):
    self.__exec = v

  @remote.setter
  def remote(self, v):
    self.__remote = v

  def to_dict(self) -> IFeatureSettings:
    return {
      'dev_tools': self.__dev_tools,
      'exec': self.__exec,
      'remote': self.__remote,
    }