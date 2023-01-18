import hashlib
import pdb

from mitmproxy.coretypes.multidict import MultiDict
from typing import List, Dict, TypedDict, Union

from stoobly_agent.lib.logger import Logger, bcolors
from stoobly_agent.lib.utils.python_to_ruby_type import type_map

class IgnoredParam(TypedDict):
  inferred_type: str
  query: str

class RequestHasher():

  _instance = None

  def __init__(self):
    if self._instance:
        raise RuntimeError('Call instance() instead')
    else:
        self.type_map = type_map

  @classmethod
  def instance(cls):
      if cls._instance is None:
        cls._instance = cls()

      return cls._instance
  
  def hash_params(self, params: Union[dict, list], ignored_params: Dict[str, IgnoredParam] = {}) -> str:
    if isinstance(params, dict) or isinstance(params, list) or isinstance(params, MultiDict):
      return self.__serialize(None, params, None, ignored_params)
    else:
      return ''

  def hash_text(self, text: str) -> str:
    if len(text) == 0:
      return 
    return hashlib.md5(text.encode()).hexdigest()
 
  def __serialize(
    self, key: str, value: Union[dict, list, MultiDict, str], query: str, ignored_params: Dict[str, IgnoredParam] = {}
  ) -> str:
    if isinstance(value, dict) or isinstance(value, MultiDict):
      return self.__serialize_hash(key, value, query, ignored_params)
    elif isinstance(value, list):
      return self.__serialize_array(key, value, query, ignored_params)
    else:
      if self.__ignored(query, ignored_params, value):
        return

      return self.hash_text(self.__serialize_param(query, key, value))

  def __ignored(self, query: str, ignored_params: dict, value: Union[dict, list, str]) -> str:
    param = ignored_params.get(query)

    if not param:
      return False

    # Sometimes there's different types for a param
    if not isinstance(param, list):
      return param['query'] == query 

    for param_type in param:
      if self.__infer_type(value) == param_type['inferred_type'] and param_type['query'] == query:
        return True

  def __serialize_array(
    self, key: str, value: Union[dict, list, str], query: str, ignored_params: Dict[str, IgnoredParam] = {}
  ) -> str:
    serialized_params = []

    for v in value:
      param_hash = self.__serialize(key, v, '[*]' if not query else f"{query}[*]", ignored_params)

      if not param_hash:
        continue

      serialized_params.append(param_hash)

    return self.__hash_serialized_params(serialized_params)

  def __serialize_hash(
    self, key: str, value: Union[dict, list, str], query: str, ignored_params: Dict[str, IgnoredParam] = {}
  ) -> str:
    serialized_params = []

    for k, v in value.items():
      param_hash = self.__serialize(k, v, k if not query else f"{query}.{k}", ignored_params)

      if not param_hash:
        continue

      serialized_params.append(param_hash)

    return self.__hash_serialized_params(serialized_params)

  def __hash_serialized_params(self, serialized_params: List[str]):
    if not serialized_params or len(serialized_params) == 0:
      return '' 
    serialized_params.sort()
    return self.hash_text('.'.join(serialized_params))

  def __infer_type(self, val):
    return self.type_map.get(str(val.__class__))

  def __serialize_param(self, query, key: str, val):
    Logger.instance().debug(f"{bcolors.OKBLUE}Serializing{bcolors.ENDC} {query} => {val}")

    if isinstance(val, bool):
      # Ruby boolean are lower case
      val = str(val).lower()
    elif val == None:
      # Ruby str(nil) translates to ''
      val = ''

    return f"{str(key)}.{str(val)}"
