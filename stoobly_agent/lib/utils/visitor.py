import operator
import pdb

from typing import Callable

from jmespath import functions
from jmespath.compat import string_type
from numbers import Number
from stoobly_agent.lib.logger import Logger

LOG_ID = 'JmesPath'

def _equals(x, y):
    if _is_special_integer_case(x, y):
        return False
    else:
        return x == y


def _is_special_integer_case(x, y):
    # We need to special case comparing 0 or 1 to
    # True/False.  While normally comparing any
    # integer other than 0/1 to True/False will always
    # return False.  However 0/1 have this:
    # >>> 0 == True
    # False
    # >>> 0 == False
    # True
    # >>> 1 == True
    # True
    # >>> 1 == False
    # False
    #
    # Also need to consider that:
    # >>> 0 in [True, False]
    # True
    if type(x) is int and (x == 0 or x == 1):
        return y is True or y is False
    elif type(y) is int and (y == 0 or y == 1):
        return x is True or x is False


def _is_comparable(x):
    # The spec doesn't officially support string types yet,
    # but enough people are relying on this behavior that
    # it's been added back.  This should eventually become
    # part of the official spec.
    return _is_actual_number(x) or isinstance(x, string_type)


def _is_actual_number(x):
    # We need to handle python's quirkiness with booleans,
    # specifically:
    #
    # >>> isinstance(False, int)
    # True
    # >>> isinstance(True, int)
    # True
    if x is True or x is False:
        return False
    return isinstance(x, Number)


class Options(object):
    """Options to control how a JMESPath function is evaluated."""
    def __init__(self, dict_cls=None, custom_functions=None):
        #: The class to use when creating a dict.  The interpreter
        #  may create dictionaries during the evaluation of a JMESPath
        #  expression.  For example, a multi-select hash will
        #  create a dictionary.  By default we use a dict() type.
        #  You can set this value to change what dict type is used.
        #  The most common reason you would change this is if you
        #  want to set a collections.OrderedDict so that you can
        #  have predictable key ordering.
        self.dict_cls = dict_cls
        self.custom_functions = custom_functions


class _Expression(object):
    def __init__(self, expression, interpreter):
        self.expression = expression
        self.interpreter = interpreter

    def visit(self, node, *args, **kwargs):
        return self.interpreter.visit(node, *args, **kwargs)


class Visitor(object):
    def __init__(self):
        self._method_cache = {}

        # EDITED
        self.visited_nodes = []
        self.nodes = []

    def visit(self, node, *args, **kwargs):
        self.build_traverse_path(node) # On first visit, build expected traverse path

        self.increment_visits(node)

        node_type = node['type']
        method = self._method_cache.get(node_type)
        if method is None:
            method = getattr(
                self, 'visit_%s' % node['type'], self.default_visit)
            self._method_cache[node_type] = method

        return method(node, *args, **kwargs)

    def increment_visits(self, node):
        self.visited_nodes.append(node)
        Logger.instance(LOG_ID).debug(f"{len(self.visited_nodes)} {node}")

    def build_traverse_path(self, node):
        if len(self.nodes) > 0:
            return

        self.nodes.append(node)

        self.build_traverse_path_traverse(node)

        Logger.instance(LOG_ID).debug('Traverse Path')
        for i, node in enumerate(self.nodes):
            Logger.instance(LOG_ID).debug(f"{i + 1} {node}")

    def build_traverse_path_traverse(self, node):
        if node['type'] == 'projection':
            self.nodes.append(node)

        for node in node.get('children'):
            self.nodes.append(node)

            if len(node['children']) > 0:
                self.build_traverse_path_traverse(node)

    def default_visit(self, node, *args, **kwargs):
        raise NotImplementedError("default_visit")


class TreeInterpreter(Visitor):
    COMPARATOR_FUNC = {
        'eq': _equals,
        'ne': lambda x, y: not _equals(x, y),
        'lt': operator.lt,
        'gt': operator.gt,
        'lte': operator.le,
        'gte': operator.ge
    }
    _EQUALITY_OPS = ['eq', 'ne']
    MAP_TYPE = dict

    def __init__(self, options=None):
        super(TreeInterpreter, self).__init__()
        self._dict_cls = self.MAP_TYPE

        self.replacements = []
        self.replacement_number = 0
        self.handle_after_replace = None
        self.handle_replace = None

        if isinstance(options, dict):
            if 'replacements' in options:
                self.replacements: list = options.get('replacements') or []

            if 'handle_after_replace' in options:
                self.handle_after_replace: Callable = options['handle_after_replace']

            if 'handle_replace' in options:
                self.handle_replace: Callable = options['handle_replace']

            options = None

        if options is None:
            options = Options()

        self._options = options
        if options.dict_cls is not None:
            self._dict_cls = self._options.dict_cls
        if options.custom_functions is not None:
            self._functions = self._options.custom_functions
        else:
            self._functions = functions.Functions()

    # Greater than or equal is if there's multiple leaves
    def is_leaf(self):
        r =  len(self.visited_nodes) >= len(self.nodes)
        return r

    def is_path(self):
        if self.is_leaf():
            return False

        for i, visited_node in enumerate(self.visited_nodes):
            if visited_node != self.nodes[i]:
                return False

        return True

    def on_visit_leaf(self, obj, key):
        if not self.is_leaf():
            return

        if self.__do_replace():
            self.replace(obj, key)

    def __handle_replace(self, name, value):
        replacement_value = None

        if self.handle_replace:
            replacement_value = self.handle_replace(name, value, self.replacement_number)
        else: 
            replacement_value = self.replacements[self.replacement_number % len(self.replacements)]

        return replacement_value

    def __do_replace(self):
        return self.handle_replace or (self.replacements and isinstance(self.replacements, list) and len(self.replacements) > 0)
        
    def replace(self, obj, key):
        current_value = None

        try:
            current_value = obj[key]
        except KeyError:
            pass
        except IndexError:
            pass
        
        try:
            obj[key] = self.__handle_replace(key, current_value)
        except ValueError:
            return

        if self.handle_after_replace:
            self.handle_after_replace(key, current_value, self.replacement_number)

        self.replacement_number += 1

    def default_visit(self, node, *args, **kwargs):
        raise NotImplementedError(node['type'])

    def visit_subexpression(self, node, value):
        result = value
        flushed = False # Flushed denotes whether we are visiting a list

        _visited_nodes = self.visited_nodes.copy()

        for i, node in enumerate(node['children']):
            result = self.visit(node, result)

            # If current subexpression has deviated from the path, then flush
            if not self.is_path():
                self.visited_nodes = _visited_nodes.copy()
                flushed = True

        '''
        For each element in list, a new subexpression node gets created

        e.g. 
        For: [{'alias': { 'id': 1}}, {'alias': { 'id': 2}}]

        The parse results will look like:
        {'type': 'subexpression', 'children': [{'type': 'field', 'children': [], 'value': 'alias'}, {'type': 'field', 'children': [], 'value': 'id'}]}, 
        {'type': 'field', 'children': [], 'value': 'alias'}, 
        {'type': 'field', 'children': [], 'value': 'id'}, 
        {'type': 'subexpression', 'children': [{'type': 'field', 'children': [], 'value': 'alias'}, {'type': 'field', 'children': [], 'value': 'id'}]}, 
        {'type': 'field', 'children': [], 'value': 'alias'}
        {'type': 'field', 'children': [], 'value': 'id'}, 

        We don't want this, pop after each subexpression
        ''' 
        if flushed:
            self.visited_nodes.pop() 

        return result

    def visit_field(self, node, value):
        try:
            cur_value = value.get(node['value'])

            self.on_visit_leaf(value, node['value']) # ADDED

            return cur_value
        except AttributeError:
            return None

    def visit_comparator(self, node, value):
        # Common case: comparator is == or !=
        comparator_func = self.COMPARATOR_FUNC[node['value']]
        if node['value'] in self._EQUALITY_OPS:
            return comparator_func(
                self.visit(node['children'][0], value),
                self.visit(node['children'][1], value)
            )
        else:
            # Ordering operators are only valid for numbers.
            # Evaluating any other type with a comparison operator
            # will yield a None value.
            left = self.visit(node['children'][0], value)
            right = self.visit(node['children'][1], value)
            num_types = (int, float)
            if not (_is_comparable(left) and
                    _is_comparable(right)):
                return None
            return comparator_func(left, right)

    def visit_current(self, node, value):
        return value

    def visit_expref(self, node, value):
        return _Expression(node['children'][0], self)

    def visit_function_expression(self, node, value):
        resolved_args = []
        for child in node['children']:
            current = self.visit(child, value)
            resolved_args.append(current)
        return self._functions.call_function(node['value'], resolved_args)

    def visit_filter_projection(self, node, value):
        base = self.visit(node['children'][0], value)
        if not isinstance(base, list):
            return None
        comparator_node = node['children'][2]
        collected = []
        for element in base:
            if self._is_true(self.visit(comparator_node, element)):
                current = self.visit(node['children'][1], element)
                if current is not None:
                    collected.append(current)
        return collected

    def visit_flatten(self, node, value):
        base = self.visit(node['children'][0], value)
        if not isinstance(base, list):
            # Can't flatten the object if it's not a list.
            return None
        merged_list = []
        for element in base:
            if isinstance(element, list):
                merged_list.extend(element)
            else:
                merged_list.append(element)
        return merged_list

    def visit_identity(self, node, value):
        return value

    def visit_index(self, node, value):
        # Even though we can index strings, we don't
        # want to support that.
        if not isinstance(value, list):
            return None
        try:
            cur_value = value[node['value']]

            self.on_visit_leaf(value, node['value']) # ADDED

            return cur_value
        except IndexError:
            return None

    def visit_index_expression(self, node, value):
        result = value

        length = len(node['children'])
        for i, node in enumerate(node['children']):
            result = self.visit(node, result)

        return result

    def visit_slice(self, node, value):
        if not isinstance(value, list):
            return None
        s = slice(*node['children'])
        return value[s]

    def visit_key_val_pair(self, node, value):
        return self.visit(node['children'][0], value)

    def visit_literal(self, node, value):
        return node['value']

    def visit_multi_select_dict(self, node, value):
        if value is None:
            return None
        collected = self._dict_cls()
        for child in node['children']:
            collected[child['value']] = self.visit(child, value)
        return collected

    def visit_multi_select_list(self, node, value):
        if value is None:
            return None
        collected = []
        for child in node['children']:
            collected.append(self.visit(child, value))
        return collected

    def visit_or_expression(self, node, value):
        matched = self.visit(node['children'][0], value)
        if self._is_false(matched):
            matched = self.visit(node['children'][1], value)
        return matched

    def visit_and_expression(self, node, value):
        matched = self.visit(node['children'][0], value)
        if self._is_false(matched):
            return matched
        return self.visit(node['children'][1], value)

    def visit_not_expression(self, node, value):
        original_result = self.visit(node['children'][0], value)
        if type(original_result) is int and original_result == 0:
            # Special case for 0, !0 should be false, not true.
            # 0 is not a special cased integer in jmespath.
            return False
        return not original_result

    def visit_pipe(self, node, value):
        result = value
        for node in node['children']:
            result = self.visit(node, result)
        return result

    def visit_projection(self, node, value):
        self.increment_visits(node)

        base = self.visit(node['children'][0], value)
        if not isinstance(base, list):
            return None
        collected = []

        for i, element in enumerate(base):
            child = node['children'][1]

            current = self.visit(child, element)

            # ADDED, replacement won't happen if child is identity, try it here
            if child['type'] == 'identity':
                self.on_visit_leaf(base, i)

            if current is not None:
                collected.append(current)

        return collected

    def visit_value_projection(self, node, value):
        base = self.visit(node['children'][0], value)
        try:
            base = base.values()
        except AttributeError:
            return None
        collected = []
        for element in base:
            current = self.visit(node['children'][1], element)
            if current is not None:
                collected.append(current)
        return collected

    def _is_false(self, value):
        # This looks weird, but we're explicitly using equality checks
        # because the truth/false values are different between
        # python and jmespath.
        return (value == '' or value == [] or value == {} or value is None or
                value is False)

    def _is_true(self, value):
        return not self._is_false(value)


class GraphvizVisitor(Visitor):
    def __init__(self):
        super(GraphvizVisitor, self).__init__()
        self._lines = []
        self._count = 1

    def visit(self, node, *args, **kwargs):
        self._lines.append('digraph AST {')
        current = '%s%s' % (node['type'], self._count)
        self._count += 1
        self._visit(node, current)
        self._lines.append('}')
        return '\n'.join(self._lines)

    def _visit(self, node, current):
        self._lines.append('%s [label="%s(%s)"]' % (
            current, node['type'], node.get('value', '')))
        for child in node.get('children', []):
            child_name = '%s%s' % (child['type'], self._count)
            self._count += 1
            self._lines.append('  %s -> %s' % (current, child_name))
            self._visit(child, child_name)
