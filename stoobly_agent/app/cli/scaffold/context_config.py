"""Initialize and update Stoobly context directories for scaffold commands.

When ``scaffold app create`` or ``scaffold service create`` is run with one or
more ``--context-dir-path`` options, each context directory gets a lightweight
Stoobly init and a ``.config.yml`` file linking it to the app scaffold.

This module is invoked from ``scaffold_cli`` after app or service create builds.
"""

import os

from mergedeep import merge

from stoobly_agent.app.cli.scaffold.config import Config
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DataDir

SCAFFOLD_CONFIG_KEY = 'scaffold'
APP_DIR_PATH_CONFIG_KEY = 'app_dir_path'
SERVICES_CONFIG_KEY = 'services'


def _ensure_context_dir(context_dir_path: str) -> str:
  abs_context_dir = os.path.abspath(context_dir_path)

  DataDir.instance(abs_context_dir).create(abs_context_dir)
  Settings.instance(abs_context_dir)

  return abs_context_dir


def _read_scaffold_config(context_dir_path: str) -> tuple[Config, dict, dict]:
  config = Config(context_dir_path)
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
  """Prepare a context directory and record the app dir in its ``.config.yml``.

  For each context dir passed to ``scaffold app create``:

  1. Create ``context_dir/.stoobly`` if missing (same as a lightweight init).
  2. Create ``context_dir/.stoobly/settings.yml`` from the default template if
     missing. Existing settings are not reset.
  3. Write ``context_dir/.config.yml`` with ``scaffold.app_dir_path`` set to the
     relative path from the context dir to the app dir (e.g. ``../app``).
  4. Reset ``scaffold.services`` to an empty array.

  If ``context_dir/.config.yml`` already exists, other properties are preserved.

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


def add_context_service(context_dir_path: str, app_dir_path: str, service_name: str) -> None:
  """Add a service to ``scaffold.services`` in a context dir ``.config.yml``.

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
