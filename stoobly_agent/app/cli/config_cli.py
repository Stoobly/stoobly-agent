import click
import json
import pdb
import time

from typing import List

from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.app.settings.rewrite_rule import ParameterRule, RewriteRule
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.keys import ProjectKey, ScenarioKey
from stoobly_agent.lib.logger import Logger

from .helpers.validations import *

@click.group(
    epilog="Run 'stoobly-agent config COMMAND --help' for more information on a command.",
    help="Manage proxy config"
)
@click.pass_context
def config(ctx):
    pass

@config.command(
    help="Display config contents"
)
@click.option('--save-to-file', is_flag=True, default=False, help='To save to a file or not.')
def dump(**kwargs):
    settings = Settings.instance()

    output = json.dumps(settings.to_dict(), indent=2, sort_keys=True)

    if kwargs['save_to_file']:
        timestamp = str(int(time.time() * 1000))
        config_dump_file_name = f"stoobly_agent_config_dump_{timestamp}.json"

        with open(config_dump_file_name, 'w') as output_file:
            output_file.write(output)

        print(f"Config successfully dumped to {config_dump_file_name}")
    else:
        print(output)

is_remote = Settings.instance().cli.features.remote
if is_remote:
    @click.group(
        help="Manage active scenario."
    )
    @click.pass_context
    def scenario(ctx):
        pass

    @scenario.command(
        help="Set active scenario."
    )
    @click.argument('scenario_key')
    def set(**kwargs):
        settings = Settings.instance()

        scenario_key = ScenarioKey(kwargs['scenario_key'])
        validate_scenario_key(scenario_key)

        project_key = settings.proxy.intercept.project_key
        validate_project_key(project_key)
        project_key = ProjectKey(project_key)

        if scenario_key.project_id != project_key.id:
            return print("Please provide a scenario that belongs to the current project.\n")

        data_rule = settings.proxy.data.data_rules(project_key.id)
        data_rule.scenario_key = kwargs['scenario_key']
        settings.commit()

        print("Scenario updated!")

    @click.group(
        help="Manage active project."
    )
    @click.pass_context
    def project(ctx):
        pass

    @project.command(
        help="Set active project."
    )
    @click.argument('project_key')
    def set(**kwargs):
        settings = Settings.instance()

        project_key = kwargs['project_key']
        validate_project_key(project_key)
        _project_key = ProjectKey(project_key)

        data_rule = settings.proxy.data.data_rules(_project_key.id)
        scenario_key = data_rule.scenario_key

        if scenario_key:
            validate_scenario_key(scenario_key)
            scenario_key = ScenarioKey(scenario_key)

            if project_key.id != scenario_key.project_id:
                data_rule.scenario_key = None
                print("Current scenario does not belong to current project, unsetting current scenario.\n")

        settings.proxy.intercept.project_key = project_key 
        settings.commit()

        print("Project updated!")

    @click.group(
        help="Manage API key."
    )
    @click.pass_context
    def api_key(ctx):
        pass

    @api_key.command(
        help="Set API Key"
    )
    @click.argument('api_key')
    def set(**kwargs):
        settings = Settings.instance()

        api_key = kwargs['api_key']
        settings.remote.api_key = api_key

        settings.commit()

        print("API Key updated!")

    @click.group(
        help="Manage rewrite rules."
    )
    @click.pass_context
    def rewrite(ctx):
        pass

    @rewrite.command(
        help="Set rewrite rule."
    )
    @click.option(
        '--method', 
        multiple=True, 
        required=True,
        type=click.Choice(['GET', 'POST', 'DELETE', 'OPTIONS', 'PUT']), 
        help='HTTP methods.'
    )
    @click.option(
        '--mode',
        multiple=True,
        required=True,
        type=click.Choice([mode.MOCK, mode.RECORD, mode.REPLAY, mode.TEST])
    )
    @click.option('--name', required=True, help='Name of the request component.')
    @click.option('--pattern', required=True, help='URLs pattern.')
    @click.option('--project_key', help='Project to add rewrite rule to.')
    @click.option(
        '--type', 
        required=True,
        type=click.Choice([request_component.BODY_PARAM, request_component.HEADER, request_component.QUERY_PARAM]), 
        help='Request component type.'
    )
    @click.option('--value', required=True, help='Rewrite value.')
    def set(**kwargs):
        settings = Settings.instance()
        project_key_str = resolve_project_key_and_validate(kwargs, settings)
        project_key = ProjectKey(project_key_str)

        methods = list(kwargs['method'])
        modes = list(kwargs['mode'])
    
        rewrite_rules = settings.proxy.rewrite.rewrite_rules(project_key.id)

        rewrite_rule_filter = lambda rule: rule.pattern == kwargs['pattern'] and rule.methods == methods
        filtered_rewrite_rules: List[RewriteRule] = list(filter(rewrite_rule_filter, rewrite_rules))

        if len(filtered_rewrite_rules) == 0:
            rewrite_rule = RewriteRule({
                'methods': methods,
                'pattern': kwargs['pattern'],
                'parameter_rules': [__select_parameter_rule(kwargs)]
            })
            rewrite_rules.append(rewrite_rule)
            settings.proxy.rewrite.set_rewrite_rules(project_key.id, rewrite_rules)
        else:
            parameter_rule_filter = lambda rule: rule.name == kwargs['name'] and rule.type == kwargs['type'] and rule.modes == modes
            for rewrite_rule in filtered_rewrite_rules:
                parameter_rules = rewrite_rule.parameter_rules
                filtered_parameter_rules: List[ParameterRule] = list(filter(parameter_rule_filter, parameter_rules))
                parameter_rule_dict = __select_parameter_rule(kwargs)

                if len(filtered_parameter_rules) == 0:
                    parameter_rule = ParameterRule(parameter_rule_dict)
                    parameter_rules.append(parameter_rule)
                    rewrite_rule.parameter_rules = parameter_rules
                else:
                    for parameter_rule in filtered_parameter_rules:
                        parameter_rule.update(parameter_rule_dict)

        settings.commit()

        Logger.instance().debug(f"Rewrite {kwargs['name']} -> {kwargs['value']} set!")

    config.add_command(api_key)
    config.add_command(project)
    config.add_command(rewrite)
    config.add_command(scenario)

def __select_parameter_rule(kwargs):
    return {
        'modes': list(kwargs['mode']),
        'name': kwargs['name'],
        'value': kwargs['value'],
        'type': kwargs['type'],
    }