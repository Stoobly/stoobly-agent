import sys

from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys import InvalidProjectKey, InvalidReportKey, InvalidRequestKey, InvalidScenarioKey
from stoobly_agent.lib.api.keys import ProjectKey, ReportKey, RequestKey, ScenarioKey
from stoobly_agent.lib.logger import Logger

# Handle

def handle_invalid_project_key():
  print('Error: Invalid project key', file=sys.stderr) 
  sys.exit(1)

def handle_invalid_report_key():
  print('Error: Invalid report key', file=sys.stderr) 
  sys.exit(1)

def handle_invalid_request_key():
  print('Error: Invalid request key', file=sys.stderr) 
  sys.exit(1)

def handle_invalid_scenario_key():
  print('Error: Invalid scenario key', file=sys.stderr) 
  sys.exit(1)

# Validate

def validate_project_key(project_key) -> ProjectKey:
    try:
        return ProjectKey(project_key)
    except InvalidProjectKey:
        handle_invalid_project_key()

def validate_report_key(report_key) -> ReportKey:
  try:
    return ReportKey(report_key)
  except InvalidReportKey:
    handle_invalid_report_key()

def validate_request_key(request_key) -> RequestKey:
  try:
    return RequestKey(request_key)
  except InvalidRequestKey:
    handle_invalid_request_key()

def validate_scenario_key(scenario_key) -> ScenarioKey:
    try:
        return ScenarioKey(scenario_key)
    except InvalidScenarioKey:
        handle_invalid_scenario_key()

# Resolve

def resolve_project_key(kwargs: dict, settings: Settings) -> str:
    project_key = kwargs.get('project_key')

    if not project_key:
      project_key = settings.proxy.intercept.project_key
      #Logger.instance().info(f"No project key specified, using {project_key}")

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