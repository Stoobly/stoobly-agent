
import click

from stoobly_agent.lib.intercepted_requests_logger import InterceptedRequestsLogger


@click.group(help="Manage intercepted requests logs")
def log():
  pass

@log.command(help="Dump intercepted requests log")
@click.option('--requests-log-path', help='Path to the intercepted requests log')
def dump(**kwargs):
  requests_log_path = kwargs.get('requests_log_path')
  if requests_log_path:
    InterceptedRequestsLogger.set_file_path(requests_log_path)

  InterceptedRequestsLogger.dump_logs()

@log.command(help="Clear intercepted requests log")
@click.option('--requests-log-path', help='Path to the intercepted requests log')
def clear(**kwargs):
  requests_log_path = kwargs.get('requests_log_path')
  if requests_log_path:
    InterceptedRequestsLogger.set_file_path(requests_log_path)

  InterceptedRequestsLogger.truncate()

