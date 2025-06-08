from stoobly_agent.config.constants import mock_policy, record_order, record_policy, replay_policy, test_strategy

from .types.proxy_settings import DataRules as IDataRules

class DataRules:

  def __init__(self, data_rules: IDataRules):
    self.__data_rules = data_rules or {}

    self.__mock_policy = self.__data_rules.get('mock_policy') or mock_policy.FOUND
    self.__record_order = self.__data_rules.get('record_order') or record_order.APPEND
    self.__record_policy = self.__data_rules.get('record_policy') or record_policy.ALL
    self.__replay_policy = self.__data_rules.get('replay_policy') or replay_policy.ALL
    self.__scenario_key = self.__data_rules.get('scenario_key')
    self.__test_policy = self.__data_rules.get('test_policy') or mock_policy.FOUND
    self.__test_strategy = self.__data_rules.get('test_strategy') or test_strategy.DIFF

  @property
  def mock_policy(self):
    return self.__mock_policy 

  @mock_policy.setter
  def mock_policy(self, v):
    self.__mock_policy = v
    self.__data_rules['mock_policy'] = v

  @property
  def record_policy(self):
    return self.__record_policy 

  @record_policy.setter
  def record_policy(self, v):
    self.__record_policy = v
    self.__data_rules['record_policy'] = v

  @property
  def record_order(self):
    return self.__record_order

  @record_order.setter
  def record_order(self, v):
    valid_orders = [record_order.APPEND, record_order.OVERWRITE]
    if v not in valid_orders:
      raise TypeError(f"record_order has to be one of {valid_orders}, got {v}")

    self.__record_order = v
    self.__data_rules['record_order'] = v

  @property
  def replay_policy(self):
    return self.__replay_policy

  @replay_policy.setter
  def replay_policy(self, v):
    self.__record_policy = v
    self.__data_rules['replay_policy'] = v

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

  @test_policy.setter
  def test_policy(self, v):
    self.__test_policy = v
    self.__data_rules['test_policy'] = v

  @property
  def test_strategy(self):
    return self.__test_strategy 

  def to_dict(self) -> IDataRules:
    return {
      'mock_policy': self.__mock_policy,
      'record_order': self.__record_order,
      'record_policy': self.__record_policy,
      'replay_policy': self.__replay_policy,
      'scenario_key': self.__scenario_key,
      'test_policy': self.__test_policy,
      'test_strategy': self.__test_strategy,
    }