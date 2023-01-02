import jmespath

from typing import Callable, TypedDict, Union

from .visitor import TreeInterpreter, Visitor

# Monkey patch jmespath with replacement functionality
jmespath.parser.visitor.Vistor = Visitor
jmespath.parser.visitor.TreeInterpreter = TreeInterpreter

class Options(TypedDict):
  handle_after_replace: Callable
  handle_replace: Callable

def search(query: str, o: Union[dict, list], options: Options = {}):
  try:
    return jmespath.search(query, o, options)
  except jmespath.exceptions.LexerError as e:
    # On LexerError, try escaping the query
    return jmespath.search(f"\"{query}\"", o, options)

def compile(expression: str):
  return jmespath.compile(expression)

def flatten(value, query: str) -> list:
  array_count = query.count('[*]')

  if array_count == 0 or not isinstance(value, list):
    return [value]
  else:
    return __flatten(value, array_count)

def __flatten(ar, depth, cur_depth = 0):
  if cur_depth == depth:
    return ar

  next_ar = []
  for el in ar:
    if cur_depth == depth - 1:
      next_ar.append(el)
    else:
      if isinstance(el, list):
        next_ar.append(el)
  
  return __flatten(next_ar, depth, cur_depth + 1)