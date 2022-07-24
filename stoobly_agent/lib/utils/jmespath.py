import jmespath

from .visitor import TreeInterpreter, Visitor

# Monkey patch jmespath with replacement functionality
jmespath.parser.visitor.Vistor = Visitor
jmespath.parser.visitor.TreeInterpreter = TreeInterpreter

def search(query, o, options = {}):
  jmespath.search(query, o, options)