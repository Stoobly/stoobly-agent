import os
import shutil

from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.logger import Logger

from .app import App

LOG_ID = 'DenormalizeService'

class DenormalizeService:
    """
    Service to handle denormalization of scaffold namespace from data_dir to context_dir.
    This allows the app to run with all its configuration in the context directory.
    """

    def __init__(self, workflow_namespace: WorkflowNamespace):
        self.app = workflow_namespace.app
        self.logger = Logger.instance(LOG_ID)
        self.denormalized_app = App(workflow_namespace.path)

    @property
    def source_path(self):
        """Source path: scaffold_namespace_path from data_dir"""
        return self.app.scaffold_namespace_path

    @property
    def destination_path(self):
        """Destination path: scaffold_namespace_path in context_dir"""
        return self.denormalized_app.scaffold_namespace_path

    def denormalize(self):
        """
        Copy scaffold namespace from data_dir to context_dir.
        If the folder exists in the destination, remove it first.
        """
        if not os.path.exists(self.source_path):
            self.logger.error(f"Source path does not exist: {self.source_path}")
            return False

        if self.source_path == self.destination_path:
            return True

        # Remove existing destination folder if it exists
        if os.path.exists(self.destination_path):
            self.logger.debug(f"Removing existing destination: {self.destination_path}")
            try:
                shutil.rmtree(self.destination_path)
            except Exception as e:
                self.logger.error(f"Failed to remove destination: {e}")
                if os.path.exists(self.destination_path):
                    return False

        # Copy the folder
        try:
            shutil.copytree(self.source_path, self.destination_path)
            self.logger.debug(f"Denormalized scaffold to {self.destination_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to copy scaffold namespace: {e}")
            return False
