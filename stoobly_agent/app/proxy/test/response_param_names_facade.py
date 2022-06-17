from typing import List

from stoobly_agent.lib.api.interfaces.endpoints import ResponseParamName

class ResponseParamNamesFacade():

  def __init__(self, response_param_names_response):
    self.__response_param_names = response_param_names_response

    self.__aliased_response_param_names = None
    self.__deterministic_response_param_names = None
    self.__required_response_param_names = None

  @property
  def aliased(self) -> List[ResponseParamName]: 
    if not self.__aliased_response_param_names:
      filter_handler = lambda param_name: param_name.get('alias_id') != None
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