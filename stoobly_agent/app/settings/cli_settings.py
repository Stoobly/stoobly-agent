import os

from .feature_settings import FeatureSettings
from .types.cli_settings import CLISettings as ICLISettings 

class CLISettings():

  def __init__(self, cli_settings: ICLISettings):
    self.__cli_settings = cli_settings

    self.__features = FeatureSettings(self.__cli_settings.get('features'))

  @property
  def features(self) -> FeatureSettings:
    return self.__features

  def to_dict(self) -> ICLISettings:
    return {
      'features': self.__features.to_dict()
    }