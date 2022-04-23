import click

from stoobly_agent.app.cli.helpers import run_command, run_command_with_proxy_export
from stoobly_agent.app.settings import Settings

class ExecDecorator():
  def __init__(self, main):
    self.__main = main

  def decorate(self):
    @self.__main.command(
      help="Run shell command with proxy enabled"
    )
    @click.option('--command', is_flag=True, default=False, help='Read commands from the command_string operand instead of from the standard input.')
    @click.option('--shell', default='sh', help='Shell script to run interpret command(s).')
    @click.argument('file_path')
    def exec(**kwargs):
        is_command = kwargs['command']
        shell = kwargs['shell']
        file_path = kwargs['file_path']

        settings = Settings.instance()
        proxy_url = settings.proxy.url

        if not proxy_url:
            run_command(shell, file_path, is_command)
        else:
            run_command_with_proxy_export(shell, file_path, is_command, proxy_url)