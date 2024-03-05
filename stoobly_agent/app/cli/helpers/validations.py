import json
import pdb
import click
import re
import sys

from typing import Union

from stoobly_agent.app.cli.helpers.handle_replay_service import DEFAULT_FORMAT, JSON_FORMAT
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys import InvalidOrganizationKey, InvalidProjectKey, InvalidReportKey, InvalidRequestKey, InvalidScenarioKey
from stoobly_agent.lib.api.keys import OrganizationKey, ProjectKey, ReportKey, RequestKey, ScenarioKey

from .trace_aliases import adapt_trace_aliases, Alias, parse_aliases

# Print

def print_invalid_key(resource: str, format = DEFAULT_FORMAT):
  error_message = f"Error: Invalid {resource} key"

  if format == JSON_FORMAT:
    print_error_json_format(error_message)
  else:
    print(error_message, file=sys.stderr) 

def print_error_json_format(error_message):
    output = { 'error': error_message }
    print(json.dumps(output), file=sys.stderr)

# Handle

def handle_invalid_key(resource: str, format = DEFAULT_FORMAT):
  print_invalid_key(resource, format)
  sys.exit(1)

def handle_missing_key(resource: str, format = DEFAULT_FORMAT):
  error_message = f"Error: Missing {resource} key"

  if format == JSON_FORMAT:
    print_error_json_format(error_message)
  else:
    print(error_message, file=sys.stderr) 

  sys.exit(1)

def handle_invalid_alias(expected_alias: Alias, alias_value: str, format = DEFAULT_FORMAT):
  error_message = f"Error: Invalid alias {expected_alias['name']} value, got {alias_value}, expected {expected_alias['value']}"

  if format == JSON_FORMAT:
    print_error_json_format(error_message)
  else:
    print(error_message, file=sys.stderr) 

  sys.exit(1)

def handle_missing_alias(expected_alias: Alias, format = DEFAULT_FORMAT):
  error_message = f"Error: Missing alias {expected_alias['name']}"

  if format == JSON_FORMAT:
    print_error_json_format(error_message)
  else:
    print(error_message, file=sys.stderr)

  sys.exit(1)

# Validate

def validate_organization_key(organization_key) -> OrganizationKey:
  try:
    return OrganizationKey(organization_key)
  except InvalidOrganizationKey:
    handle_invalid_key('organization') if organization_key else handle_missing_key('organization')

def validate_project_key(project_key) -> ProjectKey:
  try:
    return ProjectKey(project_key)
  except InvalidProjectKey:
    handle_invalid_key('project') if project_key else handle_missing_key('project')

def validate_report_key(report_key) -> ReportKey:
  try:
    return ReportKey(report_key)
  except InvalidReportKey:
    handle_invalid_key('report') if report_key else handle_missing_key('report')

def validate_request_key(request_key) -> RequestKey:
  try:
    request_key = RequestKey(request_key)
    project_key = ProjectKey(Settings.instance().proxy.intercept.project_key)

    is_local = ProjectKey.check_is_local(request_key.project_id)
    if project_key.is_local != is_local:
      raise InvalidRequestKey(f"Error: Change to {'local' if is_local else 'remote'} project")

    return request_key
  except InvalidRequestKey:
    handle_invalid_key('request') if request_key else handle_missing_key('request')

def validate_scenario_key(scenario_key) -> ScenarioKey:
  try:
    scenario_key = ScenarioKey(scenario_key)
    project_key = ProjectKey(Settings.instance().proxy.intercept.project_key)

    is_local = ProjectKey.check_is_local(scenario_key.project_id)
    if project_key.is_local != is_local:
      raise InvalidRequestKey(f"Error: Change to {'local' if is_local else 'remote'} project")

    return scenario_key
  except InvalidScenarioKey:
    handle_invalid_key('scenario') if scenario_key else handle_missing_key('scenario')

def validate_aliases(validations, **kwargs) -> Union[Alias, None]:
  assigns = kwargs.get('assign')
  trace_id = kwargs.get('trace_id')

  aliases = parse_aliases(assigns) + adapt_trace_aliases(trace_id)
  aliases_map = {}
  for _alias in aliases:
    aliases_map[_alias.get('name')] = _alias.get('value')

  for validation in validations:
    parsed_validation = parse_aliases([validation])[0]
    name = parsed_validation['name']

    if name not in aliases_map or not aliases_map[name]:
      handle_missing_alias(parsed_validation, kwargs.get('format'))

    if parsed_validation['value'] != None:
      if not re.match(parsed_validation['value'], aliases_map[name]):
        handle_invalid_alias(parsed_validation, aliases_map[name], kwargs.get('format'))

def filter_response(res, status: int):
    if status != 0 and status < 400:
        return False

    print(f"Error: {res}", file=sys.stderr)

    return True

# Prompt

def prompt_project_key(settings: Settings):
  while True:
    project_key = click.prompt('Please enter a project key', type=str)

    try:
      ProjectKey(project_key)
      break
    except InvalidProjectKey:
      print_invalid_key('project')
      print(f"Try `stoobly-agent project list` to find a project key", file=sys.stderr) 

  settings.proxy.intercept.project_key = project_key
  settings.commit()

  return project_key

# Resolve

def resolve_project_key(kwargs: dict, settings: Settings) -> str:
    project_key = kwargs.get('project_key')

    if not project_key:
      project_key = settings.proxy.intercept.project_key

      if not project_key or len(project_key) == 0:
        project_key = prompt_project_key(settings)

    return project_key

def resolve_project_key_and_validate(kwargs: dict, settings: Settings  = Settings.instance()) -> str:
    project_key = resolve_project_key(kwargs, settings)

    validate_project_key(project_key)

    return project_key

def resolve_scenario_key(kwargs: dict, settings: Settings) -> str:
    scenario_key = kwargs.get('key')

    if not scenario_key:
        project_key = validate_project_key(settings.proxy.intercept.project_key)
        data_rule = settings.proxy.data.data_rules(project_key.id)
        scenario_key = data_rule.scenario_key
        #Logger.instance().info(f"No scenario key specified, using {scenario_key}")

    return scenario_key

def resolve_scenario_key_and_validate(kwargs: dict, settings: Settings = Settings.instance()) -> str:
    scenario_key = resolve_scenario_key(kwargs, settings)

    validate_scenario_key(scenario_key)

    return scenario_key