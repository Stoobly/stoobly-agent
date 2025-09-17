
import click

from stoobly_agent.lib.intercepted_requests_logger import InterceptedRequestsLogger


@click.group(help="Manage intercepted requests logs")
def log():
  pass

@log.command(help="List intercepted requests log entries")
@click.option('--request-log-file-path', help='Path to the intercepted requests log')
def list(**kwargs):
  request_log_file_path = kwargs.get('request_log_file_path')
  if request_log_file_path:
    InterceptedRequestsLogger.set_file_path(request_log_file_path)

  InterceptedRequestsLogger.dump_logs()

@log.command(help="Delete intercepted requests log entries")
@click.option('--request-log-file-path', help='Path to the intercepted requests log')
def delete(**kwargs):
  request_log_file_path = kwargs.get('request_log_file_path')
  if request_log_file_path:
    InterceptedRequestsLogger.set_file_path(request_log_file_path)

  InterceptedRequestsLogger.truncate()

