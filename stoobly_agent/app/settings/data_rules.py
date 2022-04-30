from stoobly_agent.config.constants import mock_policy, record_policy, replay_policy, test_strategy

from .types.proxy_settings import DataRules as IDataRules

class DataRules:

  def __init__(self, data_rules: IDataRules):
    self.__data_rules = data_rules or {}

    self.__mock_policy = self.__data_rules.get('mock_policy') or mock_policy.FOUND
    self.__record_policy = self.__data_rules.get('record_policy') or record_policy.ALL
    self.__replay_policy = self.__data_rules.get('replay_policy') or replay_policy.ALL
    self.__scenario_key = self.__data_rules.get('scenario_key')
    self.__test_policy = self.__data_rules.get('test_policy') or mock_policy.FOUND
    self.__test_strategy = self.__data_rules.get('test_strategy') or test_strategy.DIFF

  @property
  def mock_policy(self):
    return self.__mock_policy 

  @property
  def record_policy(self):
    return self.__record_policy 

  @property
  def replay_policy(self):
    return self.__replay_policy

  @property
  def scenario_key(self):
    return self.__scenario_key

  @scenario_key.setter
  def scenario_key(self, v):
    self.__scenario_key = v
    self.__data_rules['scenario_key'] = v
    if not v and 'scenario_key' in self.__data_rules:
      del self.__data_rules['scenario_key']

  @property
  def test_policy(self):
    return self.__test_policy 

  @property
  def test_strategy(self):
    return self.__test_strategy 

  def to_dict(self) -> IDataRules:
    return {
      'mock_policy': self.__mock_policy,
      'record_policy': self.__record_policy,
      'replay_policy': self.__replay_policy,
      'scenario_key': self.__scenario_key,
      'test_policy': self.__test_policy,
      'test_strategy': self.__test_strategy,
    }