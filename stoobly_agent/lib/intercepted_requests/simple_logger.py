
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests.logger import InterceptedRequestsLogger


class SimpleInterceptedRequestsLogger(InterceptedRequestsLogger):
    """Non-scaffold request logger. File path: {dir_path}/tmp/logs/requests.json"""

    @classmethod
    def _get_file_path(cls, data_dir_path: str = None, workflow: str = None, namespace: str = None, workflow_namespace=None) -> str:
        """Return the simple (non-scaffold) log file path."""
        base = InterceptedRequestsLogger
        # Use cached path when set (explicit override via set_file_path)
        if base._file_path is not None:
            return base._file_path

        if data_dir_path:
            dir_path = DataDir.instance(data_dir_path).path
        else:
            dir_path = DataDir.instance().path
        return f"{dir_path}/tmp/logs/requests.json"

    @classmethod
    def _get_log_path_message(cls, data_dir_path: str = None, workflow: str = None, namespace: str = None) -> str:
        """Return the print message for the simple log file path."""
        file_path = cls._get_file_path(data_dir_path=data_dir_path)
        return f"Requests log path: {file_path}"
