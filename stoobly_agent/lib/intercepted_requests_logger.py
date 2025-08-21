
import os
import pdb
import logging
import json
from datetime import datetime
from typing import Final

from mitmproxy.http import Request as MitmproxyRequest
from requests import Response
from stoobly_agent.app.cli.scaffold.constants import NAMESPACE_NAME_ENV, SERVICE_NAME_ENV
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.proxy.constants import custom_response_codes
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey, InvalidScenarioKey
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.lib.logger import Logger


class JSONFormatter(logging.Formatter):
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

        settings = Settings.instance()
        intercept_settings = InterceptSettings(settings)
        scenario_key = intercept_settings.scenario_key
        log_entry.update({
            "scenario_key": scenario_key
        })

        env_var_service_name = os.environ.get(SERVICE_NAME_ENV)
        if env_var_service_name:
            log_entry.update({
                "service_name": env_var_service_name
            })
        env_var_namespace_name = os.environ.get(NAMESPACE_NAME_ENV)
        if env_var_namespace_name:
            log_entry.update({
                "namespace": env_var_namespace_name
            })

        # TODO: link to agent URL

        return json.dumps(log_entry)


class InterceptedRequestsLogger():
    __LOG_ID: Final[str] = "INTERCEPTED_REQUESTS_LOGGER"
    __logger: Logger = Logger.instance(__LOG_ID)

    __settings: Settings = Settings.instance()
    __NAMESPACE: str = __settings.proxy.intercept.mode
    __file_path: str = None
    __previous_scenario_key: str = None

    @classmethod
    def set_file_path(cls, file_path: str) -> None:
        cls.__file_path = file_path

    @classmethod
    def reset_scenario_key(cls) -> None:
        cls.__previous_scenario_key = None

    @classmethod
    def set_log_level(cls, log_level: str) -> None:
        cls.__logger.setLevel(log_level)

    @classmethod
    def __get_scenario_name(cls, scenario_key: str) -> str:
        if not scenario_key:
            return None

        try:
            parsed_key = ScenarioKey(scenario_key)
            scenario = Scenario.find_by(uuid=parsed_key.id)
            return scenario.name if scenario else None
        except (InvalidScenarioKey, Exception):
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
            json_formatter = JSONFormatter()
            file_handler.setFormatter(json_formatter)
            cls.__logger.addHandler(file_handler)

        except IOError as e:
            cls.__logger.error(f"Failed to configure logger file output: {e}")

    @classmethod
    def __log_delimiter(cls, previous_scenario_key: str, current_scenario_key: str) -> None:
        cls.__ensure_directory()

        previous_name = cls.__get_scenario_name(previous_scenario_key)
        current_name = cls.__get_scenario_name(current_scenario_key)

        delimiter_entry = {
            "type": "----- Scenario change delimiter -----",
            "timestamp": datetime.now().isoformat(),
            "previous_scenario_key": previous_scenario_key,
            "previous_scenario_name": previous_name,
            "current_scenario_key": current_scenario_key,
            "current_scenario_name": current_name,
            "message": "Scenario changed",
        }

        file_path = cls.__get_file_path()
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(delimiter_entry) + '\n')
        except IOError as e:
            cls.__logger.error(f"Failed to write delimiter to log file: {e}")

    @classmethod
    def __setup_logging(cls, request: MitmproxyRequest = None, response: Response = None) -> dict:
        cls.__ensure_directory()
        cls.__check_scenario_key_changes()
        extra = {}
        if request:
            extra['request'] = request
        if response:
            extra['response'] = response
        return extra

    @classmethod
    def __check_scenario_key_changes(cls) -> None:
        settings = Settings.instance()
        intercept_settings = InterceptSettings(settings)
        current_scenario_key = intercept_settings.scenario_key

        if cls.__previous_scenario_key != current_scenario_key:
            cls.__log_delimiter(cls.__previous_scenario_key, current_scenario_key)
            cls.__previous_scenario_key = current_scenario_key

    @classmethod
    def debug(cls, message: str, request: MitmproxyRequest = None, response: Response = None) -> None:
        extra = cls.__setup_logging(request, response)
        cls.__logger.debug(message, extra=extra if extra else None)

    @classmethod
    def info(cls, message: str, request: MitmproxyRequest = None, response: Response = None) -> None:
        extra = cls.__setup_logging(request, response)
        cls.__logger.info(message, extra=extra if extra else None)

    @classmethod
    def warning(cls, message: str, request: MitmproxyRequest = None, response: Response = None) -> None:
        extra = cls.__setup_logging(request, response)
        cls.__logger.warning(message, extra=extra if extra else None)

    @classmethod
    def error(cls, message: str, request: MitmproxyRequest = None, response: Response = None) -> None:
        extra = cls.__setup_logging(request, response)
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
