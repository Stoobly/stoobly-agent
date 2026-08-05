# Scaffold apply config (`scaffold.yml`)

## Overview

Config file consumed by [`scaffold apply`](scaffold-apply.md). It declares an ordered list of scaffold CLI commands. Each step maps 1:1 to `stoobly-agent scaffold <resource> <action> …`.

Supported formats: **YAML** (default; often named `scaffold.yml`) and **JSON**.

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
| `action` | yes | Subcommand under that group (`create`, `up`, `copy`, …). |
| `options` | no | Mapping of options and positionals. Defaults to `{}`. |

`resource` + `action` are validated against [`scaffold.opencli.yaml`](../../stoobly_agent/app/cli/scaffold.opencli.yaml). Unknown resource/action, an action that is itself a group (not a leaf command), unknown option keys, invalid `acceptedValues`, or missing required options/arguments is an error. Steps are then invoked via the matching Click command.

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
      copy_on_workflow_up: true
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

  - resource: workflow
    action: up
    options:
      workflow_name: mock
      app_dir_path: ~/monorepo
      context_dir_path: ~/monorepo/apps/app-1
      log_level: warning
      dry_run: true
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
| Unknown option key (per OpenCLI) | Exit 1 (`Unknown options for command: …`) |
| Option value not in `acceptedValues` | Exit 1 (`Accepted values: …`) |
| Missing required option/argument | Exit 1 (`missing required option(s): …`) |
| Flag option given a non-boolean | Exit 1 |
