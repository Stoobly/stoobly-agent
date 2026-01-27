import hashlib
import os
import pytest
import shutil

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import SERVICES_NAMESPACE
from stoobly_agent.config.data_dir import DataDir, DATA_DIR_NAME
from stoobly_agent.test.test_helper import reset


class TestApp:

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture
    def tmp_app_dir(self, tmp_path):
        """Create a temporary app directory"""
        app_dir = os.path.join(tmp_path, 'test-app')
        os.makedirs(app_dir, exist_ok=True)
        return app_dir

    @pytest.fixture
    def tmp_context_dir(self, tmp_path):
        """Create a temporary context directory"""
        context_dir = os.path.join(tmp_path, 'test-context')
        os.makedirs(context_dir, exist_ok=True)
        return context_dir

    @pytest.fixture
    def app_with_scaffold(self, tmp_app_dir):
        """Create an app with scaffold structure"""
        # Create scaffold namespace directory
        data_dir_path = os.path.join(tmp_app_dir, DATA_DIR_NAME)
        scaffold_path = os.path.join(data_dir_path, SERVICES_NAMESPACE)
        os.makedirs(scaffold_path, exist_ok=True)
        
        # Create a dummy service
        service_path = os.path.join(scaffold_path, 'test-service')
        os.makedirs(service_path, exist_ok=True)
        
        return App(tmp_app_dir)

    class TestInit:
        """Test App initialization"""

        def test_init_with_basic_path(self, tmp_app_dir):
            """Test basic initialization with just a path"""
            app = App(tmp_app_dir)
            
            assert app.dir_path == os.path.abspath(tmp_app_dir)
            assert app.app_dir_path == os.path.abspath(tmp_app_dir)
            assert not app.containerized

        def test_init_with_relative_path(self, tmp_path):
            """Test initialization with relative path converts to absolute"""
            app = App('.')
            
            assert os.path.isabs(app.dir_path)
            assert os.path.isabs(app.app_dir_path)

        def test_init_with_custom_app_dir_path(self, tmp_app_dir, tmp_path):
            """Test initialization with custom app_dir_path"""
            custom_app_dir = os.path.join(tmp_path, 'custom-app')
            os.makedirs(custom_app_dir, exist_ok=True)
            
            app = App(tmp_app_dir, app_dir_path=custom_app_dir)
            
            assert app.dir_path == os.path.abspath(tmp_app_dir)
            assert app.app_dir_path == os.path.abspath(custom_app_dir)
            assert app.host_app_dir_path == os.path.abspath(custom_app_dir)

        def test_init_with_containerized_flag(self, tmp_app_dir):
            """Test initialization with containerized flag"""
            app = App(tmp_app_dir, containerized=True)
            
            assert app.containerized
            assert app.app_dir_path == os.path.abspath(tmp_app_dir)

        def test_init_with_custom_scaffold_namespace(self, tmp_app_dir):
            """Test initialization with custom scaffold namespace"""
            custom_namespace = 'custom-services'
            app = App(tmp_app_dir, scaffold_namespace=custom_namespace)
            
            assert app.scaffold_namespace == custom_namespace

        def test_init_with_dry_run(self, tmp_app_dir):
            """Test initialization with dry_run flag skips path validation"""
            # This should not raise an error even with non-existent paths
            app = App(tmp_app_dir, dry_run=True)
            
            # Should be able to set non-existent path when dry_run is True
            non_existent = '/non/existent/path'
            app.app_dir_path = non_existent
            assert app.app_dir_path == non_existent

    class TestProperties:
        """Test App property getters and setters"""

        def test_app_dir_path_returns_absolute_path(self, tmp_app_dir):
            """Test app_dir_path returns absolute path"""
            app = App(tmp_app_dir)
            
            assert os.path.isabs(app.app_dir_path)

        def test_ca_certs_dir_path_returns_absolute_path(self, tmp_app_dir):
            """Test ca_certs_dir_path returns absolute path"""
            app = App(tmp_app_dir)
            
            assert os.path.isabs(app.ca_certs_dir_path)

        def test_certs_dir_path_returns_absolute_path(self, tmp_app_dir):
            """Test certs_dir_path returns absolute path"""
            app = App(tmp_app_dir)
            
            assert os.path.isabs(app.certs_dir_path)

        def test_context_dir_path_returns_absolute_path(self, tmp_app_dir):
            """Test context_dir_path returns absolute path"""
            app = App(tmp_app_dir)
            
            assert os.path.isabs(app.context_dir_path)

        def test_data_dir_path_combines_context_and_data_dir_name(self, tmp_app_dir):
            """Test data_dir_path is context_dir_path + DATA_DIR_NAME"""
            app = App(tmp_app_dir)
            
            expected = os.path.join(app.context_dir_path, DATA_DIR_NAME)
            assert app.data_dir_path == expected

        def test_scaffold_namespace_path(self, tmp_app_dir):
            """Test scaffold_namespace_path combines data_dir_path and namespace"""
            app = App(tmp_app_dir)
            
            expected = os.path.join(app.data_dir_path, SERVICES_NAMESPACE)
            assert app.scaffold_namespace_path == expected

        def test_network_is_md5_of_context_dir(self, tmp_app_dir):
            """Test network property returns MD5 hash of context_dir_path"""
            app = App(tmp_app_dir)
            
            expected_hash = hashlib.md5(app.context_dir_path.encode()).hexdigest()
            assert app.network == expected_hash

        def test_network_changes_when_context_dir_changes(self, tmp_app_dir, tmp_context_dir):
            """Test network hash changes when context_dir_path changes"""
            app = App(tmp_app_dir, dry_run=True)
            
            original_network = app.network
            app.context_dir_path = tmp_context_dir
            new_network = app.network
            
            assert original_network != new_network

        def test_runtime_app_dir_path_with_host_value(self, tmp_app_dir, tmp_path):
            """Test runtime_app_dir_path with custom app_dir_path"""
            custom_app_dir = os.path.join(tmp_path, 'custom-app')
            os.makedirs(custom_app_dir, exist_ok=True)
            
            app = App(tmp_app_dir, app_dir_path=custom_app_dir)
            
            assert os.path.isabs(app.runtime_app_dir_path)

    class TestPropertySetters:
        """Test App property setters"""

        def test_set_app_dir_path_with_valid_path(self, tmp_app_dir, tmp_path):
            """Test setting app_dir_path with valid existing path"""
            app = App(tmp_app_dir)
            new_path = os.path.join(tmp_path, 'new-app')
            os.makedirs(new_path, exist_ok=True)
            
            app.app_dir_path = new_path
            assert app.app_dir_path == os.path.abspath(new_path)

        def test_set_app_dir_path_with_non_existent_raises_error(self, tmp_app_dir):
            """Test setting app_dir_path with non-existent path raises ValueError"""
            app = App(tmp_app_dir)
            non_existent = '/non/existent/path'
            
            with pytest.raises(ValueError, match="does not exist"):
                app.app_dir_path = non_existent

        def test_set_app_dir_path_with_non_string_raises_error(self, tmp_app_dir):
            """Test setting app_dir_path with non-string raises TypeError"""
            app = App(tmp_app_dir)
            
            with pytest.raises(TypeError, match="Expected a str"):
                app.app_dir_path = 123

        def test_set_ca_certs_dir_path(self, tmp_app_dir, tmp_path):
            """Test setting ca_certs_dir_path"""
            app = App(tmp_app_dir)
            new_path = os.path.join(tmp_path, 'new-ca-certs')
            os.makedirs(new_path, exist_ok=True)
            
            app.ca_certs_dir_path = new_path
            assert app.ca_certs_dir_path == os.path.abspath(new_path)

        def test_set_certs_dir_path(self, tmp_app_dir, tmp_path):
            """Test setting certs_dir_path"""
            app = App(tmp_app_dir)
            new_path = os.path.join(tmp_path, 'new-certs')
            os.makedirs(new_path, exist_ok=True)
            
            app.certs_dir_path = new_path
            assert app.certs_dir_path == os.path.abspath(new_path)

        def test_set_context_dir_path(self, tmp_app_dir, tmp_context_dir):
            """Test setting context_dir_path"""
            app = App(tmp_app_dir)
            
            app.context_dir_path = tmp_context_dir
            assert app.context_dir_path == os.path.abspath(tmp_context_dir)

    class TestHostProperties:
        """Test host_* properties that return kwarg values"""

        def test_host_app_dir_path_with_kwarg(self, tmp_app_dir, tmp_path):
            """Test host_app_dir_path returns kwarg value when provided"""
            custom_app_dir = os.path.join(tmp_path, 'custom-app')
            os.makedirs(custom_app_dir, exist_ok=True)
            
            app = App(tmp_app_dir, app_dir_path=custom_app_dir)
            
            assert app.host_app_dir_path == os.path.abspath(custom_app_dir)

        def test_host_app_dir_path_without_kwarg(self, tmp_app_dir):
            """Test host_app_dir_path falls back to app_dir_path"""
            app = App(tmp_app_dir)
            
            assert app.host_app_dir_path == app.app_dir_path

        def test_host_ca_certs_dir_path_with_kwarg(self, tmp_app_dir, tmp_path):
            """Test host_ca_certs_dir_path returns kwarg value when provided"""
            custom_ca_certs = os.path.join(tmp_path, 'custom-ca-certs')
            os.makedirs(custom_ca_certs, exist_ok=True)
            
            app = App(tmp_app_dir, ca_certs_dir_path=custom_ca_certs)
            
            assert app.host_ca_certs_dir_path == os.path.abspath(custom_ca_certs)

        def test_host_certs_dir_path_with_kwarg(self, tmp_app_dir, tmp_path):
            """Test host_certs_dir_path returns kwarg value when provided"""
            custom_certs = os.path.join(tmp_path, 'custom-certs')
            os.makedirs(custom_certs, exist_ok=True)
            
            app = App(tmp_app_dir, certs_dir_path=custom_certs)
            
            assert app.host_certs_dir_path == os.path.abspath(custom_certs)

        def test_host_context_dir_path_with_kwarg(self, tmp_app_dir, tmp_context_dir):
            """Test host_context_dir_path returns kwarg value when provided"""
            app = App(tmp_app_dir, context_dir_path=tmp_context_dir)
            
            assert app.host_context_dir_path == os.path.abspath(tmp_context_dir)

    class TestContainerizedMode:
        """Test App behavior in containerized mode"""

        def test_containerized_mode_uses_constructor_path(self, tmp_app_dir):
            """Test containerized mode uses path from constructor"""
            app = App(tmp_app_dir, containerized=True)
            
            assert app.containerized
            assert app.app_dir_path == os.path.abspath(tmp_app_dir)

        def test_containerized_mode_ignores_custom_app_dir_path(self, tmp_app_dir, tmp_path):
            """Test containerized mode ignores app_dir_path kwarg"""
            custom_app_dir = os.path.join(tmp_path, 'custom-app')
            os.makedirs(custom_app_dir, exist_ok=True)
            
            app = App(tmp_app_dir, containerized=True, app_dir_path=custom_app_dir)
            
            # In containerized mode, should use tmp_app_dir, not custom_app_dir
            assert app.app_dir_path == os.path.abspath(tmp_app_dir)

    class TestValid:
        """Test App.valid property"""

        def test_valid_returns_false_when_scaffold_does_not_exist(self, tmp_app_dir):
            """Test valid raises ValueError when scaffold namespace path doesn't exist"""
            app = App(tmp_app_dir)
            
            with pytest.raises(ValueError, match="does not exist"):
                app.valid

        def test_valid_returns_true_when_scaffold_exists(self, app_with_scaffold):
            """Test valid returns True when scaffold namespace path exists"""
            assert app_with_scaffold.valid

    class TestServices:
        """Test services-related properties"""

        def test_service_paths_returns_empty_list_when_no_services(self, tmp_app_dir):
            """Test service_paths returns empty list when no services exist"""
            # Create the scaffold directory but no services
            data_dir_path = os.path.join(tmp_app_dir, DATA_DIR_NAME)
            scaffold_path = os.path.join(data_dir_path, SERVICES_NAMESPACE)
            os.makedirs(scaffold_path, exist_ok=True)
            
            app = App(tmp_app_dir)
            
            assert app.service_paths == []

        def test_service_paths_returns_service_directories(self, app_with_scaffold):
            """Test service_paths returns paths to service directories"""
            # Add another service
            scaffold_path = app_with_scaffold.scaffold_namespace_path
            service2_path = os.path.join(scaffold_path, 'test-service-2')
            os.makedirs(service2_path, exist_ok=True)
            
            service_paths = app_with_scaffold.service_paths
            
            assert len(service_paths) == 2
            assert all(os.path.isdir(path) for path in service_paths)

        def test_service_paths_ignores_files(self, app_with_scaffold):
            """Test service_paths ignores files in scaffold namespace"""
            scaffold_path = app_with_scaffold.scaffold_namespace_path
            
            # Create a file (should be ignored)
            file_path = os.path.join(scaffold_path, 'readme.txt')
            with open(file_path, 'w') as f:
                f.write('test')
            
            service_paths = app_with_scaffold.service_paths
            
            # Should only have the one service directory, not the file
            assert len(service_paths) == 1

        def test_services_returns_service_names(self, app_with_scaffold):
            """Test services returns list of service names"""
            # Add another service
            scaffold_path = app_with_scaffold.scaffold_namespace_path
            service2_path = os.path.join(scaffold_path, 'another-service')
            os.makedirs(service2_path, exist_ok=True)
            
            services = app_with_scaffold.services
            
            assert len(services) == 2
            assert 'test-service' in services
            assert 'another-service' in services

    class TestCopyFoldersAndHiddenFiles:
        """Test copy_folders_and_hidden_files method"""

        def test_copy_creates_destination_directory(self, tmp_app_dir, tmp_path):
            """Test copy creates destination directory if it doesn't exist"""
            app = App(tmp_app_dir)
            
            src = os.path.join(tmp_path, 'src')
            dst = os.path.join(tmp_path, 'dst')
            os.makedirs(src, exist_ok=True)
            
            app.copy_folders_and_hidden_files(src, dst)
            
            assert os.path.exists(dst)

        def test_copy_copies_hidden_files(self, tmp_app_dir, tmp_path):
            """Test copy copies hidden files"""
            app = App(tmp_app_dir)
            
            src = os.path.join(tmp_path, 'src')
            dst = os.path.join(tmp_path, 'dst')
            os.makedirs(src, exist_ok=True)
            
            # Create a hidden file
            hidden_file = os.path.join(src, '.hidden')
            with open(hidden_file, 'w') as f:
                f.write('hidden content')
            
            app.copy_folders_and_hidden_files(src, dst)
            
            dst_hidden = os.path.join(dst, '.hidden')
            assert os.path.exists(dst_hidden)
            with open(dst_hidden, 'r') as f:
                assert f.read() == 'hidden content'

        def test_copy_copies_regular_files_if_not_exists(self, tmp_app_dir, tmp_path):
            """Test copy copies regular files if they don't exist in destination"""
            app = App(tmp_app_dir)
            
            src = os.path.join(tmp_path, 'src')
            dst = os.path.join(tmp_path, 'dst')
            os.makedirs(src, exist_ok=True)
            
            # Create a regular file
            regular_file = os.path.join(src, 'file.txt')
            with open(regular_file, 'w') as f:
                f.write('content')
            
            app.copy_folders_and_hidden_files(src, dst)
            
            dst_file = os.path.join(dst, 'file.txt')
            assert os.path.exists(dst_file)

        def test_copy_skips_existing_regular_files(self, tmp_app_dir, tmp_path):
            """Test copy skips regular files if they already exist in destination"""
            app = App(tmp_app_dir)
            
            src = os.path.join(tmp_path, 'src')
            dst = os.path.join(tmp_path, 'dst')
            os.makedirs(src, exist_ok=True)
            os.makedirs(dst, exist_ok=True)
            
            # Create file in source
            src_file = os.path.join(src, 'file.txt')
            with open(src_file, 'w') as f:
                f.write('new content')
            
            # Create existing file in destination
            dst_file = os.path.join(dst, 'file.txt')
            with open(dst_file, 'w') as f:
                f.write('old content')
            
            app.copy_folders_and_hidden_files(src, dst)
            
            # Destination file should not be overwritten
            with open(dst_file, 'r') as f:
                assert f.read() == 'old content'

        def test_copy_overwrites_hidden_files(self, tmp_app_dir, tmp_path):
            """Test copy overwrites hidden files even if they exist"""
            app = App(tmp_app_dir)
            
            src = os.path.join(tmp_path, 'src')
            dst = os.path.join(tmp_path, 'dst')
            os.makedirs(src, exist_ok=True)
            os.makedirs(dst, exist_ok=True)
            
            # Create hidden file in source
            src_hidden = os.path.join(src, '.hidden')
            with open(src_hidden, 'w') as f:
                f.write('new hidden')
            
            # Create existing hidden file in destination
            dst_hidden = os.path.join(dst, '.hidden')
            with open(dst_hidden, 'w') as f:
                f.write('old hidden')
            
            app.copy_folders_and_hidden_files(src, dst)
            
            # Hidden file should be overwritten
            with open(dst_hidden, 'r') as f:
                assert f.read() == 'new hidden'

        def test_copy_respects_ignore_patterns(self, tmp_app_dir, tmp_path):
            """Test copy respects ignore patterns"""
            app = App(tmp_app_dir)
            
            src = os.path.join(tmp_path, 'src')
            dst = os.path.join(tmp_path, 'dst')
            os.makedirs(src, exist_ok=True)
            
            # Create files
            file1 = os.path.join(src, 'keep.txt')
            file2 = os.path.join(src, 'ignore.txt')
            with open(file1, 'w') as f:
                f.write('keep')
            with open(file2, 'w') as f:
                f.write('ignore')
            
            # Copy with ignore pattern
            app.copy_folders_and_hidden_files(src, dst, ignore=['ignore.txt'])
            
            assert os.path.exists(os.path.join(dst, 'keep.txt'))
            assert not os.path.exists(os.path.join(dst, 'ignore.txt'))

        def test_copy_handles_nested_directories(self, tmp_app_dir, tmp_path):
            """Test copy handles nested directory structures"""
            app = App(tmp_app_dir)
            
            src = os.path.join(tmp_path, 'src')
            dst = os.path.join(tmp_path, 'dst')
            nested = os.path.join(src, 'subdir', 'nested')
            os.makedirs(nested, exist_ok=True)
            
            # Create file in nested directory
            nested_file = os.path.join(nested, '.config')
            with open(nested_file, 'w') as f:
                f.write('nested config')
            
            app.copy_folders_and_hidden_files(src, dst)
            
            dst_nested = os.path.join(dst, 'subdir', 'nested', '.config')
            assert os.path.exists(dst_nested)
            with open(dst_nested, 'r') as f:
                assert f.read() == 'nested config'

    class TestDenormalize:
        """Test denormalize method"""

        @pytest.fixture
        def workflow_namespace_mock(self, tmp_path):
            """Create a mock workflow namespace"""
            from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace
            
            namespace_path = os.path.join(tmp_path, 'workflows')
            os.makedirs(namespace_path, exist_ok=True)
            
            # Create a minimal app to get a workflow namespace
            app = App(tmp_path)
            return WorkflowNamespace(app, 'test-workflow')

        def test_denormalize_without_migrate_returns_true(self, tmp_app_dir, workflow_namespace_mock):
            """Test denormalize without migrate flag returns True"""
            app = App(tmp_app_dir, app_dir_path=tmp_app_dir)
            
            result = app.denormalize(workflow_namespace_mock, migrate=False)
            
            assert result is True

        def test_denormalize_updates_runtime_app_dir_path(self, tmp_app_dir, workflow_namespace_mock):
            """Test denormalize updates runtime_app_dir_path"""
            app = App(tmp_app_dir, app_dir_path=tmp_app_dir)
            
            original_runtime_path = app.runtime_app_dir_path
            app.denormalize(workflow_namespace_mock, migrate=False)
            
            # runtime_app_dir_path should include relative path to workflow namespace
            assert app.runtime_app_dir_path != original_runtime_path

    class TestDataDir:
        """Test data_dir related properties"""

        def test_data_dir_returns_data_dir_instance(self, tmp_app_dir):
            """Test data_dir returns DataDir instance"""
            app = App(tmp_app_dir)
            
            assert isinstance(app.data_dir, DataDir)

        def test_app_data_dir_returns_data_dir_instance(self, tmp_app_dir):
            """Test app_data_dir returns DataDir instance"""
            app = App(tmp_app_dir)
            
            assert isinstance(app.app_data_dir, DataDir)

        def test_data_dir_path_property_returns_string(self, tmp_app_dir):
            """Test data_dir_path property returns string path"""
            app = App(tmp_app_dir)
            
            assert isinstance(app.data_dir_path, str)
            assert DATA_DIR_NAME in app.data_dir_path
