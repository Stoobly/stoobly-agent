import click
import time

from ..settings import Settings

@click.group()
@click.pass_context
def config(ctx):
    pass

@config.command()
@click.option('--pretty-print', is_flag=True, default=False, help='Pretty print the json.')
@click.option('--save-to-file', is_flag=True, default=False, help='To save to a file or not.')
def dump(**kwargs):
    settings = Settings.instance()

    output = settings.to_json(pretty_print=kwargs['pretty_print'])

    if kwargs['save_to_file']:
        timestamp = str(int(time.time() * 1000))
        config_dump_file_name = f"stoobly_agent_config_dump_{timestamp}.json"

        with open(config_dump_file_name, 'w') as output_file:
            output_file.write(output)

        print(f"Config successfully dumped to {config_dump_file_name}")
    else:
        print(output)