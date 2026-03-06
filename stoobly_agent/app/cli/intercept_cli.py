import click
import pdb
import sys

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode, mock_policy, record_order, record_policy, record_strategy, replay_policy, test_strategy
from stoobly_agent.lib.api.keys.project_key import ProjectKey

mode_options = [mode.MOCK, mode.RECORD, mode.REPLAY]
settings: Settings = Settings.instance()

if settings.cli.features.remote:
    mode_options.append(mode.TEST)

active_mode = settings.proxy.intercept.mode

def __get_order_options(active_mode: str) -> list[str]:
    if active_mode == mode.RECORD:
        return [record_order.APPEND, record_order.OVERWRITE]
    else:
        return []

def __get_policy_options(active_mode: str) -> list[str]:
    if active_mode == mode.MOCK:
        return [mock_policy.ALL, mock_policy.FOUND]
    elif active_mode == mode.RECORD:
        return [record_policy.ALL, record_policy.API, record_policy.FOUND, record_policy.NOT_FOUND]
    elif active_mode == mode.REPLAY:
        return [replay_policy.ALL]
    elif active_mode == mode.TEST:
        return [mock_policy.FOUND]
    else:
        return []

def __get_strategy_options(active_mode: str) -> list[str]:
    if active_mode == mode.RECORD:
        return [record_strategy.FULL, record_strategy.MINIMAL]
    elif active_mode == mode.TEST:
        return [test_strategy.CONTRACT, test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY]
    else:
        return []

order_options = __get_order_options(active_mode)
policy_options = __get_policy_options(active_mode)
strategy_options = __get_strategy_options(active_mode)

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
    from .helpers.handle_config_update_service import handle_intercept_active_update
    settings = Settings.instance()

    settings.proxy.intercept.active = True

    handle_intercept_active_update(settings)

    settings.commit()

    print("Intercept enabled!")

@intercept.command(
    help="Disable intercept"
)
def disable(**kwargs):
    from .helpers.handle_config_update_service import handle_intercept_active_update
    settings = Settings.instance()

    settings.proxy.intercept.active = False

    handle_intercept_active_update(settings)

    settings.commit()

    print("Intercept disabled!")

@intercept.command(
    help="Configure intercept"
)
@click.option('--mode', type=click.Choice(mode_options))
@click.option('--order', help=f"Order to use for recording. Valid options: {order_options}")
@click.option('--policy', help=f"Policy to use for recording. Valid options: {policy_options}")
@click.option('--strategy', help=f"Strategy to use for recording. Valid options: {strategy_options}")
def configure(**kwargs):
    settings: Settings = Settings.instance()

    if not kwargs['mode'] and not kwargs['order'] and not kwargs['policy'] and not kwargs['strategy']:
        print("Error: Missing an option")
        sys.exit(1)

    if kwargs['mode']:
        if settings.proxy.intercept.mode != kwargs['mode']:
            if settings.proxy.intercept.active:
                from .helpers.handle_config_update_service import handle_intercept_active_update

                settings.proxy.intercept.active = False
                handle_intercept_active_update(settings)

            settings.proxy.intercept.mode = kwargs['mode']

            print(f"Updating intercept mode to {kwargs['mode']}")

    _mode = kwargs['mode'] or settings.proxy.intercept.mode 

    if kwargs['order']:
        active_mode = settings.proxy.intercept.mode

        if active_mode == mode.RECORD:
            project_key = ProjectKey(settings.proxy.intercept.project_key)
            data_rule = settings.proxy.data.data_rules(project_key.id)
            data_rule.record_order = kwargs['order']
        else:
            print("Error: set --mode to a intercept mode that supports the order option", file=sys.stderr)
            sys.exit(1)

        from .helpers.handle_config_update_service import handle_order_update
        handle_order_update(settings)

        print(f"Updating {_mode} order to {kwargs['order']}")

    if kwargs['policy']:
        active_mode = settings.proxy.intercept.mode
        valid_policies = __get_policy_options(active_mode)

        if kwargs['policy'] not in valid_policies:
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

        print(f"Updating {_mode} policy to {kwargs['policy']}")

    if kwargs['strategy']:
        active_mode = settings.proxy.intercept.mode

        if active_mode == mode.RECORD or active_mode == mode.TEST:
            project_key = ProjectKey(settings.proxy.intercept.project_key)
            data_rule = settings.proxy.data.data_rules(project_key.id)

            if active_mode == mode.RECORD:
                data_rule.record_strategy = kwargs['strategy']
            elif active_mode == mode.TEST:
                data_rule.test_strategy = kwargs['strategy']
        else:
            print("Error: set --strategy to a intercept mode that supports the strategy option", file=sys.stderr)
            sys.exit(1)

        from .helpers.handle_config_update_service import handle_strategy_update
        handle_strategy_update(settings)

        print(f"Updating {_mode} policy to {kwargs['strategy']}")


    settings.commit()

@intercept.command(
    help="Show intercept"
)
def show(**kwargs):
    settings: Settings = Settings.instance()

    _mode = settings.proxy.intercept.mode
    project_key = ProjectKey(settings.proxy.intercept.project_key)
    data_rule = settings.proxy.data.data_rules(project_key.id)
    policy = None
    strategy = None

    if active_mode == mode.MOCK:
        policy = data_rule.mock_policy
    elif active_mode == mode.RECORD:
        policy = data_rule.record_policy
        strategy = data_rule.record_strategy
    elif active_mode == mode.REPLAY:
        policy = data_rule.replay_policy
    elif active_mode == mode.TEST:
        policy = data_rule.test_policy
        strategy = data_rule.test_strategy

    if not _mode:
        print('No intercept mode set')
    else:
        print(f"{_mode.capitalize()} with policy: '{policy}', strategy: '{strategy}', {'enabled' if settings.proxy.intercept.active else 'disabled'}")
