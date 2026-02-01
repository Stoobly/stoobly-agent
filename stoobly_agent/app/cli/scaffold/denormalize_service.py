import os
import shutil

from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace
from stoobly_agent.config.data_dir import DATA_DIR_NAME, TMP_DIR_NAME, DataDir
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

    def denormalize_up(self):
        """
        Copy scaffold namespace from data_dir to context_dir.
        """
        if not os.path.exists(self.source_path):
            self.logger.error(f"Source path does not exist: {self.source_path}")
            return False

        if self.source_path == self.destination_path:
            return True

        try:
            shutil.copytree(self.source_path, self.destination_path, dirs_exist_ok=True)

            self.logger.debug(f"Denormalized scaffold to {self.destination_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to copy scaffold namespace: {e}")
            return False

    def denormalize_down(self, script: str):
        # Remove existing destination folder contents if it exists
        
        # Within a container, host_scaffold_namespace_path does not exist, check self.destination_path
        destination_path = self.destination_path
        if os.path.exists(destination_path): 
            if not script:
                self.logger.debug(f"Removing existing destination contents: {destination_path}")
                try:
                    shutil.rmtree(destination_path)
                except Exception as e:
                    self.logger.error(f"Failed to remove destination: {e}")
                    if os.path.exists(destination_path):
                        return False
            else:
                destination_path = self.app.host_runtime_scaffold_namespace_path

                print(f"rm -rf {destination_path}", file=script)