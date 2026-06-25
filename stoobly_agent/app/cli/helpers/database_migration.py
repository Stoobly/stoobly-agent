import sys

from typing import List, Optional

CONTEXT_DIR_PATH_OPTION = '--context-dir-path'

# Top-level commands that should not trigger automatic database migration.
SKIP_MIGRATION_COMMANDS = {
  'ca-cert',
  'describe',
  'dev-tools',
  'feature',
  'init',
  'intercept',
  'scaffold',
  'setting'
}


def non_option_args(argv: List[str] = None) -> List[str]:
  """Extract positional command tokens from CLI argv, ignoring flags and their values.

  Used to determine the command path (e.g. ``['scaffold', 'app', 'create']``) before
  Click invokes the target command.

  Args:
    argv: CLI arguments excluding the program name. Defaults to ``sys.argv[1:]``.

  Returns:
    Positional tokens in argv order, with options and option values removed.
  """
  if argv is None:
    argv = sys.argv[1:]

  args = []
  skip_next = False

  for index, arg in enumerate(argv):
    if skip_next:
      skip_next = False
      continue

    if arg in ('-h', '--help', '--version'):
      continue

    if arg.startswith('-'):
      if '=' not in arg and index + 1 < len(argv) and not argv[index + 1].startswith('-'):
        skip_next = True
      continue

    args.append(arg)

  return args


def resolve_context_dir_path_from_argv(argv: List[str] = None) -> Optional[str]:
  """Resolve the Stoobly context directory path from ``--context-dir-path`` in argv.

  Supports both ``--context-dir-path /path`` and ``--context-dir-path=/path`` forms.
  When the flag is absent, returns ``None`` so callers can fall back to the default
  data directory for the current working directory.

  Args:
    argv: CLI arguments excluding the program name. Defaults to ``sys.argv[1:]``.

  Returns:
    The context directory path if ``--context-dir-path`` is present, otherwise ``None``.
  """
  if argv is None:
    argv = sys.argv[1:]

  context_dir_path = None
  index = 0

  while index < len(argv):
    arg = argv[index]

    if arg == CONTEXT_DIR_PATH_OPTION:
      if index + 1 < len(argv):
        context_dir_path = argv[index + 1]
        index += 2
        continue
    elif arg.startswith(f'{CONTEXT_DIR_PATH_OPTION}='):
      context_dir_path = arg.split('=', 1)[1]

    index += 1

  return context_dir_path

def should_skip_database_migration(command_path: List[str]) -> bool:
  """Determine whether automatic database migration should be skipped.

  Migration is skipped when no command is invoked, when the command manages its
  own database setup (``init``), or when it runs migration explicitly
  (``dev-tools migrate``).

  Args:
    command_path: Positional command tokens from :func:`non_option_args`.

  Returns:
    ``True`` if migration should be skipped, otherwise ``False``.
  """
  if not command_path:
    return True

  top_level = command_path[0]

  if top_level in SKIP_MIGRATION_COMMANDS:
    return True

  return False
