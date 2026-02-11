
import os
import logging
import logging.handlers
import json
import queue
import atexit
from datetime import datetime
from typing import TYPE_CHECKING, Final, Optional

if TYPE_CHECKING:
    from requests import Response
    from mitmproxy.http import Request as MitmproxyRequest, Response as MitmproxyResponse

from stoobly_agent.app.cli.helpers.print_service import JSON_FORMAT, SIMPLE_FORMAT
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

    # Log level mappings for conversion between string and numeric levels
    __STR_TO_LEVEL: Final[dict] = {
        DEBUG: logging.DEBUG,
        INFO: logging.INFO,
        WARNING: logging.WARNING,
        ERROR: logging.ERROR,
    }
    __LEVEL_TO_STR: Final[dict] = {v: k for k, v in __STR_TO_LEVEL.items()}

    __SUBSTRING_MATCH_FIELDS: Final[set] = {'url', 'user_agent', 'message', 'scenario_name', 'test_title', 'service_name'}

    __settings: Settings = Settings.instance()
    __file_path: str = None
    __previous_scenario_key: str = None


    # Feature flag: Set to True to enable async queue-based logging
    __USE_ASYNC_QUEUE: bool = True

    # Async logging components
    __queue_listener: Optional[logging.handlers.QueueListener] = None
    __log_queue: Optional[queue.Queue] = None
    __file_handler: Optional[logging.FileHandler] = None
    __atexit_registered: bool = False

    @staticmethod
    def _get_namespace() -> str:
        # Imported lazily to avoid circular import
        from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_NAMESPACE_ENV
        return os.environ.get(WORKFLOW_NAMESPACE_ENV, InterceptedRequestsLogger.__settings.proxy.intercept.mode)

    # Initialize logger as disabled by default
    __logger.disabled = True

    @classmethod
    def __cleanup_handlers(cls) -> None:
        """Stop queue listener and close handlers"""
        # Stop the queue listener (flushes remaining records)
        if cls.__queue_listener is not None:
            cls.__queue_listener.stop()
            cls.__queue_listener = None

        # Close file handler
        if cls.__file_handler is not None:
            cls.__file_handler.close()
            cls.__file_handler = None

        # Clear queue reference
        cls.__log_queue = None

    @classmethod
    def shutdown(cls) -> None:
        """Public method to shutdown logger gracefully"""
        cls.__cleanup_handlers()
        cls.__logger.handlers.clear()

    @classmethod
    def flush(cls) -> None:
        """Flush pending log messages to disk without stopping the listener."""
        if cls.__USE_ASYNC_QUEUE and cls.__log_queue is not None:
            # Wait for the queue to be empty (all messages processed)
            # QueueListener calls task_done() after handling each record (since Python 3.7+)
            cls.__log_queue.join()

        # Flush the file handler buffer to disk
        if cls.__file_handler is not None:
            cls.__file_handler.flush()

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
            intercept_settings = InterceptSettings(self.__settings, request=request)
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
        numeric_level = cls.__STR_TO_LEVEL.get(log_level.lower())
        if numeric_level is None:
            raise ValueError(f"Invalid log level: {log_level}. Must be one of: {', '.join(cls.__STR_TO_LEVEL.keys())}")
        cls.__logger.setLevel(numeric_level)

    @classmethod
    def get_log_level(cls) -> str:
        return cls.__LEVEL_TO_STR.get(cls.__logger.level, INFO)

    @classmethod
    def _get_scenario_name(cls, scenario_key: str) -> str:
        if not scenario_key:
            return None

        try:
            parsed_key = ScenarioKey(scenario_key)
            scenario = Scenario.find_by(uuid=parsed_key.id)
            return scenario.name if scenario else None
        except InvalidScenarioKey:
            return None

    @classmethod
    def _get_scenario_id(cls, scenario_key: str) -> int:
        if not scenario_key:
            return None

        try:
            parsed_key = ScenarioKey(scenario_key)
            scenario = Scenario.find_by(uuid=parsed_key.id)
            return scenario.id if scenario else None
        except InvalidScenarioKey:
            return None

    @classmethod
    def _extract_request_key(cls, response) -> str:
        if not response or not hasattr(response, 'headers'):
            return None

        try:
            return response.headers.get('X-Stoobly-Request-Key')
        except AttributeError:
            return None

    @classmethod
    def _get_request_id(cls, request_key: str) -> int:
        if not request_key:
            return None

        try:
            parsed_key = RequestKey(request_key)
            request = Request.find_by(uuid=parsed_key.id)
            return request.id if request else None
        except InvalidRequestKey:
            return None

    @classmethod
    def __get_file_path(cls, data_dir_path: str = None) -> str:
        if cls.__file_path is not None:
            return cls.__file_path

        if data_dir_path:
            dir_path = DataDir.instance(data_dir_path).path
        else:
            dir_path = DataDir.instance().path
        namespace = cls._get_namespace()
        return f"{dir_path}/tmp/{namespace}/logs/requests.json"

    @classmethod
    def enable_logger_file(cls, data_dir_path: str = None) -> None:
        cls.__ensure_directory(data_dir_path)

        # Enable the logger before setup so error logging works
        cls.__logger.disabled = False

        try:
            # Clean up existing handlers/listeners
            cls.__cleanup_handlers()

            # Create file handler
            cls.__file_handler = logging.FileHandler(
                cls.__get_file_path(data_dir_path)
            )
            cls.__file_handler.setLevel(logging.DEBUG)
            json_formatter = cls.JSONFormatter(cls.__settings)
            cls.__file_handler.setFormatter(json_formatter)

            # Remove all existing handlers to prevent logging to stdout
            cls.__logger.handlers.clear()
            # Prevent propagation to parent loggers which may have console handlers
            cls.__logger.propagate = False

            if cls.__USE_ASYNC_QUEUE:
                # Async queue-based logging
                cls.__log_queue = queue.Queue()
                cls.__queue_listener = logging.handlers.QueueListener(
                    cls.__log_queue,
                    cls.__file_handler,
                    respect_handler_level=True
                )
                cls.__queue_listener.start()

                # Register cleanup on program exit to flush remaining logs (only once)
                if not cls.__atexit_registered:
                    atexit.register(cls.shutdown)
                    cls.__atexit_registered = True

                queue_handler = logging.handlers.QueueHandler(cls.__log_queue)
                cls.__logger.addHandler(queue_handler)
            else:
                # Synchronous direct logging
                cls.__logger.addHandler(cls.__file_handler)

        except OSError as e:
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
    def _entry_matches_filters(cls, entry: dict, filters: dict) -> bool:
        """Check if a log entry matches all provided filters.

        Args:
            entry: Parsed JSON log entry dict.
            filters: Dict of field_name -> expected_value.

        Returns:
            True if the entry matches all filters, False otherwise.
        """
        for key, expected_value in filters.items():
            actual_value = entry.get(key)

            if actual_value is None:
                return False

            if key in cls.__SUBSTRING_MATCH_FIELDS:
                # Substring matching
                if str(expected_value) not in str(actual_value):
                    return False
            elif key == 'status_code':
                # status_code compares as integer
                try:
                    if int(actual_value) != int(expected_value):
                        return False
                except (ValueError, TypeError) as e:
                    # Skip malformed entries instead of crashing
                    cls.__logger.warning(
                        f"Skipping log entry with malformed status_code: '{actual_value}' "
                        f"(expected integer). Entry timestamp: {entry.get('timestamp', 'unknown')}. Error: {e}"
                    )
                    return False
            elif key == 'level':
                # Case-insensitive comparison for level
                if str(actual_value).upper() != str(expected_value).upper():
                    return False
            else:
                # All other fields use exact string match
                if str(actual_value) != str(expected_value):
                    return False

        return True

    @classmethod
    def dump_logs(cls, data_dir_path: str = None, filters: dict = None, output_format: str = None, select: list = None, without_headers: bool = False):
        """Dump log entries to stdout, optionally filtering by field values and selecting columns.

        Args:
            data_dir_path: Path to the Stoobly data directory.
            filters: Optional dict of field_name -> value pairs for filtering entries.
            output_format: Output format ('json' or 'simple'). If None and select is provided, defaults to 'json'.
            select: Optional list of field names to display. If empty, all fields shown.
            without_headers: If True, don't print column headers (for table format only).
        """

        file_path = cls.__get_file_path(data_dir_path)
        if not os.path.exists(file_path):
            return

        select = select or []

        needs_formatting = output_format or len(select) > 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                entries = []
                for line in f:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    try:
                        entry = json.loads(stripped)
                    except json.JSONDecodeError:
                        continue

                    # Handle delimiter entries
                    is_delimiter = 'type' in entry and 'delimiter' in str(entry.get('type', '')).lower()
                    if is_delimiter:
                        if needs_formatting or filters:
                            continue
                        # No formatting: print inline to preserve ordering
                        print(stripped)
                        continue

                    # Apply filters
                    if filters and not cls._entry_matches_filters(entry, filters):
                        continue

                    if not needs_formatting:
                        # Print inline to preserve ordering with delimiters
                        print(json.dumps(entry))
                        continue

                    entries.append(entry)

                # If no formatting requested, everything was already printed inline
                if not needs_formatting:
                    return

                # Default to table format when select is used but format is not specified
                if select and not output_format:
                    output_format = SIMPLE_FORMAT

                # Apply select if provided
                if select:
                    filtered_entries = []
                    for entry in entries:
                        filtered_entry = {}
                        for key in select:
                            if key in entry:
                                filtered_entry[key] = entry[key]
                        filtered_entries.append(filtered_entry)
                    entries = filtered_entries

                # Print based on format
                if not entries:
                    print(end='')
                    return

                if output_format == JSON_FORMAT:
                    # Print as JSON array
                    print(json.dumps(entries, indent=2))
                else:
                    # Print as table using tabulate
                    from tabulate import tabulate

                    # Build headers and rows
                    headers = []
                    rows = []

                    for entry in entries:
                        if not headers:
                            headers = list(entry.keys())

                        row = [entry.get(h, '') for h in headers]
                        rows.append(row)

                    if without_headers:
                        print(tabulate(rows, tablefmt='plain'))
                    else:
                        print(tabulate(rows, headers=headers, tablefmt='plain'))

        except IOError as e:
            cls.__logger.error(f"Failed to read log file: {e}")
            print(f"Failed to read log file: {e}")

    @classmethod
    def truncate(cls, data_dir_path: str = None) -> None:
        cls.__ensure_directory(data_dir_path)

        file_path = cls.__get_file_path(data_dir_path)

        if not os.path.exists(file_path):
            cls.enable_logger_file(data_dir_path)
            return

        try:
            # Stop queue listener and close file handler to release the file lock
            cls.__cleanup_handlers()

            # Close and remove existing handlers (backward compatibility)
            for handler in cls.__logger.handlers[:]:
                if isinstance(handler, logging.FileHandler):
                    handler.close()
                    cls.__logger.removeHandler(handler)

            # Clear all handlers
            cls.__logger.handlers.clear()

            # Now truncate the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('')

            # Re-enable logging with fresh handlers
            cls.enable_logger_file(data_dir_path)
            cls.__logger.debug(f"Cleared log file: {file_path}")

            cls.reset_scenario_key()
        except IOError as e:
            cls.__logger.error(f"Failed to clear log file: {e}")

    @classmethod
    def __ensure_directory(cls, data_dir_path: str = None):
        file_path = cls.__get_file_path(data_dir_path)
        directory = os.path.dirname(file_path)

        if directory and not os.path.exists(directory):
            try:
                cls.__logger.debug(f"created missing directory: {directory}")
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                cls.__logger.error(f"Failed to create log directory: {e}")
