from stoobly_agent.app.proxy.replay.alias_resolver import AliasResolver

class AliasContext():

  def __init__(self, alias_resolver: AliasResolver):
    self.__alias_resolver = alias_resolver
    self.__resolved_aliases = []

  @property
  def alias_resolver(self):
    return self.__alias_resolver

  @property
  def resolved_aliases(self):
    return self.__resolved_aliases

  def resolve_alias(self, alias_name: str, value: str):
    trace_alias = self.alias_resolver.resolve_alias(alias_name, value)
    self.resolved_aliases.append(trace_alias)
    return trace_alias