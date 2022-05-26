import jmespath

from stoobly_agent.app.proxy.replay.visitor import TreeInterpreter, Visitor

# Monkey patch jmespath with replacement functionality
jmespath.parser.visitor.Vistor = Visitor
jmespath.parser.visitor.TreeInterpreter = TreeInterpreter

import json

def a():
    a = {'foo': 1}
    jmespath.search('foo', a, { 'replacements': ['*'] })
    print(a)
    print(equals(a, {'foo': '*'}))

def b():
    a = {'foo': { 'bar': 1 }}
    jmespath.search('foo.bar', a, { 'replacements': ['*'] })
    print(a)
    print(equals(a, {'foo': { 'bar': '*' }}))

def c():
    a = [1]
    jmespath.search('[*]', a, { 'replacements': ['*'] })
    print(a)
    print(equals(a, ['*']))

def d():
    a = [[1]]
    jmespath.search('[0][0]', a, { 'replacements': ['*'] })
    print(a)
    print(equals(a, ([['*']])))

def e():
    a = [{'a': 1}]
    jmespath.search('[*].a', a, { 'replacements': ['*'] })
    print(a)
    print(equals(a, [{'a': '*'}]))

def f():
    a = [{'a': [{'a': 1}]}]
    jmespath.search('[*].a[*].a', a, { 'replacements': ['*'] })
    print(a)
    print(equals(a, [{'a': [{'a': '*'}]}]))

def g():
    a = [{'a': [{'a': {'a': [{'a': 1}]}}]}]
    jmespath.search('[*].a[*].a.a[*].a', a, { 'replacements': ['*'] })
    print(a)
    print(equals(a, [{'a': [{'a': {'a': [{'a': '*'}]}}]}]))

def h():
    a = [{'a': [{'a': {'a': [{'a': 1}, {'a': 2}]}}]}]
    jmespath.search('[*].a[*].a.a[*].a', a, { 'replacements': ['*'] })
    print(a)
    print(equals(a, [{'a': [{'a': {'a': [{'a': '*'}, {'a': '*'}]}}]}]))

def i():
    a = [{'a': 1}, {'a': 2}, {'a': 3}]
    jmespath.search('[*].a', a, { 'replacements': ['*'] })
    print(a)
    print(equals(a, [{'a': '*'}, {'a': '*'}, {'a': '*'}]))


def equals(a, b):
    return json.dumps(a) == json.dumps(b)

a()
b()
c()
d()
e()
f()
g()
h()
i()