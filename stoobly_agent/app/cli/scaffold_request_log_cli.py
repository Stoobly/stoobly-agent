import click

from stoobly_agent.app.cli.helpers.log_options import build_log_filters, log_list_options
from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests.scaffold_logger import ScaffoldInterceptedRequestsLogger

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
@click.option('--context-dir-path', default=None, help='Path to Stoobly data directory.')
@click.option('--namespace', help='Workflow namespace to get logs for.')
@click.argument('workflow_name')
def request_log_path(**kwargs):
    context_dir_path = kwargs.get('context_dir_path') or DataDir.instance().context_dir_path
    app = App(context_dir_path)
    workflow_namespace = WorkflowNamespace(app, kwargs.get('namespace') or kwargs.get('workflow_name'))

    ScaffoldInterceptedRequestsLogger.get_log_file_path(
        workflow=kwargs.get('workflow_name'),
        namespace=kwargs.get('namespace'),
        workflow_namespace=workflow_namespace,
    )

@request_log.command(name="list", help="List intercepted requests log entries")
@click.option('--context-dir-path', default=None, help='Path to Stoobly data directory.')
@click.option('--namespace', help='Workflow namespace to list logs for.')
@click.option('--service-name', default=None, help='Filter by service name.')
@log_list_options
@click.argument('workflow_name')
def request_log_list(**kwargs):
    context_dir_path = kwargs.get('context_dir_path') or DataDir.instance().context_dir_path
    app = App(context_dir_path)
    workflow_namespace = WorkflowNamespace(app, kwargs.get('namespace') or kwargs.get('workflow_name'))
    filters = build_log_filters(kwargs, extra_keys=['service_name', 'namespace'])

    ScaffoldInterceptedRequestsLogger.dump_logs(
        workflow=kwargs.get('workflow_name'),
        namespace=kwargs.get('namespace'),
        workflow_namespace=workflow_namespace,
        filters=filters if filters else None,
        output_format=kwargs.get('format'),
        select=kwargs.get('select'),
        without_headers=kwargs.get('without_headers', False),
    )

@request_log.command(name="delete", help="Delete intercepted requests log entries")
@click.option('--context-dir-path', default=None, help='Path to Stoobly data directory.')
@click.option('--namespace', help='Workflow namespace to delete logs for.')
@click.argument('workflow_name')
def request_log_delete(**kwargs):
    context_dir_path = kwargs.get('context_dir_path') or DataDir.instance().context_dir_path
    app = App(context_dir_path)
    workflow_namespace = WorkflowNamespace(app, kwargs.get('namespace') or kwargs.get('workflow_name'))
    
    ScaffoldInterceptedRequestsLogger.truncate(
        workflow=kwargs.get('workflow_name'),
        namespace=kwargs.get('namespace'),
        workflow_namespace=workflow_namespace,
    )

request.add_command(request_log, name="log")
