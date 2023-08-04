import click
import pdb
import sys

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode, mock_policy, record_policy, replay_policy
from stoobly_agent.lib.api.keys.project_key import ProjectKey

from .helpers.handle_config_update_service import handle_intercept_active_update, handle_policy_update

settings = Settings.instance()

mode_options = [mode.MOCK, mode.RECORD, mode.REPLAY]

if settings.cli.features.remote:
    mode_options.append(mode.TEST)

active_mode = settings.proxy.intercept.mode

def __get_policy_options(active_mode):
    if active_mode == mode.MOCK:
        return [mock_policy.ALL, mock_policy.FOUND]
    elif active_mode == mode.RECORD:
        return [record_policy.ALL, record_policy.FOUND, record_policy.NOT_FOUND,record_policy.OVERWRITE]
    elif active_mode == mode.REPLAY:
        return [replay_policy.ALL]
    elif active_mode == mode.TEST:
        return [mock_policy.FOUND]

policy_options = __get_policy_options(active_mode)

@click.group(
    epilog="Run 'stoobly-agent intercept COMMAND --help' for more information on a command.",
    help="Manage request intercept"
)
@click.pass_context
def intercept(ctx):
    pass

@intercept.command(
    help="Enable intercept"
)
def enable(**kwargs):
    settings.proxy.intercept.active = True

    handle_intercept_active_update(settings)

    settings.commit()

    print("Intercept enabled!")

@intercept.command(
    help="Disable intercept"
)
def disable(**kwargs):
    settings = Settings.instance()

    settings.proxy.intercept.active = False

    handle_intercept_active_update(settings)

    settings.commit()

    print("Intercept disabled!")

@intercept.command(
    help="Configure intercept"
)
@click.option('--mode', type=click.Choice(mode_options))
@click.option('--policy', type=click.Choice(policy_options))
def configure(**kwargs):
    settings = Settings.instance()

    if not kwargs['mode'] and not kwargs['policy']:
        print("Error: Missing an option")
        sys.exit(1)

    if kwargs['mode']:
        if settings.proxy.intercept.mode != kwargs['mode']:
            if settings.proxy.intercept.active:
                settings.proxy.intercept.active = False
                handle_intercept_active_update(settings)

            settings.proxy.intercept.mode = kwargs['mode']

            print(f"Updating intercept mode to {kwargs['mode']}")

    _mode = kwargs['mode'] or settings.proxy.intercept.mode 

    if kwargs['policy']:
        active_mode = settings.proxy.intercept.mode
        valid_policies = __get_policy_options(active_mode)

        if not kwargs['policy'] in valid_policies:
            print("Error: Valid policies for {active_mode} are {valid_policies}", file=sys.stderr)
            sys.exit(1)

        project_key = ProjectKey(settings.proxy.intercept.project_key)
        data_rule = settings.proxy.data.data_rules(project_key.id)
        
        if active_mode == mode.MOCK:
            data_rule.mock_policy = kwargs['policy']
        elif active_mode == mode.RECORD:
            data_rule.record_policy = kwargs['policy']
        elif active_mode == mode.REPLAY:
            data_rule.replay_policy = kwargs['policy']
        elif active_mode == mode.TEST:
            data_rule.test_policy = kwargs['policy']

        handle_policy_update(settings)

        print(f"Updating {_mode} policy to {kwargs['policy']}")

    settings.commit()

@intercept.command(
    help="Show intercept"
)
def show(**kwargs):
    settings = Settings.instance()

    _mode = settings.proxy.intercept.mode
    project_key = ProjectKey(settings.proxy.intercept.project_key)
    data_rule = settings.proxy.data.data_rules(project_key.id)
    policy = None

    if active_mode == mode.MOCK:
        policy = data_rule.mock_policy
    elif active_mode == mode.RECORD:
        policy = data_rule.record_policy
    elif active_mode == mode.REPLAY:
        policy = data_rule.replay_policy
    elif active_mode == mode.TEST:
        policy = data_rule.test_policy

    if not _mode:
        print('No intercept mode set')
    else:
        print(f"{_mode.capitalize()} with policy {policy} {'enabled' if settings.proxy.intercept.active else 'disabled'}")
