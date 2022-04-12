import click
import json
import time

from stoobly_agent.app.settings import Settings

@click.group(
    epilog="Run 'stoobly-agent config COMMAND --help' for more information on a command.",
    help="Manage proxy config"
)
@click.pass_context
def config(ctx):
    pass

@config.command()
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