from ctypes import Union
import pdb
from typing import List

from stoobly_agent.lib.api.interfaces.endpoints import ResponseParamName
from stoobly_agent.config.constants import test_filter

class ResponseParamNamesFacade():

  def __init__(self, response_param_names_response):
    self.__response_param_names = response_param_names_response

    self.__aliased_response_param_names = None
    self.__deterministic_response_param_names = None
    self.__required_response_param_names = None

    self.__filter: test_filter.TestFilter = test_filter.ALL

    self.__response_param_name_map = {}
    for response_param_name in self.__response_param_names:
      if not response_param_name.get('query'):
        continue

      self.__response_param_name_map[response_param_name['query']] = response_param_name

  @property
  def aliased(self) -> List[ResponseParamName]: 
    if not self.__aliased_response_param_names:
      filter_handler = lambda param_name: param_name.get('alias') != None
      self.__aliased_response_param_names = list(filter(filter_handler, self.__response_param_names))

    return self.__aliased_response_param_names

  @property
  def deterministic(self) -> List[ResponseParamName]:
    if not self.__deterministic_response_param_names:
      filter_handler = lambda param_name: (not not param_name.get('is_deterministic') )
      self.__deterministic_response_param_names = list(filter(filter_handler, self.__response_param_names))

    return self.__deterministic_response_param_names

  @property
  def required(self) -> List[ResponseParamName]: 
    if not self.__required_response_param_names:
      filter_handler = lambda param_name: (not not param_name.get('is_required'))
      self.__required_response_param_names = list(filter(filter_handler, self.__response_param_names))

    return self.__required_response_param_names

  def is_selected(self, query: str) -> bool:
    if self.__filter == test_filter.ALL:
      return True
    elif self.__filter == test_filter.ALIAS:
      _response_param_name = self.__response_param_name_map.get(query)
      if not _response_param_name:
        return True

      # If aliased, then filter
      return not not _response_param_name.get('alias')
    elif self.__filter == test_filter.CUSTOM:
      pass
    else:
      return False

  def with_filter(self, filter: test_filter.TestFilter):
    self.__filter = filter
    return self
    