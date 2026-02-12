
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests.logger import InterceptedRequestsLogger


class ScaffoldInterceptedRequestsLogger(InterceptedRequestsLogger):
    """Scaffold request logger"""

    @classmethod
    def _get_file_path(cls, workflow: str = None, namespace: str = None, data_dir_path: str = None, **kwargs) -> str:
        """Return the scaffold log file path."""
        base = InterceptedRequestsLogger
        # Only use cache when no specific workflow/namespace is requested
        if (base._file_path is not None) and (workflow is None) and (namespace is None):
            return base._file_path

        if data_dir_path:
            dir_path = DataDir.instance(data_dir_path).path
        else:
            dir_path = DataDir.instance().path

        wf = cls._sanitize_path_component(workflow if workflow else cls._get_workflow()) or cls._get_workflow()
        # If namespace not provided, default to workflow (if provided) before falling back to env/settings
        ns = cls._sanitize_path_component(namespace if namespace else (workflow or cls._get_namespace())) or wf
        return f"{dir_path}/tmp/{wf}/{ns}/logs/requests-{wf}.json"

    @classmethod
    def _get_log_path_message(cls, workflow: str = None, namespace: str = None, **kwargs) -> str:
        """Return the print message for the scaffold log file path."""
        file_path = cls._get_file_path(workflow=workflow, namespace=namespace, **kwargs)
        return f"Requests log path for workflow: {workflow}, namespace: {namespace}\nFile path: {file_path}"
