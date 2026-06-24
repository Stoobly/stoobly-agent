import os
import json
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
  from mitmproxy.http import Request as MitmproxyRequest, Response as MitmproxyResponse

from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_NAMESPACE_ENV, SERVICE_NAME_ENV
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.config.constants import custom_headers


class JSONFormatter(logging.Formatter):
  """Formats log records as JSON entries."""

  def __init__(
    self,
    settings: Settings,
    get_scenario_name: Callable[[str], Optional[str]] = None,
    extract_request_key: Callable = None,
    should_log_context_dir_path: Callable[[], bool] = None,
    get_context_dir_path: Callable[[], str] = None,
  ):
    super().__init__()
    self.__settings = settings
    self.__get_scenario_name = get_scenario_name
    self.__extract_request_key = extract_request_key
    self.__should_log_context_dir_path = should_log_context_dir_path
    self.__get_context_dir_path = get_context_dir_path

  def format(self, record: logging.LogRecord) -> str:
    timestamp = datetime.fromtimestamp(record.created)

    # Handle delimiter entries such as when changing scenarios
    if hasattr(record, 'delimiter'):
      delimiter_entry = {
        "timestamp": datetime.fromtimestamp(record.created).isoformat(),
        **record.delimiter
      }
      return json.dumps(delimiter_entry)

    log_entry = {
      "timestamp": timestamp.isoformat(),
      "level": record.levelname,
      "message": record.getMessage()
    }

    request = None

    # Extract fields from request
    if hasattr(record, 'request') and record.request is not None:
      # Lazy import for runtime usage
      request: 'MitmproxyRequest' = record.request
      agent = request.headers.get("User-Agent", None)

      if agent:
        log_entry.update({
          "user_agent": agent
        })

      url = request.pretty_url

      log_entry.update({
        "method": request.method,
        "url": url,
      })

    # Extract fields from response
    if hasattr(record, 'response') and record.response is not None:
      response: 'MitmproxyResponse' = record.response
      log_entry.update({
        "status_code": response.status_code,
      })

      if request:
        # Calculate latency
        latency = timestamp.timestamp() - request.timestamp_start
        latency_ms = round(latency * 1000)
        log_entry.update({
          "latency_ms": latency_ms
        })

    # Set test title if available in request headers
    test_title = ""
    if request and hasattr(request, 'headers') and request.headers:
      test_title = request.headers.get(custom_headers.TEST_TITLE, "")
      if test_title:
        log_entry.update({
          "test_title": test_title
        })

    # Set scenario key
    intercept_settings = InterceptSettings(self.__settings, request=request)
    scenario_key = intercept_settings.scenario_key
    log_entry.update({
      "scenario_key": scenario_key
    })

    # Set scenario name if scenario_key is set; fall back to header when test_title is present
    scenario_name = ""
    if scenario_key and self.__get_scenario_name:
      scenario_name = self.__get_scenario_name(scenario_key)
      log_entry.update({
        "scenario_name": scenario_name
      })
    elif not scenario_key and test_title:
      scenario_name = request.headers.get(custom_headers.SCENARIO_NAME, "")
      if scenario_name:
        log_entry.update({
          "scenario_name": scenario_name
        })

    # Set scaffold service name
    service_name = ""
    env_var_service_name = os.environ.get(SERVICE_NAME_ENV)
    if env_var_service_name:
      service_name = env_var_service_name
      log_entry.update({
        "service_name": service_name
      })

    # Set scaffold namespace name
    env_var_namespace_name = os.environ.get(WORKFLOW_NAMESPACE_ENV)
    if env_var_namespace_name:
      log_entry.update({
        "namespace": env_var_namespace_name
      })

    if self.__should_log_context_dir_path and self.__should_log_context_dir_path():
      log_entry.update({
        "context_dir_path": self.__get_context_dir_path()
      })

    # Set request key and UI URL - prioritize passed-in value, fallback to response headers
    request_key = None

    # Check for passed-in request_key first
    if hasattr(record, 'request_key') and record.request_key is not None:
      request_key = record.request_key
    # Fallback to extracting from response headers
    elif hasattr(record, 'response') and record.response is not None:
      request_key = self.__extract_request_key(record.response)

    if request_key:
      log_entry.update({
        "request_key": request_key
      })

    # Set fixture path if provided
    if hasattr(record, 'fixture_path') and record.fixture_path is not None:
      log_entry.update({
        "fixture_path": record.fixture_path
      })

    return json.dumps(log_entry)
