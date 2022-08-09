import pdb

from typing import List

from stoobly_agent.app.cli.helpers.trace_aliases import parse_aliases
from stoobly_agent.app.proxy.replay.trace_context import TraceContext
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import alias_resolve_strategy
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.orm.trace import Trace

class TraceContextFacade():

  def __init__(self, settings: Settings, trace: Trace = None):
    self.__settings = settings
    self.__endpoints_resource = EndpointsResource(self.__settings.remote.api_url, self.__settings.remote.api_key)
    self.__trace_context = TraceContext(self.__endpoints_resource, trace)

  @property
  def trace_context(self):
    return self.__trace_context

  def with_aliases(self, aliases):
    for _alias in self.__parse_aliases(aliases):
      self.__trace_context.create_trace_alias(_alias['name'], _alias['value'])
    return self

  def __parse_aliases(self, aliases: List[str]):
    if not aliases:
      return []

    return parse_aliases(aliases) 