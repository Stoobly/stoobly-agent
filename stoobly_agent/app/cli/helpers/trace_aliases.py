import pdb
from typing import List, TypedDict

from stoobly_agent.lib.orm.trace import Trace

class Alias(TypedDict):
  name: str
  value: str

def parse_aliases(aliases: List[str]) -> List[Alias]: 
  def parse_alias_string(_alias):
    toks = _alias.split('=', 1)

    try:
      value = eval(toks[1])
    except Exception as e:
      if len(toks) > 1:
        value = toks[1]
      else:
        value = None

    return {
      'name': toks[0],
      'value': value,
    }

  return list(map(parse_alias_string, aliases))

def adapt_trace_aliases(trace_id: int) -> List[Alias]:
  trace = Trace.find_by(id=trace_id)
  if not trace:
    return []

  trace_aliases = trace.trace_aliases

  def trace_alias_to_alias(trace_alias):
    return {
      'name': trace_alias.name,
      'value': trace_alias.value,
    }
    
  return list(map(trace_alias_to_alias, trace_aliases))