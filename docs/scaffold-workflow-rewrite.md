# `scaffold workflow rewrite`

## What it does

`stoobly-agent scaffold workflow rewrite` syncs replay rewrite rules for services in a workflow.

For each selected service, if upstream URL components differ from the service URL (hostname, port, or scheme), the command upserts a rewrite rule so replay traffic is rewritten from the service URL to the upstream URL.

In practice, this keeps replay routing aligned with service-level `UPSTREAM_*` settings after scaffold config changes.

## Command

```bash
stoobly-agent scaffold workflow rewrite [OPTIONS] WORKFLOW_NAME
```

### Options

- `--app-dir-path TEXT` Path to application directory.
- `--containerized` Set if run from within a container.
- `--context-dir-path TEXT` Path to Stoobly data directory.
- `--service TEXT` Select specific services. Defaults to all services in the workflow.

## How rewrite rules are generated

For each service:

1. Resolve service URL from service config.
2. Compare service URL parts with effective upstream values.
3. If any of `hostname`, `port`, or `scheme` differs, persist a rewrite rule with:
   - pattern: `{service_url}/?.*?`
   - methods: `GET`, `PATCH`, `POST`, `PUT`, `DELETE`, `OPTIONS`
   - mode: `develop`
   - destination: upstream hostname/port/scheme

If a service has no URL, no rewrite rule is created for that service.

## Workflow template behavior

Rewrite rules are keyed by workflow template when a workflow is custom-templated.  
The command resolves template with:

- `workflow template` when present
- otherwise `WORKFLOW_NAME`

This means custom workflows inherit rewrite behavior from their template type.

## Docker test workflow exception

When runtime is Docker, local services in the `test` workflow are skipped.

This avoids adding replay rewrites for local test services where upstream hostname is expected to be `host.docker.internal`.

## Examples

Rewrite all services in the `record` workflow:

```bash
stoobly-agent scaffold workflow rewrite record
```

Rewrite one service only:

```bash
stoobly-agent scaffold workflow rewrite --service payments-api record
```

Run from a containerized context:

```bash
stoobly-agent scaffold workflow rewrite \
  --containerized \
  --context-dir-path /home/stoobly/.stoobly \
  record
```
