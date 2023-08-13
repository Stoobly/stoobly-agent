import pdb

from .parameter_rule import ParameterRule
from .types.proxy_settings import RewriteRule as IRewriteRule
from .url_rule import UrlRule

class RewriteRule:

  def __init__(self, rewrite_rule: IRewriteRule):
    self.__rewrite_rule = rewrite_rule

    self.__methods = self.__rewrite_rule.get('methods') or []
    self.__pattern = self.__rewrite_rule.get('pattern')

    self.__raw_parameter_rules = self.__rewrite_rule.get('parameter_rules') or []
    self.__parameter_rules = list(map(lambda rule: ParameterRule(rule), self.__raw_parameter_rules))

    self.__raw_url_rules = self.__rewrite_rule.get('url_rules') or []
    self.__url_rules = list(map(lambda rule: UrlRule(rule), self.__raw_url_rules))

  @property 
  def methods(self):
    return self.__methods

  @property
  def pattern(self):
    return self.__pattern

  @property
  def parameter_rules(self):
    return self.__parameter_rules

  @parameter_rules.setter
  def parameter_rules(self, v):
    self.__parameter_rules = v

  @property
  def url_rules(self):
    return self.__url_rules

  @url_rules.setter
  def url_rules(self, v):
    self.__url_rules = v

  def to_dict(self):
    return {
      'methods': self.__methods,
      'pattern': self.__pattern,
      'parameter_rules': list(map(lambda parameter: parameter.to_dict(), self.__parameter_rules)),
      'url_rules': list(map(lambda url: url.to_dict(), self.__url_rules)),
    }