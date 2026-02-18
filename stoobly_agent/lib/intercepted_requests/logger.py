
import os
import logging
import logging.handlers
import queue
import atexit
import re
from typing import TYPE_CHECKING, Final, Optional

if TYPE_CHECKING:
    from requests import Response
    from mitmproxy.http import Request as MitmproxyRequest
    from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace

from stoobly_agent.app.cli.helpers.print_service import JSON_FORMAT, SIMPLE_FORMAT
from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_NAME_ENV, WORKFLOW_NAMESPACE_ENV
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey, InvalidScenarioKey
from stoobly_agent.lib.api.keys.request_key import RequestKey, InvalidRequestKey
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.logger import DEBUG, ERROR, INFO, WARNING, Logger
from stoobly_agent.lib.intercepted_requests.json_formatter import JSONFormatter


class InterceptedRequestsLogger():
    """Base class for intercepted request logging.

    Subclasses must implement _get_file_path() and _get_log_path_message().
    Use SimpleInterceptedRequestsLogger for non-scaffold logging,
    or ScaffoldInterceptedRequestsLogger for scaffold-based logging.
    """

    _LOG_ID: Final[str] = "InterceptedRequestsLogger"
    _logger: Logger = Logger.instance(_LOG_ID)

    # Log level mappings for conversion between string and numeric levels
    _STR_TO_LEVEL: Final[dict] = {
        DEBUG: logging.DEBUG,
        INFO: logging.INFO,
        WARNING: logging.WARNING,
        ERROR: logging.ERROR,
    }
    _LEVEL_TO_STR: Final[dict] = {v: k for k, v in _STR_TO_LEVEL.items()}

    _SUBSTRING_MATCH_FIELDS: Final[set] = {'url', 'user_agent', 'message', 'scenario_name', 'test_title', 'service_name'}

    _settings: Settings = Settings.instance()
    _file_path: str = None
    _previous_scenario_key: str = None

    # Feature flag: Set to True to enable async queue-based logging
    _USE_ASYNC_QUEUE: bool = True

    # Async logging components
    _queue_listener: Optional[logging.handlers.QueueListener] = None
    _log_queue: Optional[queue.Queue] = None
    _file_handler: Optional[logging.FileHandler] = None
    _atexit_registered: bool = False

    # Initialize logger as disabled by default
    _logger.disabled = True

    @classmethod
    def _get_file_path(cls, data_dir_path: str = None, workflow: str = None, namespace: str = None, workflow_namespace: 'WorkflowNamespace' = None) -> str:
        """Return the log file path. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement _get_file_path")

    @classmethod
    def _get_log_path_message(cls, data_dir_path: str = None, workflow: str = None, namespace: str = None) -> str:
        """Return the print message for get_log_file_path. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement _get_log_path_message")

    @staticmethod
    def _sanitize_path_component(value: str) -> str:
        """Remove path traversal sequences and invalid characters to prevent path traversal attacks."""
        if value is None:
            return None
        # Remove null bytes, path separators, URL-encoded separators, and traversal sequences
        sanitized = re.sub(r'\x00|[/\\]|%2[Ff]|%5[Cc]|\.\.', '', value)
        return sanitized if sanitized else None

    @staticmethod
    def _get_workflow() -> str:
        """Get the workflow name from env var or settings."""
        return os.environ.get(WORKFLOW_NAME_ENV) or InterceptedRequestsLogger._settings.proxy.intercept.mode

    @staticmethod
    def _get_namespace() -> str:
        """Get the namespace from env var, falling back to workflow."""
        return os.environ.get(WORKFLOW_NAMESPACE_ENV) or InterceptedRequestsLogger._get_workflow()

    @classmethod
    def _cleanup_handlers(cls) -> None:
        """Stop queue listener and close handlers."""
        base = InterceptedRequestsLogger
        # Stop the queue listener (flushes remaining records)
        if base._queue_listener is not None:
            base._queue_listener.stop()
            base._queue_listener = None

        # Close file handler
        if base._file_handler is not None:
            base._file_handler.close()
            base._file_handler = None

        # Clear queue reference
        base._log_queue = None

    @classmethod
    def shutdown(cls) -> None:
        """Public method to shutdown logger gracefully."""
        base = InterceptedRequestsLogger
        cls._cleanup_handlers()
        base._logger.handlers.clear()

    @classmethod
    def flush(cls) -> None:
        """Flush pending log messages to disk without stopping the listener."""
        base = InterceptedRequestsLogger
        if base._USE_ASYNC_QUEUE and base._log_queue is not None:
            # Wait for the queue to be empty (all messages processed)
            base._log_queue.join()

        # Flush the file handler buffer to disk
        if base._file_handler is not None:
            base._file_handler.flush()

    @classmethod
    def set_file_path(cls, file_path: str) -> None:
        """Set a cached file path (used by scaffold mode)."""
        InterceptedRequestsLogger._file_path = file_path

    @classmethod
    def reset_scenario_key(cls) -> None:
        """Reset the previous scenario key tracker."""
        InterceptedRequestsLogger._previous_scenario_key = None

    @classmethod
    def set_log_level(cls, log_level: str) -> None:
        """Set the log level for the logger."""
        base = InterceptedRequestsLogger
        numeric_level = base._STR_TO_LEVEL.get(log_level.lower())
        if numeric_level is None:
            raise ValueError(f"Invalid log level: {log_level}. Must be one of: {', '.join(base._STR_TO_LEVEL.keys())}")
        base._logger.setLevel(numeric_level)

    @classmethod
    def get_log_level(cls) -> str:
        """Get the current log level as a string."""
        base = InterceptedRequestsLogger
        return base._LEVEL_TO_STR.get(base._logger.level, INFO)

    @classmethod
    def _get_scenario_name(cls, scenario_key: str) -> str:
        """Look up scenario name from a scenario key."""
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
        """Look up scenario ID from a scenario key."""
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
        """Extract request key from response headers."""
        if not response or not hasattr(response, 'headers'):
            return None

        try:
            return response.headers.get('X-Stoobly-Request-Key')
        except AttributeError:
            return None

    @classmethod
    def _get_request_id(cls, request_key: str) -> int:
        """Look up request ID from a request key."""
        if not request_key:
            return None

        try:
            parsed_key = RequestKey(request_key)
            request = Request.find_by(uuid=parsed_key.id)
            return request.id if request else None
        except InvalidRequestKey:
            return None

    @classmethod
    def _entry_matches_filters(cls, entry: dict, filters: dict) -> bool:
        """Check if a log entry matches all provided filters.

        Args:
            entry: Parsed JSON log entry dict.
            filters: Dict of field_name -> expected_value.

        Returns:
            True if the entry matches all filters, False otherwise.
        """
        base = InterceptedRequestsLogger
        for key, expected_value in filters.items():
            actual_value = entry.get(key)

            if actual_value is None:
                return False

            if key in base._SUBSTRING_MATCH_FIELDS:
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
                    base._logger.warning(
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

    # --- Template methods (shared logic, delegate to cls._get_file_path) ---

    @classmethod
    def enable_logger_file(cls, data_dir_path: str = None, workflow: str = None, namespace: str = None, workflow_namespace: 'WorkflowNamespace' = None) -> None:
        """Enable file-based logging. Subclass determines the file path."""
        base = InterceptedRequestsLogger
        cls._ensure_directory(data_dir_path=data_dir_path, workflow=workflow, namespace=namespace, workflow_namespace=workflow_namespace)

        # Enable the logger before setup so error logging works
        base._logger.disabled = False

        try:
            # Clean up existing handlers/listeners
            cls._cleanup_handlers()

            # Create file handler
            base._file_handler = logging.FileHandler(
                cls._get_file_path(data_dir_path=data_dir_path, workflow=workflow, namespace=namespace, workflow_namespace=workflow_namespace)
            )
            base._file_handler.setLevel(logging.DEBUG)
            json_formatter = JSONFormatter(
                base._settings,
                get_scenario_name=cls._get_scenario_name,
                extract_request_key=cls._extract_request_key,
            )
            base._file_handler.setFormatter(json_formatter)

            # Remove all existing handlers to prevent logging to stdout
            base._logger.handlers.clear()
            # Prevent propagation to parent loggers which may have console handlers
            base._logger.propagate = False

            if base._USE_ASYNC_QUEUE:
                # Async queue-based logging
                base._log_queue = queue.Queue()
                base._queue_listener = logging.handlers.QueueListener(
                    base._log_queue,
                    base._file_handler,
                    respect_handler_level=True
                )
                base._queue_listener.start()

                # Register cleanup on program exit to flush remaining logs (only once)
                if not base._atexit_registered:
                    atexit.register(base.shutdown)
                    base._atexit_registered = True

                queue_handler = logging.handlers.QueueHandler(base._log_queue)
                base._logger.addHandler(queue_handler)
            else:
                # Synchronous direct logging
                base._logger.addHandler(base._file_handler)

        except OSError as e:
            base._logger.error(f"Failed to configure logger file output: {e}")

    @classmethod
    def get_log_file_path(cls, data_dir_path: str = None, workflow: str = None, namespace: str = None, workflow_namespace: 'WorkflowNamespace' = None) -> str:
        """Get the log file path and print it."""
        file_path = cls._get_file_path(data_dir_path=data_dir_path, workflow=workflow, namespace=namespace, workflow_namespace=workflow_namespace)

        print(cls._get_log_path_message(data_dir_path=data_dir_path, workflow=workflow, namespace=namespace))

        if not os.path.exists(file_path):
            return

        return file_path

    @classmethod
    def dump_logs(cls, data_dir_path: str = None, filters: dict = None, output_format: str = None, select: list = None, without_headers: bool = False, workflow: str = None, namespace: str = None, workflow_namespace: 'WorkflowNamespace' = None):
        """Dump log entries to stdout, optionally filtering by field values and selecting columns.

        Args:
            data_dir_path: Optional path to the data directory. If None, uses default or cached path.
            filters: Optional dict of field_name -> value pairs for filtering entries.
            output_format: Output format ('json' or 'simple'). If None and select is provided, defaults to 'simple'.
            select: Optional list of field names to display. If empty, all fields shown.
            without_headers: If True, don't print column headers (for table format only).
            workflow: Workflow name for scaffold-based logging.
            namespace: Workflow namespace for scaffold-based logging.
            workflow_namespace: WorkflowNamespace object for scaffold-based logging.
        """
        base = InterceptedRequestsLogger
        file_path = cls._get_file_path(data_dir_path=data_dir_path, workflow=workflow, namespace=namespace, workflow_namespace=workflow_namespace)
        if not os.path.exists(file_path):
            return

        select = select or []

        needs_formatting = output_format or len(select) > 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import json
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
            base._logger.error(f"Failed to read log file: {e}")
            print(f"Failed to read log file: {e}")

    @classmethod
    def truncate(cls, data_dir_path: str = None, workflow: str = None, namespace: str = None, workflow_namespace: 'WorkflowNamespace' = None) -> None:
        """Truncate (clear) the log file and re-enable logging."""
        base = InterceptedRequestsLogger
        cls._ensure_directory(data_dir_path=data_dir_path, workflow=workflow, namespace=namespace, workflow_namespace=workflow_namespace)

        file_path = cls._get_file_path(data_dir_path=data_dir_path, workflow=workflow, namespace=namespace, workflow_namespace=workflow_namespace)

        if not os.path.exists(file_path):
            cls.enable_logger_file(data_dir_path=data_dir_path, workflow=workflow, namespace=namespace, workflow_namespace=workflow_namespace)
            return

        try:
            # Stop queue listener and close file handler to release the file lock
            cls._cleanup_handlers()

            # Close and remove existing handlers (backward compatibility)
            for handler in base._logger.handlers[:]:
                if isinstance(handler, logging.FileHandler):
                    handler.close()
                    base._logger.removeHandler(handler)

            # Clear all handlers
            base._logger.handlers.clear()

            # Now truncate the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('')

            # Re-enable logging with fresh handlers
            cls.enable_logger_file(data_dir_path=data_dir_path, workflow=workflow, namespace=namespace, workflow_namespace=workflow_namespace)

            base._logger.debug(f"Cleared log file: {file_path}")

            cls.reset_scenario_key()
        except IOError as e:
            base._logger.error(f"Failed to clear log file: {e}")

    @classmethod
    def _ensure_directory(cls, data_dir_path: str = None, workflow: str = None, namespace: str = None, workflow_namespace: 'WorkflowNamespace' = None) -> None:
        """Ensure the log file directory exists."""
        file_path = cls._get_file_path(data_dir_path=data_dir_path, workflow=workflow, namespace=namespace, workflow_namespace=workflow_namespace)
        directory = os.path.dirname(file_path)

        if directory and not os.path.exists(directory):
            try:
                InterceptedRequestsLogger._logger.debug(f"created missing directory: {directory}")
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                InterceptedRequestsLogger._logger.error(f"Failed to create log directory: {e}")

    # --- Logging methods (called by proxy handlers on the base class) ---

    @classmethod
    def _log_scenario_change_delimiter(cls, previous_scenario_key: str, current_scenario_key: str) -> None:
        """Log a delimiter entry when the scenario changes."""
        base = InterceptedRequestsLogger
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

        base._logger.info(f"Scenario changed to {current_name or ''}", extra=extra)

    @classmethod
    def _setup_logging(cls, request: 'MitmproxyRequest' = None, response: 'Response' = None, request_key: str = None, fixture_path: str = None) -> dict:
        """Prepare extra fields for a log entry and check for scenario changes."""
        cls._check_scenario_key_changes()
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
    def _check_scenario_key_changes(cls) -> None:
        """Check if the scenario key has changed and log a delimiter if so."""
        base = InterceptedRequestsLogger
        intercept_settings = InterceptSettings(base._settings)
        current_scenario_key = intercept_settings.scenario_key

        if base._previous_scenario_key != current_scenario_key:
            cls._log_scenario_change_delimiter(base._previous_scenario_key, current_scenario_key)
            base._previous_scenario_key = current_scenario_key

    @classmethod
    def debug(cls, message: str, *, request: 'MitmproxyRequest' = None, response: 'Response' = None, request_key: str = None, fixture_path: str = None) -> None:
        """Log a debug message."""
        extra = cls._setup_logging(request, response, request_key, fixture_path)
        InterceptedRequestsLogger._logger.debug(message, extra=extra if extra else None)

    @classmethod
    def info(cls, message: str, *, request: 'MitmproxyRequest' = None, response: 'Response' = None, request_key: str = None, fixture_path: str = None) -> None:
        """Log an info message."""
        extra = cls._setup_logging(request, response, request_key, fixture_path)
        InterceptedRequestsLogger._logger.info(message, extra=extra if extra else None)

    @classmethod
    def warning(cls, message: str, *, request: 'MitmproxyRequest' = None, response: 'Response' = None, request_key: str = None, fixture_path: str = None) -> None:
        """Log a warning message."""
        extra = cls._setup_logging(request, response, request_key, fixture_path)
        InterceptedRequestsLogger._logger.warning(message, extra=extra if extra else None)

    @classmethod
    def error(cls, message: str, *, request: 'MitmproxyRequest' = None, response: 'Response' = None, request_key: str = None, fixture_path: str = None) -> None:
        """Log an error message."""
        extra = cls._setup_logging(request, response, request_key, fixture_path)
        InterceptedRequestsLogger._logger.error(message, extra=extra if extra else None)
