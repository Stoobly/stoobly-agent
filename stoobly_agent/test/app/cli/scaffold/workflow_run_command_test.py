import os
import pytest
import shutil

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.app_config import AppConfig
from stoobly_agent.app.cli.scaffold.app_create_command import AppCreateCommand
from stoobly_agent.app.cli.scaffold.constants import SERVICES_NAMESPACE
from stoobly_agent.app.cli.scaffold.denormalize_service import DenormalizeService
from stoobly_agent.app.cli.scaffold.workflow_run_command import WorkflowRunCommand
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.test_helper import reset


class TestDenormalizeDown():
    """Test suite for the denormalize_down functionality"""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='function')
    def app_dir_path(self):
        """Create a temporary app directory for testing"""
        data_dir: DataDir = DataDir.instance()
        path = os.path.abspath(os.path.join(data_dir.tmp_dir_path, '..', '..', 'test-app'))
        os.makedirs(path, exist_ok=True)
        yield path
        # Cleanup after test
        if os.path.exists(path):
            shutil.rmtree(path)

    @pytest.fixture(scope='function')
    def app(self, app_dir_path):
        """Create an App instance"""
        return App(app_dir_path)

    @pytest.fixture(scope='function')
    def app_with_scaffold(self, app_dir_path):
        """Create an app with scaffolding"""
        app = App(app_dir_path)
        
        # Create the scaffold namespace directory
        scaffold_path = app.scaffold_namespace_path
        os.makedirs(scaffold_path, exist_ok=True)
        
        # Create some test files in the scaffold
        test_file = os.path.join(scaffold_path, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        # Create a test service directory
        test_service_dir = os.path.join(scaffold_path, 'test-service')
        os.makedirs(test_service_dir, exist_ok=True)
        
        service_file = os.path.join(test_service_dir, 'config.yml')
        with open(service_file, 'w') as f:
            f.write('service: test')
        
        yield app

    @pytest.fixture(scope='function')
    def denormalizable_app(self, app_dir_path):
        """Create an app with denormalize enabled"""
        app = App(app_dir_path)
        
        # Create the scaffold namespace directory
        scaffold_path = app.scaffold_namespace_path
        os.makedirs(scaffold_path, exist_ok=True)
        
        # Create app config with denormalize enabled
        app_config = AppConfig(scaffold_path)
        app_config.denormalize = True
        app_config.name = 'test-app'
        app_config.write()
        
        # Create some test files
        test_file = os.path.join(scaffold_path, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        yield app

    @pytest.fixture(scope='function')
    def workflow_run_command(self, denormalizable_app):
        """Create a WorkflowRunCommand instance"""
        return WorkflowRunCommand(
            denormalizable_app,
            workflow_name='test-workflow',
            service_name='test-service'
        )

    def test_denormalize_down_updates_app_to_denormalized_app(
        self, workflow_run_command, denormalizable_app
    ):
        """Test that denormalize_down updates self.app to the denormalized app"""
        original_app = workflow_run_command.app
        
        # Call denormalize_down
        options = {'namespace': 'test-workflow'}
        workflow_run_command.denormalize_down(options)
        
        # Verify app object has been replaced (different instance)
        assert workflow_run_command.app is not original_app

    def test_denormalize_down_updates_app_dir_path(
        self, workflow_run_command, denormalizable_app
    ):
        """Test that denormalize_down updates the app_dir_path property"""
        # Call denormalize_down
        options = {'namespace': 'test-workflow'}
        workflow_run_command.denormalize_down(options)
        
        # Verify app_dir_path equals the app's dir_path
        assert workflow_run_command.app_dir_path == workflow_run_command.app.dir_path

    def test_denormalize_down_updates_network(
        self, workflow_run_command
    ):
        """Test that denormalize_down updates the network property"""
        original_network = workflow_run_command.network
        
        # Call denormalize_down
        options = {'namespace': 'test-workflow'}
        workflow_run_command.denormalize_down(options)
        
        # Verify network has expected format with namespace and app network hash
        assert workflow_run_command.network.startswith('test-workflow.')
        assert len(workflow_run_command.network) > len('test-workflow.')

    def test_denormalize_down_updates_options_app_dir_path(
        self, workflow_run_command, denormalizable_app
    ):
        """Test that denormalize_down updates the app_dir_path in options"""
        options = {'namespace': 'test-workflow'}
        
        # Call denormalize_down
        workflow_run_command.denormalize_down(options)
        
        # Verify options has been updated
        assert 'app_dir_path' in options
        assert options['app_dir_path'] == denormalizable_app.context_dir_path

    def test_denormalize_down_preserves_other_options(
        self, workflow_run_command
    ):
        """Test that denormalize_down preserves other options"""
        options = {
            'namespace': 'test-workflow',
            'user_id': 1000,
            'detached': True,
            'custom_option': 'custom_value'
        }
        
        # Call denormalize_down
        workflow_run_command.denormalize_down(options)
        
        # Verify other options are preserved
        assert options['namespace'] == 'test-workflow'
        assert options['user_id'] == 1000
        assert options['detached'] is True
        assert options['custom_option'] == 'custom_value'

    def test_denormalize_down_with_empty_options(
        self, workflow_run_command
    ):
        """Test that denormalize_down works with empty options dict"""
        options = {}
        
        # Call denormalize_down - should not raise exception
        workflow_run_command.denormalize_down(options)
        
        # Verify app_dir_path was added to options
        assert 'app_dir_path' in options

    def test_denormalize_down_idempotent(
        self, workflow_run_command, denormalizable_app
    ):
        """Test that calling denormalize_down multiple times is idempotent"""
        options = {'namespace': 'test-workflow'}
        
        # Call denormalize_down first time
        workflow_run_command.denormalize_down(options)
        first_app_dir = workflow_run_command.app_dir_path
        first_network = workflow_run_command.network
        
        # Call denormalize_down second time
        workflow_run_command.denormalize_down(options)
        second_app_dir = workflow_run_command.app_dir_path
        second_network = workflow_run_command.network
        
        # Verify results are the same
        assert first_app_dir == second_app_dir
        assert first_network == second_network
        assert workflow_run_command.app_dir_path == denormalizable_app.context_dir_path

    def test_denormalize_down_creates_denormalized_app_with_correct_path(
        self, workflow_run_command, denormalizable_app
    ):
        """Test that denormalized app has correct dir_path"""
        options = {'namespace': 'test-workflow'}
        
        # Call denormalize_down
        workflow_run_command.denormalize_down(options)
        
        # Verify the denormalized app's dir_path equals context_dir_path
        assert workflow_run_command.app.dir_path == denormalizable_app.context_dir_path
        
        # Verify scaffold_namespace_path contains SERVICES_NAMESPACE
        assert SERVICES_NAMESPACE in workflow_run_command.app.scaffold_namespace_path

    def test_denormalize_down_network_format(
        self, workflow_run_command
    ):
        """Test that network has correct format after denormalization"""
        options = {'namespace': 'test-workflow'}
        workflow_run_command.denormalize_down(options)
        
        # Network should have format: <namespace>.<app_network_hash>
        network_parts = workflow_run_command.network.split('.')
        assert len(network_parts) == 2
        assert network_parts[0] == 'test-workflow'
        # Second part should be a hash (32 char hex string)
        assert len(network_parts[1]) == 32

    def test_denormalize_down_with_multiple_services(
        self, denormalizable_app
    ):
        """Test denormalize_down with multiple service instances"""
        # Create multiple workflow run command instances
        command1 = WorkflowRunCommand(
            denormalizable_app,
            workflow_name='test-workflow',
            service_name='service-1'
        )
        command2 = WorkflowRunCommand(
            denormalizable_app,
            workflow_name='test-workflow',
            service_name='service-2'
        )
        
        options1 = {'namespace': 'test-workflow'}
        options2 = {'namespace': 'test-workflow'}
        
        # Denormalize both
        command1.denormalize_down(options1)
        command2.denormalize_down(options2)
        
        # Both should have same app_dir_path (context_dir_path)
        assert command1.app_dir_path == command2.app_dir_path
        assert command1.app_dir_path == denormalizable_app.context_dir_path
        
        # Both options should be updated
        assert options1['app_dir_path'] == options2['app_dir_path']

    def test_denormalize_down_namespace_option_preserved(
        self, workflow_run_command
    ):
        """Test that namespace in options is not modified"""
        options = {'namespace': 'custom-namespace'}
        
        workflow_run_command.denormalize_down(options)
        
        # Namespace should remain unchanged
        assert options['namespace'] == 'custom-namespace'

    def test_denormalize_down_updates_internal_state_correctly(
        self, workflow_run_command, denormalizable_app
    ):
        """Test that internal state is updated correctly after denormalize_down"""
        options = {'namespace': 'test-workflow'}
        
        # Get original values
        original_app = workflow_run_command.app
        
        # Call denormalize_down
        workflow_run_command.denormalize_down(options)
        
        # Verify all internal state is consistent
        assert workflow_run_command.app is not original_app
        assert workflow_run_command.app_dir_path == workflow_run_command.app.dir_path
        assert workflow_run_command.app.dir_path == denormalizable_app.context_dir_path

    def test_denormalize_down_with_nested_namespace(
        self, denormalizable_app
    ):
        """Test denormalize_down with a nested namespace value"""
        command = WorkflowRunCommand(
            denormalizable_app,
            workflow_name='test-workflow',
            service_name='test-service',
            namespace='nested-namespace'
        )
        
        options = {'namespace': 'nested-namespace'}
        command.denormalize_down(options)
        
        # Should still work and update app_dir_path
        assert command.app_dir_path == denormalizable_app.context_dir_path
        assert options['app_dir_path'] == denormalizable_app.context_dir_path
