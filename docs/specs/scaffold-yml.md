# Scaffold apply config (`scaffold.yml`)

## Overview

Config file consumed by [`scaffold apply`](scaffold-apply.md). It declares an ordered list of scaffold CLI commands. Each step maps 1:1 to `stoobly-agent scaffold <resource> <action> …`.

Supported formats: **YAML** (default; often named `scaffold.yml`) and **JSON**. When `PATH` is omitted, apply reads the scaffold app’s `.stoobly/scaffold.yml` (`AppDataDir.scaffold_file_path`), falling back to the nearest context when no app exists yet.

## Schema (version 1)

### Top-level

| Key | Required | Description |
|-----|----------|-------------|
| `version` | yes | Schema version (integer). Currently only `1` is supported. |
| `commands` | yes | Non-empty ordered list of steps to run. |

Missing or unsupported `version`, missing `commands`, or an empty `commands` list is an error.

### Step

| Key | Required | Description |
|-----|----------|-------------|
| `resource` | yes | Scaffold command group (`app`, `service`, `workflow`, `hostname`, …). |
| `action` | yes | Subcommand under that group (`create`, `up`, `copy`, …). For nested groups, use a space-separated path to the leaf (for example `rewrite set` under `setting`). |
| `options` | no | Mapping of options and positionals. Defaults to `{}`. |

`resource` + `action` are validated against [`scaffold.opencli.yaml`](../../stoobly_agent/app/cli/scaffold.opencli.yaml). Unknown resource/action, an action that is itself a group (not a leaf command), a command that cannot be used with scaffold apply, unknown option keys, invalid `acceptedValues`, or missing required options/arguments is an error. Steps are then invoked via the matching Click command. Only commands that expose `--apply` may appear in an apply config.

A default config can be created with `stoobly-agent scaffold create`, which writes `.stoobly/scaffold.yml` in the current working directory only when it does not already exist.

`app`/`service`/`workflow` `create`, plus `setting` and `intercept` commands, write to `scaffold.yml` by default and only mutate scaffold files when `--apply` is set. `workflow copy` still mutates by default and skips recording when `--apply` is passed. Replaying via `scaffold apply` forces `--apply` so steps run and are never re-saved into the file.

`service update` and `service delete` always apply and do **not** support `--apply`. Instead of recording an `update`/`delete` step, they change the matching `service create` step: update merges options (creating a create step if missing; rename via `--name` updates `service_name`), and delete removes that create step.

Recording uses **upsert by identity** for some commands (matching step replaced in place); others still append. Updates round-trip `scaffold.yml` with comment-preserving YAML so existing comments and key order are kept:

| Commands | Identity |
|----------|----------|
| `app` / `service` / `workflow` `create` | name (`app_name` / `service_name` / `workflow_name`) |
| `setting` `filter set` / `match set` | action + `pattern` + `method` |
| `setting` `rewrite set` | action + `pattern` + `method` + `type` + `name` |
| `intercept` `enable` / `disable` / `set` | action + `workflow` (omitted `workflow` means all workflows) |

`workflow copy` and other recorded commands without a rule above still append.

### Options

Keys use **snake_case** matching Click parameter names (for example `app_dir_path`, `copy_on_workflow_up`).

| Kind | YAML / JSON shape |
|------|-------------------|
| Flag | boolean (`true` / `false`) |
| Single value | scalar |
| Multi-option (`multiple=True`) | list (a single scalar is also accepted and treated as one value) |
| Positional argument | key matching the argument name (`app_name`, `service_name`, `workflow_name`, …) |

Unknown option keys for the target command are an error.

### Path expansion

These option keys are treated as paths:

- `app_dir_path`
- `context_dir_path`
- `script_path`
- `ca_certs_dir_path`
- `certs_dir_path`
- `docker_socket_path`

For each:

1. Expand `~`.
2. If the path is still relative, resolve it against the **config file’s directory**.

Lists (for example multiple `context_dir_path` values) expand each entry.

### Directories

Apply does **not** create directories. Paths that existing commands require to exist (for example `context_dir_path` with `exists=True`) must already exist; otherwise the underlying command validation fails.

## Example

```yaml
version: 1
commands:
  - resource: app
    action: create
    options:
      app_name: monorepo
      app_dir_path: ~/monorepo
      context_dir_path:
        - ~/monorepo/apps/app-1
        - ~/monorepo/apps/app-2
      ui_port: 4201
      plugin: [playwright]

  - resource: service
    action: create
    options:
      service_name: dashboard
      app_dir_path: ~/monorepo
      context_dir_path:
        - ~/monorepo/apps/app-1
      hostname: local.stoobly.com
      scheme: http
      port: 80
      local: true

  - resource: service
    action: create
    options:
      service_name: google
      app_dir_path: ~/monorepo
      context_dir_path:
        - ~/monorepo/apps/app-1
        - ~/monorepo/apps/app-2
      env: [TEST]
      hostname: www.google.com
      scheme: https
      openapi_specification: true
      port: 443

  - resource: workflow
    action: create
    options:
      workflow_name: ci
      app_dir_path: ~/monorepo
      service: [google]
      template: mock

  - resource: service
    action: create
    options:
      service_name: assets
      app_dir_path: ~/monorepo
      hostname: http.badssl.com
      scheme: http
      port: 80
      detached: true
      workflow: [test]

```

## Validation errors

All of the following are checked **before** any step is invoked. Failures exit 1 with an error on stderr (via the apply logger).

| Condition | Result |
|-----------|--------|
| Missing / unreadable / empty / non-mapping config | Exit 1 with error message |
| Parse failure (invalid YAML/JSON) | Exit 1 with error message |
| Missing `version` | Exit 1 (`Missing required property: version`) |
| Unsupported `version` | Exit 1 (`Unsupported version: … Supported versions: …`) |
| Missing / empty `commands` | Exit 1 |
| Step missing `resource` or `action` | Exit 1 |
| Unknown resource or action (per OpenCLI) | Exit 1 (`Unknown resource` / `Unknown action`) |
| Action is a group, not a leaf command | Exit 1 (`… is a group, not a command`) |
| Command cannot be used with scaffold apply | Exit 1 (`cannot be used with scaffold apply`) |
| Unknown option key (per OpenCLI) | Exit 1 (`Unknown options for command: …`) |
| Option value not in `acceptedValues` | Exit 1 (`Accepted values: …`) |
| Missing required option/argument | Exit 1 (`missing required option(s): …`) |
| Flag option given a non-boolean | Exit 1 |
