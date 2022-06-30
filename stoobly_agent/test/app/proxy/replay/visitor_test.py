import jmespath

from stoobly_agent.app.proxy.replay.visitor import TreeInterpreter, Visitor

# Monkey patch jmespath with replacement functionality
jmespath.parser.visitor.Vistor = Visitor
jmespath.parser.visitor.TreeInterpreter = TreeInterpreter

import json

class TestSearch():
    def test_a(self):
        a = {'foo': 1}
        jmespath.search('foo', a, { 'replacements': ['*'] })
        assert self.equals(a, {'foo': '*'}), print(a)

    def test_b(self):
        a = {'foo': { 'bar': 1 }}
        jmespath.search('foo.bar', a, { 'replacements': ['*'] })
        assert self.equals(a, {'foo': { 'bar': '*' }}), print(a)

    def test_c(self):
        a = [1]
        jmespath.search('[*]', a, { 'replacements': ['*'] })
        assert self.equals(a, ['*']), print(a)

    def test_d(self):
        a = [[1]]
        jmespath.search('[0][0]', a, { 'replacements': ['*'] })
        assert self.equals(a, ([['*']])), print(a)

    def test_e(self):
        a = [{'a': 1}]
        jmespath.search('[*].a', a, { 'replacements': ['*'] })
        assert self.equals(a, [{'a': '*'}]), print(a)

    def test_f(self):
        a = [{'a': [{'a': 1}]}]
        jmespath.search('[*].a[*].a', a, { 'replacements': ['*'] })
        assert self.equals(a, [{'a': [{'a': '*'}]}]), print(a)

    def test_g(self):
        a = [{'a': [{'a': {'a': [{'a': 1}]}}]}]
        jmespath.search('[*].a[*].a.a[*].a', a, { 'replacements': ['*'] })
        assert self.equals(a, [{'a': [{'a': {'a': [{'a': '*'}]}}]}]), print(a)

    def test_h(self):
        a = [{'a': [{'a': {'a': [{'a': 1}, {'a': 2}]}}]}]
        jmespath.search('[*].a[*].a.a[*].a', a, { 'replacements': ['*'] })
        assert self.equals(a, [{'a': [{'a': {'a': [{'a': '*'}, {'a': '*'}]}}]}]), print(a)

    def test_i(self):
        a = [{'a': 1}, {'a': 2}, {'a': 3}]
        jmespath.search('[*].a', a, { 'replacements': ['*'] })
        assert self.equals(a, [{'a': '*'}, {'a': '*'}, {'a': '*'}]), print(a)

    def test_i(self):
        a = [{'a': 1}, {'a': 'a'}, {'a': None}]
        jmespath.search('[*].a', a, { 'replacements': ['*'] })
        assert self.equals(a, [{'a': '*'}, {'a': '*'}, {'a': '*'}]), print(a)

    def equals(self, a, b):
        return json.dumps(a) == json.dumps(b)
