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
  return jmespath.search(query, o, options)

def compile(expression: str):
  return jmespath.compile(expression)