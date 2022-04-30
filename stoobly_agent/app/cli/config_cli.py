import click
import json
import sys
import time

from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys import ProjectKey, ScenarioKey

from .helpers.validations import *

@click.group(
    epilog="Run 'stoobly-agent config COMMAND --help' for more information on a command.",
    help="Manage proxy config"
)
@click.pass_context
def config(ctx):
    pass

@config.command(
    help="Display config contents."
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
        project_key = ProjectKey(project_key)

        data_rule = settings.proxy.data.data_rules(project_key.id)
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

    config.add_command(project)
    config.add_command(scenario)