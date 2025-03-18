from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from typing import List

from stoobly_agent.app.settings.constants.request_component import REQUEST_COMPONENTS, RESPONSE_COMPONENTS
from stoobly_agent.app.settings.rewrite_rule import RewriteRule

from ..mitmproxy.request_facade import MitmproxyRequestFacade
from ..mitmproxy.response_facade import MitmproxyResponseFacade

def select_request_rewrite_rules(rewrite_rules: List[RewriteRule]):
  rules = []

  for rewrite_rule in rewrite_rules:
    parameter_rules = list(filter(
      lambda parameter: parameter.type in REQUEST_COMPONENTS and parameter.name, 
      rewrite_rule.parameter_rules or []
    ))

    if len(parameter_rules) > 0:
      rewrite_rule = RewriteRule(rewrite_rule.to_dict())
      rewrite_rule.url_rules = rewrite_rule.url_rules
      rewrite_rule.parameter_rules = parameter_rules
      rules.append(rewrite_rule)

  return rules

def select_response_rewrite_rules(rewrite_rules: List[RewriteRule]):
  rules = []

  for rewrite_rule in rewrite_rules:
    parameter_rules = list(filter(
      lambda parameter: parameter.type in RESPONSE_COMPONENTS and parameter.name, 
      rewrite_rule.parameter_rules or []
    ))

    if len(parameter_rules) > 0:
      rewrite_rule = RewriteRule(rewrite_rule.to_dict())
      rewrite_rule.url_rules = [] 
      rewrite_rule.parameter_rules = parameter_rules
      rules.append(rewrite_rule)

  return rules

def rewrite_request_response(flow: MitmproxyHTTPFlow, rewrite_rules: List[RewriteRule]):
  request = rewrite_request(flow, rewrite_rules)
  response = rewrite_response(flow, rewrite_rules, request)
  return request, response

def rewrite_request(flow: MitmproxyHTTPFlow, rewrite_rules: List[RewriteRule]):
  request = None

  # Adapt flow.request
  request = MitmproxyRequestFacade(flow.request)

  _rewrite_rules = select_request_rewrite_rules(rewrite_rules) 
  if len(_rewrite_rules):
    request.with_parameter_rules(_rewrite_rules).with_url_rules(_rewrite_rules).rewrite()

  return request

def rewrite_response(flow: MitmproxyHTTPFlow, rewrite_rules: List[RewriteRule], request = None):
  # Adapt flow.request
  request = request or MitmproxyRequestFacade(flow.request)

  # Adapt flow.response
  response = MitmproxyResponseFacade(flow.response)

  _rewrite_rules = select_response_rewrite_rules(rewrite_rules)
  if len(_rewrite_rules):
    response.with_parameter_rules(_rewrite_rules, request).rewrite()

  return response