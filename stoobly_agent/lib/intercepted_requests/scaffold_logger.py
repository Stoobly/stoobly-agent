
from typing import TYPE_CHECKING

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests.logger import InterceptedRequestsLogger

if TYPE_CHECKING:
    from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace


class ScaffoldInterceptedRequestsLogger(InterceptedRequestsLogger):
    """Scaffold request logger"""

    @classmethod
    def _get_file_path(cls, data_dir_path: str = None, workflow: str = None, namespace: str = None, workflow_namespace: 'WorkflowNamespace' = None) -> str:
        """Return the scaffold log file path.

        set_file_path override is used only when no path-affecting args are
        given. Explicit workflow/namespace/data_dir_path/workflow_namespace
        always recomputes. Otherwise fall back to the last enable_logger_file
        path before computing a default.
        """
        base = InterceptedRequestsLogger
        no_path_args = (
            workflow is None
            and namespace is None
            and data_dir_path is None
            and workflow_namespace is None
        )
        if no_path_args and base._file_path is not None:
            return base._file_path
        if no_path_args and base._active_file_path is not None:
            return base._active_file_path

        wf = cls._sanitize_path_component(workflow if workflow else cls._get_workflow()) or cls._get_workflow()

        if workflow_namespace is not None:
            return f"{workflow_namespace.path}/logs/{wf}.requests.json"

        # Fallback. If workflow_namespace not provided, default to workflow (if provided) before falling back to env/settings
        if data_dir_path:
            tmp_dir_path = DataDir.instance(data_dir_path).tmp_dir_path
        else:
            tmp_dir_path = DataDir.instance().tmp_dir_path

        ns = cls._sanitize_path_component(namespace if namespace else (workflow or cls._get_namespace())) or wf
        return f"{tmp_dir_path}/{ns}/logs/{wf}.requests.json"

    @classmethod
    def _get_log_path_message(cls, data_dir_path: str = None, workflow: str = None, namespace: str = None) -> str:
        """Return the print message for the scaffold log file path."""
        file_path = cls._get_file_path(workflow=workflow, namespace=namespace)
        return f"Requests log path for workflow: {workflow}, namespace: {namespace}\nFile path: {file_path}"
