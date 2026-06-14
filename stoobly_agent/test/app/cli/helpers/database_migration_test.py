from stoobly_agent.app.cli.helpers.database_migration import (
  SKIP_MIGRATION_COMMANDS,
  non_option_args,
  resolve_context_dir_path_from_argv,
  should_skip_database_migration,
)


class TestNonOptionArgs:
  def test_skips_options_and_their_values(self):
    assert non_option_args([
      'scaffold', 'app', 'create', 'myapp',
      '--context-dir-path', '/tmp/app',
      '--plugin', 'playwright',
    ]) == ['scaffold', 'app', 'create', 'myapp']

  def test_skips_help(self):
    assert non_option_args(['--help']) == []
    assert non_option_args(['scaffold', '--help']) == ['scaffold']


class TestResolveContextDirPathFromArgv:
  def test_returns_none_without_context_dir_path(self):
    argv = ['scaffold', 'app', 'create', 'myapp', '--app-dir-path', '/tmp/app']

    assert resolve_context_dir_path_from_argv(argv) is None

  def test_supports_space_separated_form(self):
    argv = ['scaffold', 'workflow', 'up', '--context-dir-path', '/tmp/context']

    assert resolve_context_dir_path_from_argv(argv) == '/tmp/context'

  def test_supports_equals_form(self):
    argv = ['request', 'logs', 'list', '--context-dir-path=/tmp/context']

    assert resolve_context_dir_path_from_argv(argv) == '/tmp/context'


class TestShouldSkipDatabaseMigration:
  def test_skips_without_command(self):
    assert should_skip_database_migration([]) is True

  def test_skips_top_level_commands(self):
    for command in SKIP_MIGRATION_COMMANDS:
      assert should_skip_database_migration([command]) is True

  def test_skips_subcommands_of_skip_commands(self):
    assert should_skip_database_migration(['dev-tools', 'migrate']) is True
    assert should_skip_database_migration(['scaffold', 'app', 'create']) is True

  def test_runs_for_other_commands(self):
    assert should_skip_database_migration(['mock']) is False
    assert should_skip_database_migration(['request', 'logs', 'list']) is False
