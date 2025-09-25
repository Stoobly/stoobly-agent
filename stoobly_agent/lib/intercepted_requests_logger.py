
import os
import pdb
import logging
import json
from datetime import datetime
from typing import Final

from mitmproxy.http import Request as MitmproxyRequest
from requests import Response
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
    __LOG_ID: Final[str] = "INTERCEPTED_REQUESTS_LOGGER"
    __logger: Logger = Logger.instance(__LOG_ID)

    __settings: Settings = Settings.instance()
    __NAMESPACE: str = os.environ.get(WORKFLOW_NAMESPACE_ENV, __settings.proxy.intercept.mode)
    __file_path: str = None
    __previous_scenario_key: str = None

    class JSONFormatter(logging.Formatter):
        def __init__(self, outer_cls):
            super().__init__()
            self.outer_cls = outer_cls

        def format(self, record: logging.LogRecord) -> str:
            log_entry = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "message": record.getMessage()
            }

            # Extract fields from request
            if hasattr(record, 'request') and record.request is not None:
                request: MitmproxyRequest = record.request
                log_entry.update({
                    "method": request.method,
                    "url": request.pretty_url,
                })

            # Extract fields from response
            if hasattr(record, 'response') and record.response is not None:
                response = record.response
                log_entry.update({
                    "status_code": response.status_code,
                })

            # Set scenario key
            intercept_settings = InterceptSettings(self.outer_cls._InterceptedRequestsLogger__settings)
            scenario_key = intercept_settings.scenario_key
            log_entry.update({
                "scenario_key": scenario_key
            })

            # Set scenario name if scenario_key is set
            scenario_name = ""
            if scenario_key:
                scenario_name = self.outer_cls._get_scenario_name(scenario_key)
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

            # Set scenario UI URL if scenario_key has a value
            stoobly_ui_scenario_url = ""
            if scenario_key:
                scenario_id = self.outer_cls._get_scenario_id(scenario_key)
                if scenario_id:
                    base_url = self.outer_cls._InterceptedRequestsLogger__settings.ui.url
                    if not base_url or base_url == 'http://local.stoobly.com:4200':
                        base_url = 'http://localhost:4200'
                    stoobly_ui_scenario_url = f"{base_url}/agent/scenarios/{scenario_id}"
                log_entry.update({
                    "stoobly_ui_scenario_url": stoobly_ui_scenario_url
                })

            # Set request key and UI URL - prioritize passed-in value, fallback to response headers
            stoobly_ui_request_url = ""
            request_key = None

            # Check for passed-in request_key first
            if hasattr(record, 'request_key') and record.request_key is not None:
                request_key = record.request_key
            # Fallback to extracting from response headers
            elif hasattr(record, 'response') and record.response is not None:
                request_key = self.outer_cls._extract_request_key(record.response)

            if request_key:
                log_entry.update({
                    "request_key": request_key
                })

                request_id = self.outer_cls._get_request_id(request_key)
                if request_id:
                    base_url = self.outer_cls._InterceptedRequestsLogger__settings.ui.url
                    if not base_url or base_url == 'http://local.stoobly.com:4200':
                        base_url = 'http://localhost:4200'
                    stoobly_ui_request_url = f"{base_url}/agent/requests/{request_id}"

                    log_entry.update({
                        "stoobly_ui_request_url": stoobly_ui_request_url
                    })

            # Set fixture path if provided
            if hasattr(record, 'fixture_path') and record.fixture_path is not None:
                log_entry.update({
                    "fixture_path": record.fixture_path
                })

            # Set test name if available in request headers
            if hasattr(record, 'request') and record.request is not None:
                request: MitmproxyRequest = record.request
                if hasattr(request, 'headers') and request.headers:
                    test_name = request.headers.get(custom_headers.TEST_NAME, "")
                    if test_name:
                        log_entry.update({
                            "test_name": test_name
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

        try:
            # Remove all existing handlers to prevent logging to stdout
            cls.__logger.handlers.clear()
            # Prevent propagation to parent loggers which may have console handlers
            cls.__logger.propagate = False

            file_handler = logging.FileHandler(cls.__get_file_path())
            json_formatter = cls.JSONFormatter(cls)
            file_handler.setFormatter(json_formatter)
            cls.__logger.addHandler(file_handler)

        except IOError as e:
            cls.__logger.error(f"Failed to configure logger file output: {e}")

    @classmethod
    def __log_delimiter(cls, previous_scenario_key: str, current_scenario_key: str) -> None:
        cls.__ensure_directory()

        previous_name = cls._get_scenario_name(previous_scenario_key)
        current_name = cls._get_scenario_name(current_scenario_key)

        delimiter_entry = {
            "type": "----- Scenario change delimiter -----",
            "timestamp": datetime.now().isoformat(),
            "message": "Scenario changed",
            "previous_scenario_key": previous_scenario_key or "",
            "previous_scenario_name": previous_name or "",
            "current_scenario_key": current_scenario_key or "",
            "current_scenario_name": current_name or "",
        }

        file_path = cls.__get_file_path()
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(delimiter_entry) + '\n')
        except IOError as e:
            cls.__logger.error(f"Failed to write delimiter to log file: {e}")

    @classmethod
    def __setup_logging(cls, request: MitmproxyRequest = None, response: Response = None, request_key: str = None, fixture_path: str = None) -> dict:
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
            cls.__log_delimiter(cls.__previous_scenario_key, current_scenario_key)
            cls.__previous_scenario_key = current_scenario_key

    @classmethod
    def debug(cls, message: str, *, request: MitmproxyRequest = None, response: Response = None, request_key: str = None, fixture_path: str = None) -> None:
        extra = cls.__setup_logging(request, response, request_key, fixture_path)
        cls.__logger.debug(message, extra=extra if extra else None)

    @classmethod
    def info(cls, message: str, *, request: MitmproxyRequest = None, response: Response = None, request_key: str = None, fixture_path: str = None) -> None:
        extra = cls.__setup_logging(request, response, request_key, fixture_path)
        cls.__logger.info(message, extra=extra if extra else None)

    @classmethod
    def warning(cls, message: str, *, request: MitmproxyRequest = None, response: Response = None, request_key: str = None, fixture_path: str = None) -> None:
        extra = cls.__setup_logging(request, response, request_key, fixture_path)
        cls.__logger.warning(message, extra=extra if extra else None)

    @classmethod
    def error(cls, message: str, *, request: MitmproxyRequest = None, response: Response = None, request_key: str = None, fixture_path: str = None) -> None:
        extra = cls.__setup_logging(request, response, request_key, fixture_path)
        cls.__logger.error(message, extra=extra if extra else None)

    @classmethod
    def dump_logs(cls):
        file_path = cls.__get_file_path()
        if not os.path.exists(file_path):
            cls.__logger.error(f"Log file not found at: {file_path}")
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
        file_path = cls.__get_file_path()

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('')
            cls.__logger.info(f"Cleared log file: {file_path}")

            cls.reset_scenario_key()
        except IOError as e:
            cls.__logger.error(f"Failed to clear log file: {e}")

    @classmethod
    def __ensure_directory(cls):
        file_path = cls.__get_file_path()
        directory = os.path.dirname(file_path)

        if directory and not os.path.exists(directory):
            try:
                Logger.instance(cls.__LOG_ID).info(f"created missing directory: {file_path}")
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                cls.__logger.error(f"Failed to create log directory: {e}")
