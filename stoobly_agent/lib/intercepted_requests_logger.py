
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

    @classmethod
    def set_file_path(cls, file_path: str) -> None:
        cls.__file_path = file_path

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
    def log_error(cls, request: MitmproxyRequest, response: Response) -> None:
        cls.__ensure_directory()

        response_code = response.status_code

        generic_message = "Log for intercepted request"
        message = generic_message

        if response_code == custom_response_codes.NOT_FOUND:
            message += " 499 Mock Not Found"

        # Create log record with request and response data
        cls.__logger.error(message, extra={'request': request, 'response': response})

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
    def clear(cls) -> None:
        file_path = cls.__get_file_path()

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('')
            cls.__logger.info(f"Cleared log file: {file_path}")
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
