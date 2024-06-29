import pdb

from typing import Union

from stoobly_agent.lib.api.interfaces.endpoints import RequestComponentName
from stoobly_agent.lib.utils.python_to_ruby_type import convert

class SchemaBuilder:
  ###
  #
  # @param endpoint_id [Integer]
  # @param param_column_name [String] e.g. query_param_name, body_param_name, response_param_name
  #
  def __init__(self, endpoint_id, param_column_name: str):
    self.endpoint_id = endpoint_id
    self.param_column_name: str = param_column_name

  def build(self, params):
    params_list = []
    for literal_param in params:
      param: RequestComponentName = {
        'endpoint_id': self.endpoint_id,
        'name': literal_param['name'],
        'query': literal_param['query'],
        'is_required': literal_param['required'],
        'inferred_type': convert(self.__infer_type(literal_param['value'])),
        'is_deterministic': True,
        'id': literal_param['id'],
        f"{self.param_column_name}_id": literal_param['parent_id']
      }
      params_list.append(param)
    return params_list

  def __infer_type(self, val) -> str:
    return str(val.__class__)
