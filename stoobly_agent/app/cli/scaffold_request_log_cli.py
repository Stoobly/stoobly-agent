import click

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests.scaffold_logger import ScaffoldInterceptedRequestsLogger

data_dir: DataDir = DataDir.instance()

@click.group(
  epilog="Run 'stoobly-agent scaffold request COMMAND --help' for more information on a command.",
  help="Manage scaffold request logs"
)
@click.pass_context
def request(ctx):
    pass


@click.group(
  epilog="Run 'stoobly-agent scaffold request log COMMAND --help' for more information on a command.",
  help="Manage intercepted requests logs for workflows"
)
@click.pass_context
def request_log(ctx):
    pass

@request_log.command(name="path", help="Get intercepted requests log path")
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--namespace', help='Workflow namespace to get logs for.')
@click.argument('workflow_name')
def request_log_path(**kwargs):
    context_dir_path = kwargs.get('context_dir_path') or DataDir.instance().context_dir_path
    ScaffoldInterceptedRequestsLogger.get_log_file_path(
        workflow=kwargs.get('workflow_name'),
        namespace=kwargs.get('namespace'),
        data_dir_path=context_dir_path
    )

@request_log.command(name="list", help="List intercepted requests log entries")
@click.option('--context-dir-path', default=None, help='Path to Stoobly data directory.')
@click.option('--namespace', help='Workflow namespace to list logs for.')
@click.argument('workflow_name')
def request_log_list(**kwargs):
    context_dir_path = kwargs.get('context_dir_path') or DataDir.instance().context_dir_path
    ScaffoldInterceptedRequestsLogger.dump_logs(
        workflow=kwargs.get('workflow_name'),
        namespace=kwargs.get('namespace'),
        data_dir_path=context_dir_path
    )

@request_log.command(name="delete", help="Delete intercepted requests log entries")
@click.option('--context-dir-path', default=None, help='Path to Stoobly data directory.')
@click.option('--namespace', help='Workflow namespace to delete logs for.')
@click.argument('workflow_name')
def request_log_delete(**kwargs):
    context_dir_path = kwargs.get('context_dir_path') or DataDir.instance().context_dir_path
    ScaffoldInterceptedRequestsLogger.truncate(
        workflow=kwargs.get('workflow_name'),
        namespace=kwargs.get('namespace'),
        data_dir_path=context_dir_path
    )

request.add_command(request_log, name="log")
