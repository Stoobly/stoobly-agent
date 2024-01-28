import copy
import pdb

from typing import Union

from stoobly_agent.app.proxy.test.matchers.context import MatchContext
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.config.constants.lifecycle_hooks import BEFORE_REQUEST_COMPONENT_CREATE, BEFORE_REQUEST_COMPONENT_DELETE

class SynchronizeEvent():

  def __init__(self, component_type: request_component.RequestComponent, previous_state: Union[dict, list], key, value):
    self.__component_type = component_type
    self.__key = key
    self.__previous_state = previous_state
    self.__value = value

  @property
  def key(self):
    return self.__key

  @property
  def previous_state(self):
    return self.__previous_state

  @property
  def value(self):
    return self.__value

  @property
  def is_body_param(self):
    return self.__component_type == request_component.BODY_PARAM

  @property
  def is_query_param(self):
    return self.__component_type == request_component.QUERY_PARAM

class SynchronizeCreateEvent(SynchronizeEvent):

  def __init__(self, component_type: request_component.RequestComponent, previous_state: Union[dict, list], key, value):
    super().__init__(component_type, previous_state, key, value)

class SynchronizeDeleteEvent(SynchronizeEvent):

  def __init__(self, component_type: request_component.RequestComponent, previous_state: Union[dict, list], key):
    super().__init__(component_type, previous_state, key, None)

class EventLog():

  def __init__(self):
    self.__events = []

  def append(self, event: SynchronizeEvent):
    self.__events.append(event)

class RequestSynchronizeHandler():

  def __init__(self, component_type: request_component.RequestComponent, lifecycle_hooks = {}):
    self.__component_type = component_type
    self.__event_log = EventLog()
    self.__lifecycle_hooks = lifecycle_hooks

  @property
  def event_log(self):
    return self.__event_log

  def handle_length_match_error(self, context: MatchContext, value: list):
    return True

  def handle_param_name_missing(self, context: MatchContext, value: dict):
    request_component_name = context.request_component_name

    # Component deleted already
    if not request_component_name:
      return True

    potential_values = request_component_name.get('values') or [None]

    if len(potential_values) > 0:
      key = context.current_key
      new_value = potential_values[0]

      event = SynchronizeCreateEvent(self.__component_type, copy.deepcopy(value), key, new_value)
      handle_before_param_create = self.__lifecycle_hooks.get(BEFORE_REQUEST_COMPONENT_CREATE)

      if not handle_before_param_create or not handle_before_param_create(event):
        value[key] = new_value
        self.event_log.append(event)

    return True

  def handle_param_name_exists(self, context: MatchContext, value: dict):
    key = context.current_key

    event = SynchronizeDeleteEvent(self.__component_type, copy.deepcopy(value), key)
    handle_before_param_delete = self.__lifecycle_hooks.get(BEFORE_REQUEST_COMPONENT_DELETE)

    if not handle_before_param_delete or not handle_before_param_delete(event):
      del value[key]
      self.event_log.append(event)

    return True

  def handle_type_match_error(self, context: MatchContext, value):
    if isinstance(value, list) or isinstance(value, dict):
      key = context.current_key
      del value[key]

    return True

  def handle_valid_type_error(self, context: MatchContext, value):
    if isinstance(value, list) or isinstance(value, dict):
      key = context.current_key
      del value[key]
      
    return True
