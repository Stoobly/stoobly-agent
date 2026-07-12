"""Initialize and update Stoobly context directories for scaffold commands.

When ``scaffold app create`` or ``scaffold service create`` is run with one or
more ``--context-dir-path`` options, each context directory gets a lightweight
Stoobly init and a ``.stoobly/.config.yml`` file linking it to the app scaffold.
``scaffold app create`` also writes ``app_dir/.stoobly/.config.yml`` with
``scaffold.context_dir_paths`` listing relative paths to each context directory.

This module is invoked from ``scaffold_cli`` after app or service create builds.
"""

import os

from mergedeep import merge

from stoobly_agent.app.cli.scaffold.config import Config
from stoobly_agent.app.cli.scaffold.constants import CONFIG_FILE, SERVICES_NAMESPACE
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DATA_DIR_NAME, DataDir

SCAFFOLD_CONFIG_KEY = 'scaffold'
APP_DIR_PATH_CONFIG_KEY = 'app_dir_path'
CONTEXT_DIR_PATHS_CONFIG_KEY = 'context_dir_paths'
SERVICES_CONFIG_KEY = 'services'


def _ensure_context_dir(context_dir_path: str) -> str:
  abs_context_dir = os.path.abspath(context_dir_path)

  DataDir.instance(abs_context_dir).create(abs_context_dir)
  Settings.instance(abs_context_dir)

  return abs_context_dir


def _read_scaffold_config(context_dir_path: str) -> tuple[Config, dict, dict]:
  config = Config(os.path.join(context_dir_path, DATA_DIR_NAME))
  existing = config.read() or {}
  existing_scaffold = existing.get(SCAFFOLD_CONFIG_KEY) or {}
  return config, existing, existing_scaffold


def _write_scaffold_config(
  config: Config,
  existing: dict,
  existing_scaffold: dict,
  relative_app_dir_path: str,
  services: list,
) -> None:
  merged = merge({}, existing, {
    SCAFFOLD_CONFIG_KEY: merge({}, existing_scaffold, {
      APP_DIR_PATH_CONFIG_KEY: relative_app_dir_path,
      SERVICES_CONFIG_KEY: services,
    }),
  })
  config.write(merged)


def init_context_dir(context_dir_path: str, app_dir_path: str) -> None:
  """Prepare a context directory and record the app dir in its ``.stoobly/.config.yml``.

  For each context dir passed to ``scaffold app create``:

  1. Create ``context_dir/.stoobly`` if missing (same as a lightweight init).
  2. Create ``context_dir/.stoobly/settings.yml`` from the default template if
     missing. Existing settings are not reset.
  3. Write ``context_dir/.stoobly/.config.yml`` with ``scaffold.app_dir_path`` set to the
     relative path from the context dir to the app dir (e.g. ``../app``).
  4. Reset ``scaffold.services`` to an empty array.

  If ``context_dir/.stoobly/.config.yml`` already exists, other properties are preserved.

  Args:
    context_dir_path: Host path to the Stoobly context directory (parent of
      ``.stoobly``).
    app_dir_path: Host path to the application directory where the scaffold
      was created.
  """
  abs_context_dir = _ensure_context_dir(context_dir_path)
  abs_app_dir = os.path.abspath(app_dir_path)
  relative_app_dir_path = os.path.relpath(abs_app_dir, abs_context_dir)

  config, existing, existing_scaffold = _read_scaffold_config(abs_context_dir)

  _write_scaffold_config(config, existing, existing_scaffold, relative_app_dir_path, [])


def init_app_context_config(app_dir_path: str, context_dir_paths) -> None:
  """Write ``app_dir/.stoobly/.config.yml`` with relative paths to each context dir.

  Sets ``scaffold.context_dir_paths`` to the relative path from the app dir to each
  context directory (e.g. ``../context``). Other existing config properties are
  preserved.

  Args:
    app_dir_path: Host path to the application directory where the scaffold
      was created.
    context_dir_paths: Host paths to Stoobly context directories linked to the
      app.
  """
  abs_app_dir = _ensure_context_dir(app_dir_path)
  relative_paths = [
    os.path.relpath(os.path.abspath(context_dir_path), abs_app_dir)
    for context_dir_path in context_dir_paths
  ]

  config, existing, existing_scaffold = _read_scaffold_config(abs_app_dir)
  merged = merge({}, existing, {
    SCAFFOLD_CONFIG_KEY: merge({}, existing_scaffold, {
      CONTEXT_DIR_PATHS_CONFIG_KEY: relative_paths,
    }),
  })
  config.write(merged)


def add_context_service(context_dir_path: str, app_dir_path: str, service_name: str) -> None:
  """Add a service to ``scaffold.services`` in a context dir ``.stoobly/.config.yml``.

  For each context dir passed to ``scaffold service create``:

  1. Ensure ``context_dir/.stoobly`` and ``settings.yml`` exist.
  2. Update ``scaffold.app_dir_path`` to the relative path from the context dir
     to the app dir.
  3. Append ``service_name`` to ``scaffold.services`` if not already listed.

  Args:
    context_dir_path: Host path to the Stoobly context directory (parent of
      ``.stoobly``).
    app_dir_path: Host path to the application directory where the service
      scaffold was created.
    service_name: Name of the scaffolded service to record.
  """
  abs_context_dir = _ensure_context_dir(context_dir_path)
  abs_app_dir = os.path.abspath(app_dir_path)
  relative_app_dir_path = os.path.relpath(abs_app_dir, abs_context_dir)

  config, existing, existing_scaffold = _read_scaffold_config(abs_context_dir)
  services = list(existing_scaffold.get(SERVICES_CONFIG_KEY) or [])

  if service_name not in services:
    services.append(service_name)

  _write_scaffold_config(config, existing, existing_scaffold, relative_app_dir_path, services)


def get_context_services(context_dir_path: str) -> list[str]:
  """Return ``scaffold.services`` from a context dir ``.stoobly/.config.yml``, or ``[]`` if unset."""
  _, _, existing_scaffold = _read_scaffold_config(os.path.abspath(context_dir_path))
  return list(existing_scaffold.get(SERVICES_CONFIG_KEY) or [])


def _context_config_path(context_dir_path: str) -> str:
  return os.path.join(os.path.abspath(context_dir_path), DATA_DIR_NAME, CONFIG_FILE)


def resolve_app_dir_path(context_dir_path: str, app_dir_path: str = None) -> str:
  """Resolve the application scaffold directory for a Stoobly context directory.

  Resolution order:

  1. If ``context_dir/.stoobly/.config.yml`` exists and sets ``scaffold.app_dir_path``,
     resolve that path relative to the context directory.
  2. Else if ``app_dir_path`` is provided, use it.
  3. Else if ``context_dir/.stoobly/services`` exists, return ``context_dir``.
  4. Else raise ``ValueError``.
  """
  abs_context_dir = os.path.abspath(context_dir_path)
  config_path = _context_config_path(abs_context_dir)

  if os.path.exists(config_path):
    _, _, existing_scaffold = _read_scaffold_config(abs_context_dir)
    relative_app_dir_path = existing_scaffold.get(APP_DIR_PATH_CONFIG_KEY)
    if relative_app_dir_path:
      return os.path.abspath(os.path.join(abs_context_dir, relative_app_dir_path))

  if app_dir_path:
    return os.path.abspath(app_dir_path)

  services_dir = os.path.join(abs_context_dir, DATA_DIR_NAME, SERVICES_NAMESPACE)
  if os.path.isdir(services_dir):
    return abs_context_dir

  raise ValueError(
    f"Could not resolve app directory from context '{abs_context_dir}'. "
    "Run scaffold app create with --context-dir-path, or pass --app-dir-path."
  )
