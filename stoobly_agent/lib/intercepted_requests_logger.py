
import os
import logging
import json
from datetime import datetime
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from requests import Response
    from mitmproxy.http import Request as MitmproxyRequest, Response as MitmproxyResponse

from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_NAMESPACE_ENV, SERVICE_NAME_ENV
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey, InvalidScenarioKey
from stoobly_agent.lib.api.keys.request_key import RequestKey, InvalidRequestKey
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.logger import DEBUG, ERROR, INFO, WARNING, Logger
from stoobly_agent.config.constants import custom_headers


class InterceptedRequestsLogger():
    __LOG_ID: Final[str] = "InterceptedRequestsLogger"
    __logger: Logger = Logger.instance(__LOG_ID)

    __settings: Settings = Settings.instance()
    __NAMESPACE: str = os.environ.get(WORKFLOW_NAMESPACE_ENV, __settings.proxy.intercept.mode)
    __file_path: str = None
    __previous_scenario_key: str = None

    # Initialize logger as disabled by default
    __logger.disabled = True

    class JSONFormatter(logging.Formatter):
        def __init__(self, settings: Settings):
            super().__init__()
            self.__settings = settings

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

                # Truncate URL to 100 characters
                if len(url) > 100:
                    url = url[:100] + '...'

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

            # Set scenario key
            intercept_settings = InterceptSettings(self.__settings)
            scenario_key = intercept_settings.scenario_key
            log_entry.update({
                "scenario_key": scenario_key
            })

            # Set scenario name if scenario_key is set
            scenario_name = ""
            if scenario_key:
                scenario_name = InterceptedRequestsLogger._get_scenario_name(scenario_key)
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

            # Set request key and UI URL - prioritize passed-in value, fallback to response headers
            request_key = None

            # Check for passed-in request_key first
            if hasattr(record, 'request_key') and record.request_key is not None:
                request_key = record.request_key
            # Fallback to extracting from response headers
            elif hasattr(record, 'response') and record.response is not None:
                request_key = InterceptedRequestsLogger._extract_request_key(record.response)

            if request_key:
                log_entry.update({
                    "request_key": request_key
                })

            # Set fixture path if provided
            if hasattr(record, 'fixture_path') and record.fixture_path is not None:
                log_entry.update({
                    "fixture_path": record.fixture_path
                })

            # Set test title if available in request headers
            if hasattr(record, 'request') and record.request is not None:
                request: 'MitmproxyRequest' = record.request
                if hasattr(request, 'headers') and request.headers:
                    test_title = request.headers.get(custom_headers.TEST_TITLE, "")
                    if test_title:
                        log_entry.update({
                            "test_title": test_title
                        })

            return json.dumps(log_entry)

    @classmethod
    def set_file_path(cls, file_path: str) -> None:
        cls.__file_path = file_path

    @classmethod
    def reset_scenario_key(cls) -> None:
        cls.__previous_scenario_key = None

    @classmethod
    def set_log_level(cls, log_level: str) -> None:
        # Convert string log level to Python standard logging constants
        level_mapping = {
            DEBUG: logging.DEBUG,
            INFO: logging.INFO,
            WARNING: logging.WARNING,
            ERROR: logging.ERROR,
        }

        numeric_level = level_mapping.get(log_level.lower())
        if numeric_level is None:
            raise ValueError(f"Invalid log level: {log_level}. Must be one of: {', '.join(level_mapping.keys())}")
        cls.__logger.setLevel(numeric_level)

    @classmethod
    def _get_scenario_name(cls, scenario_key: str) -> str:
        if not scenario_key:
            return None

        try:
            parsed_key = ScenarioKey(scenario_key)
            scenario = Scenario.find_by(uuid=parsed_key.id)
            return scenario.name if scenario else None
        except (InvalidScenarioKey, Exception):
            return None

    @classmethod
    def _get_scenario_id(cls, scenario_key: str) -> int:
        if not scenario_key:
            return None

        try:
            parsed_key = ScenarioKey(scenario_key)
            scenario = Scenario.find_by(uuid=parsed_key.id)
            return scenario.id if scenario else None
        except (InvalidScenarioKey, Exception):
            return None

    @classmethod
    def _extract_request_key(cls, response) -> str:
        if not response or not hasattr(response, 'headers'):
            return None

        try:
            return response.headers.get('X-Stoobly-Request-Key')
        except (AttributeError, Exception):
            return None

    @classmethod
    def _get_request_id(cls, request_key: str) -> int:
        if not request_key:
            return None

        try:
            parsed_key = RequestKey(request_key)
            request = Request.find_by(uuid=parsed_key.id)
            return request.id if request else None
        except (InvalidRequestKey, Exception):
            return None

    @classmethod
    def __get_file_path(cls) -> str:
        if cls.__file_path is not None:
            return cls.__file_path

        data_dir_path = DataDir.instance().path
        return f"{data_dir_path}/tmp/{cls.__NAMESPACE}/logs/requests.json"

    @classmethod
    def enable_logger_file(cls) -> None:
        cls.__ensure_directory()

        # Enable the logger before setup so error logging works
        cls.__logger.disabled = False

        try:
            # Remove all existing handlers to prevent logging to stdout
            cls.__logger.handlers.clear()
            # Prevent propagation to parent loggers which may have console handlers
            cls.__logger.propagate = False

            file_handler = logging.FileHandler(cls.__get_file_path())
            json_formatter = cls.JSONFormatter(cls.__settings)
            file_handler.setFormatter(json_formatter)
            cls.__logger.addHandler(file_handler)

        except IOError as e:
            cls.__logger.error(f"Failed to configure logger file output: {e}")

    @classmethod
    def __log_scenario_change_delimiter(cls, previous_scenario_key: str, current_scenario_key: str) -> None:
        cls.__ensure_directory()

        previous_name = cls._get_scenario_name(previous_scenario_key)
        current_name = cls._get_scenario_name(current_scenario_key)

        extra = {
            'delimiter': {
                "type": "----- Scenario change delimiter -----",
                "previous_scenario_key": previous_scenario_key or "",
                "previous_scenario_name": previous_name or "",
                "current_scenario_key": current_scenario_key or "",
                "current_scenario_name": current_name or "",
            }
        }

        cls.__logger.info(f"Scenario changed to {current_name or ''}", extra=extra)

    @classmethod
    def __setup_logging(cls, request: 'MitmproxyRequest' = None, response: 'Response' = None, request_key: str = None, fixture_path: str = None) -> dict:
        cls.__ensure_directory()
        cls.__check_scenario_key_changes()
        extra = {}

        if request is not None:
            extra['request'] = request
        if response is not None:
            extra['response'] = response
        if request_key is not None:
            extra['request_key'] = request_key
        if fixture_path is not None:
            extra['fixture_path'] = fixture_path

        return extra

    @classmethod
    def __check_scenario_key_changes(cls) -> None:
        intercept_settings = InterceptSettings(cls.__settings)
        current_scenario_key = intercept_settings.scenario_key

        if cls.__previous_scenario_key != current_scenario_key:
            cls.__log_scenario_change_delimiter(cls.__previous_scenario_key, current_scenario_key)
            cls.__previous_scenario_key = current_scenario_key

    @classmethod
    def debug(cls, message: str, *, request: 'MitmproxyRequest' = None, response: 'Response' = None, request_key: str = None, fixture_path: str = None) -> None:
        extra = cls.__setup_logging(request, response, request_key, fixture_path)
        cls.__logger.debug(message, extra=extra if extra else None)

    @classmethod
    def info(cls, message: str, *, request: 'MitmproxyRequest' = None, response: 'Response' = None, request_key: str = None, fixture_path: str = None) -> None:
        extra = cls.__setup_logging(request, response, request_key, fixture_path)
        cls.__logger.info(message, extra=extra if extra else None)

    @classmethod
    def warning(cls, message: str, *, request: 'MitmproxyRequest' = None, response: 'Response' = None, request_key: str = None, fixture_path: str = None) -> None:
        extra = cls.__setup_logging(request, response, request_key, fixture_path)
        cls.__logger.warning(message, extra=extra if extra else None)

    @classmethod
    def error(cls, message: str, *, request: 'MitmproxyRequest' = None, response: 'Response' = None, request_key: str = None, fixture_path: str = None) -> None:
        extra = cls.__setup_logging(request, response, request_key, fixture_path)
        cls.__logger.error(message, extra=extra if extra else None)

    @classmethod
    def dump_logs(cls):
        file_path = cls.__get_file_path()
        if not os.path.exists(file_path):
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    print(content)
                else:
                    print(end='')
        except IOError as e:
            cls.__logger.error(f"Failed to read log file: {e}")
            print(f"Failed to read log file: {e}")

    @classmethod
    def truncate(cls) -> None:
        cls.__ensure_directory()

        file_path = cls.__get_file_path()

        if not os.path.exists(file_path):
            cls.enable_logger_file()
            return

        try:
            # Close and remove existing handler to release the file lock
            for handler in cls.__logger.handlers[:]:
                if isinstance(handler, logging.FileHandler):
                    handler.close()
                    cls.__logger.removeHandler(handler)

            # Now truncate the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('')

            # Re-enable logging with a fresh handler
            cls.enable_logger_file()
            cls.__logger.debug(f"Cleared log file: {file_path}")

            cls.reset_scenario_key()
        except IOError as e:
            cls.__logger.error(f"Failed to clear log file: {e}")

    @classmethod
    def __ensure_directory(cls):
        file_path = cls.__get_file_path()
        directory = os.path.dirname(file_path)

        if directory and not os.path.exists(directory):
            try:
                cls.__logger.debug(f"created missing directory: {directory}")
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                cls.__logger.error(f"Failed to create log directory: {e}")
