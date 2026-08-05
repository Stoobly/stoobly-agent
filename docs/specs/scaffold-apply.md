# Scaffold apply

## Overview

`stoobly-agent scaffold apply` runs an ordered list of scaffold CLI commands from a config file. The config maps 1:1 to `stoobly-agent scaffold <resource> <action> …`, so a script like `scaffold-test.sh` can be expressed declaratively.

Supported formats: **YAML** (default) and **JSON**.

Config file format: [`scaffold-yml.md`](scaffold-yml.md).

## CLI

```bash
stoobly-agent scaffold apply PATH [--format yaml|json] [--dry-run]
```

| Argument / option | Description |
|-------------------|-------------|
| `PATH` | Path to the config file. Must exist and be a file. |
| `--format` | Config file format. Choices: `yaml`, `json`. Default: `yaml`. |
| `--dry-run` | Validate and log each step as `would apply …` without invoking any commands. |

## Behavior

```mermaid
flowchart LR
  configFile[Config file] --> applyCmd[scaffold apply]
  applyCmd --> loader[Load and validate]
  loader --> steps["resource + action + options"]
  steps --> resolve[Click group lookup]
  resolve --> invoke[make_context + invoke]
  invoke --> existingCmds[Existing scaffold commands]
```

1. Parse the file using `--format` (`yaml` or `json`).
2. Validate `version` and `commands` (see [config schema](scaffold-yml.md)). Each step’s `resource` / `action` / `options` are checked against [`scaffold.opencli.yaml`](../../stoobly_agent/app/cli/scaffold.opencli.yaml) before any step runs.
3. For each step in order:
   - Expand path options (relative to the config file’s directory).
   - Resolve `resource` / `action` on the Click `scaffold` group.
   - Convert `options` to CLI argv and log `applying <resource> <action> [positionals…]` (or `would apply …` with `--dry-run`; positional argument values only; option flags such as `--hostname` are not logged).
   - Unless `--dry-run`, invoke the command via Click `make_context` + `invoke` so option types, callbacks, and `exists` checks still run. Parent the leaf under `scaffold → <resource>` (not under `apply`) so usage/help matches direct CLI invocation (e.g. `scaffold app create`, not `scaffold apply PATH create`).
4. On the first failing step, stop and exit non-zero. Later steps are not run. With `--dry-run`, steps are not invoked, so underlying command failures cannot occur.

Apply does not call `*CreateCommand` (or other domain command classes) directly; it reuses the existing Click handlers and their side effects.

## Implementation

| Piece | Location |
|-------|----------|
| CLI entry | `stoobly_agent/app/cli/scaffold_cli.py` (`scaffold apply`) |
| Load / validate / execute | `stoobly_agent/app/cli/scaffold/apply_command.py` |
| Tests | `stoobly_agent/test/app/cli/scaffold/apply_test.py` |

## Errors

Config validation errors (missing/unsupported `version`, missing `commands`, unknown resource/action/option, invalid `acceptedValues`, missing required args, action that is a group, etc.) are listed in [scaffold-yml.md](scaffold-yml.md#validation-errors). Validation runs up front; if it fails, no steps are invoked.

| Condition | Result |
|-----------|--------|
| `PATH` missing or not a file | Non-zero exit (Click path check) |
| Unreadable / empty / non-mapping / unparseable config | Exit 1 |
| Config validation failure | Exit 1; no steps run |
| Underlying command failure (e.g. Click validation on invoke) | Stop; exit with that command’s exit code; later steps not run |

## Test coverage

`apply_test.py` locks in:

| Area | Assertions |
|------|------------|
| Help | `scaffold apply --help` exits 0 and documents `PATH` |
| Happy path | Ordered `app create` then `service create`; services and scaffold namespace exist afterward |
| Logging | `applying app create <name>` / `applying service create <name>`; option flags not present in output |
| Dry-run | `--dry-run` logs `would apply …`, exits 0, and does not create scaffold artifacts |
| JSON | `--format json` applies a JSON config |
| Validation | Missing/unsupported version; missing `commands` / `resource`; unknown resource/action/option; invalid accepted value; missing required argument; action that is a group |
| Missing file | Non-existent `PATH` exits non-zero |
| Usage path | On invoke failure, usage shows `scaffold app create` (not nested under `apply`) |
