# Snapshot create

How `request snapshot create` and `scenario snapshot create` write snapshot files under `.stoobly/snapshots/` and append history events.

## Commands

```bash
stoobly-agent request snapshot create [--action PUT|DELETE] [--decode] <request_key>
stoobly-agent scenario snapshot create [--action PUT|DELETE] [--decode] <scenario_key>
```

Default `--action` is `PUT` (write/replace). `DELETE` removes snapshot files (when safe) and appends a delete event.

## High-level flow

```mermaid
flowchart TD
  cli[CLI snapshot create] --> prompt[prepare_snapshot_write_format]
  prompt -->|none or v2| v2[write format v2]
  prompt -->|v1 + confirm migrate| migrate[migrate_snapshots_to_v2]
  migrate --> v2
  prompt -->|v1 + decline / non-interactive| v1[write format v1]
  v2 --> write[snapshot_request / snapshot_scenario]
  v1 --> write
  write --> files[Write snapshot files]
  write --> history[Append history event]
  write --> post[update_request_snapshots verify/hooks]
```

1. CLI handler validates the key and loads the ORM request/scenario.
2. [`prepare_snapshot_write_format`](../stoobly_agent/app/cli/helpers/snapshot_format_prompt.py) picks **v1** or **v2** (and may migrate).
3. Facade → model → [`snapshot_request`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_service.py) / [`snapshot_scenario`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_service.py) writes files and appends a log event.
4. CLI runs [`update_request_snapshots`](../stoobly_agent/app/cli/helpers/update_request_snapshots_service.py) on the returned path (optional lifecycle hooks / verify). Prints request snapshot path(s).

## Format detection and write policy

Implemented in [`snapshot_format.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_format.py).

| Detected on disk | Meaning |
|------------------|---------|
| **v2** | Any `requests/*/*.http` or `scenarios/*.yaml` |
| **v1** | Any `requests/<2-char>/<uuid>` (no `.http`) or extensionless `scenarios/<uuid>` |
| **none** | Empty / no recognizable snapshot files |

Write policy:

| Detected | Create writes |
|----------|----------------|
| none or v2 | **v2** |
| v1 | **v1**, unless interactive create confirms migrate → then migrate tree and write **v2** |
| v1 + non-TTY / `--yes`-style non-interactive | stay on **v1** (no silent migrate) |

Readers always accept both formats.

## Request snapshot create (`PUT`)

Orchestration: [`snapshot_request`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_service.py).

1. Resolve write format; for v2 build slug via [`build_request_slug`](../stoobly_agent/app/models/factories/resource/local_db/helpers/request_slug.py): `{METHOD}-{path-with-/-as--}` (path only, no query). Example: `GET` + `/api/users/1` → `GET-api-users-1`.
2. Backup existing snapshot file (for rollback if log append fails).
3. Write snapshot bytes from ORM via `JoinedRequestStringAdapter`.
4. Append history event via `Log.put(request)`.
5. Return snapshot file path.

### v2 on-disk layout

```
.stoobly/snapshots/requests/<METHOD>-<path-slug>/
  <uuid>.http
  bodies/<sha256>
```

- `.http` is the existing joined control + raw HTTP request/response (monkey delimiter), **without** bodies.
- Non-empty bodies are written under `bodies/<content-hash>`.
- Last header on that HTTP message is `X-Stoobly-Body-Ref: bodies/<hash>` ([`body_ref.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/body_ref.py)).
- On read, bodies are reconstituted so apply/diff/list still see full joined bytes.

### v1 on-disk layout (unchanged)

```
.stoobly/snapshots/requests/<uuid[0:2]>/<uuid>
```

Single extensionless file of joined request+response with bodies inline.

### History line (request)

Space-delimited under `snapshots/history/`:

```
<event-uuid> request <locator> PUT <ms>
```

| Format | `<locator>` |
|--------|-------------|
| v2 | `GET-api-users/<request-uuid>` |
| v1 / legacy | `<request-uuid>` |

Apply uses the locator for O(1) file resolve; collapse/ORM identity is always the UUID suffix (`resource_id`).

## Scenario snapshot create (`PUT`)

Orchestration: [`snapshot_scenario`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_service.py).

1. Resolve write format; construct `ScenarioSnapshot` with scenario name.
2. Backup metadata (and later request payloads).
3. Write metadata, remove previous request snapshots that are no longer referenced (respecting shared refs via scenario inverted index), write current requests.
4. Append `Log.put(scenario)`.
5. Return metadata path.

### v2 on-disk layout

```
.stoobly/snapshots/scenarios/<sanitized-name>.yaml
.stoobly/snapshots/requests/<METHOD>-<path-slug>/
  <uuid>.http
  bodies/<sha256>
```

YAML fields:

```yaml
uuid: <scenario-uuid>
description: <str>
requests:
  - GET-api-users/<request-uuid>.http
```

Request entries are relative paths under `snapshots/requests/` (order preserved).

### v1 on-disk layout (unchanged)

```
.stoobly/snapshots/scenarios/<scenario-uuid>              # JSON {name, description}
.stoobly/snapshots/scenarios/requests/<scenario-uuid>     # newline-joined request UUIDs
.stoobly/snapshots/requests/<uuid[0:2]>/<uuid>            # request bodies
```

### History line (scenario)

```
<event-uuid> scenario <locator> PUT <ms>
```

| Format | `<locator>` |
|--------|-------------|
| v2 | `<sanitized-name>/<scenario-uuid>` |
| v1 / legacy | `<scenario-uuid>` |

## Delete action

`--action DELETE`:

- **Request:** remove file only if no scenario still references it; always append a DELETE history event.
- **Scenario:** remove its request snapshots (unless still referenced elsewhere), remove metadata, append DELETE history event.

Request snapshot backup/rollback still applies around the log append for request create.

## After create: verify / hooks

Both CLIs call `update_request_snapshots` with the written path and `with_snapshot=False` (does not append another history event). That path:

- Resolves request vs scenario from the file path (v1 or v2 naming).
- Optionally verifies/normalizes raw joined content.
- Optionally runs lifecycle hooks when `--lifecycle-hooks-path` is set.

## Related paths

| Path | Role |
|------|------|
| `snapshots/history/` | Append-only event shards |
| `snapshots/log` | Locked/committed event copy (gitignored) |
| `snapshots/VERSION` | Apply cursor (processed **event** UUIDs), not storage schema version |

Legacy `.uuid-index` dirs may exist under older v2 trees for uuid-only history lines; new creates rely on history locators instead.

## Key source files

| File | Role |
|------|------|
| [`request_cli.py`](../stoobly_agent/app/cli/request_cli.py) / [`scenario_cli.py`](../stoobly_agent/app/cli/scenario_cli.py) | CLI entrypoints |
| [`snapshot_format_prompt.py`](../stoobly_agent/app/cli/helpers/snapshot_format_prompt.py) | Migrate prompt + write format |
| [`snapshot_service.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_service.py) | Create/delete orchestration |
| [`request_snapshot.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/request_snapshot.py) | Request file I/O |
| [`scenario_snapshot.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/scenario_snapshot.py) | Scenario metadata + request list I/O |
| [`log_event.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/log_event.py) | History serialize/parse + locators |
| [`body_ref.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/body_ref.py) | v2 body externalize/reconstitute |
| [`snapshot_migrate.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_migrate.py) | v1 → v2 one-shot migrate |
