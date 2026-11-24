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
  cli[CLI snapshot create] --> prompt[get_snapshot_format]
  prompt -->|none or v2| v2[write format v2]
  prompt -->|v1 + confirm migrate| migrate[migrate_snapshots to v2]
  migrate --> v2
  prompt -->|v1 + decline / non-interactive| v1[write format v1]
  v2 --> write[snapshot_request / snapshot_scenario]
  v1 --> write
  write --> clazz[Instantiate RequestSnapshotV1/V2 or ScenarioSnapshotV1/V2]
  clazz --> files[Write snapshot files]
  write --> history[Append history event]
  write --> post[update_request_snapshots verify/hooks]
```

1. CLI handler validates the key and loads the ORM request/scenario.
2. [`get_snapshot_format`](../stoobly_agent/app/cli/helpers/snapshot_format_service.py) detects format **once** and picks **v1** or **v2** (and may migrate).
3. Facade → model → [`snapshot_request`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_service.py) / [`snapshot_scenario`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_service.py) constructs the matching **V1/V2** class, writes files, and appends a log event with the **same** `format` (no second disk scan).
4. CLI runs [`update_request_snapshots`](../stoobly_agent/app/cli/helpers/update_request_snapshots_service.py) on the returned path (optional lifecycle hooks / verify). Prints request snapshot path(s).

## Class hierarchy

Format-specific path and I/O live in subclasses. Shared behavior (ORM adapters, backup/rollback helpers, metadata API) stays on the base.

```mermaid
classDiagram
  Snapshot <|-- RequestSnapshot
  RequestSnapshot <|-- RequestSnapshotV1
  RequestSnapshot <|-- RequestSnapshotV2
  Snapshot <|-- ScenarioSnapshot
  ScenarioSnapshot <|-- ScenarioSnapshotV1
  ScenarioSnapshot <|-- ScenarioSnapshotV2
  LogEvent <|-- LogEventV1
  LogEvent <|-- LogEventV2

  class RequestSnapshot {
    +create(uuid, data_dir, slug, format)
    +FORMAT
    +write(request)
    +request
    +path
  }
  class RequestSnapshotV1 {
    path requests/ab/uuid
  }
  class RequestSnapshotV2 {
    +build_request_slug(method, path)
    +request_relative_path(slug, uuid)
    +parse_request_relative_path(path)
    path requests/slug/uuid.yaml
    bodies + headers + Body-Ref/Header-Ref
  }
  class ScenarioSnapshot {
    +create(uuid, data_dir, name, format)
    +write_metadata(scenario)
    +write_requests(scenario)
  }
  class ScenarioSnapshotV1 {
    JSON metadata + requests index
  }
  class ScenarioSnapshotV2 {
    +sanitize_scenario_filename(name)
    name.yaml + embedded request entries
  }
  class LogEvent {
    +create(line)
    +serialize_put / serialize_delete
    +request_locator / scenario_locator
  }
  class LogEventV1 {
    locator bare uuid
  }
  class LogEventV2 {
    locator slug/uuid or name/uuid
  }
```

| Role | How the class is chosen |
|------|-------------------------|
| **Create / delete write** ([`snapshot_service`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_service.py)) | Instantiates `RequestSnapshotV1` / `RequestSnapshotV2` or `ScenarioSnapshotV1` / `ScenarioSnapshotV2` from the resolved write format |
| **History append** ([`Log.put` / `Log.delete`](../stoobly_agent/app/models/factories/resource/local_db/helpers/log.py)) | Same `format` from create is passed through; `LogEvent.serialize_*` picks `LogEventV1` / `LogEventV2` without re-detecting. `resolve_write_format` remains a fallback when `format` is omitted |
| **Read / apply / list / diff** | `RequestSnapshot.create(...)` / `ScenarioSnapshot.create(...)` detect from disk (and prefer V2 when a history locator includes a slug/name); `LogEvent.create(line)` picks V1/V2 from locator shape |
| **Type checks** | e.g. `isinstance(snapshot, RequestSnapshotV2)` instead of comparing a format flag |

## Format detection and write policy

Implemented in [`snapshot_format.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_format.py).

| Detected on disk | Meaning |
|------------------|---------|
| **v2** | Any `requests/*/*.yaml` or `scenarios/*.yaml` |
| **v1** | Any `requests/<2-char>/<uuid>` (extensionless) or extensionless `scenarios/<uuid>` |
| **none** | Empty / no recognizable snapshot files |

Write policy:

| Detected | Create writes |
|----------|----------------|
| none or v2 | **v2** (`*SnapshotV2`) |
| v1 | **v1** (`*SnapshotV1`), unless interactive create confirms migrate → then migrate tree and write **v2** |
| v1 + non-TTY / `prompt=False` | stay on **v1** (no silent migrate) |

Readers always accept both formats via `.create()`.

## Request snapshot create (`PUT`)

Orchestration: [`snapshot_request`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_service.py).

1. Resolve write format.
2. Construct `RequestSnapshotV2` (with slug from [`RequestSnapshotV2.build_request_slug`](../stoobly_agent/app/models/factories/resource/local_db/helpers/request_snapshot.py)) or `RequestSnapshotV1`.
   - Slug: `{METHOD}-{path-with-/-as--}` (path only, no query). Example: `GET` + `/api/users/1` → `GET-api-users-1`.
3. Backup existing snapshot file (for rollback if log append fails).
4. `write(request)` — ORM → joined bytes via `JoinedRequestStringAdapter` (V2 externalizes bodies).
5. Append history event via `Log.put(request)`.
6. Return snapshot file path.

### v2 on-disk layout (`RequestSnapshotV2`)

```
.stoobly/snapshots/requests/<METHOD>-<path-slug>/
  <uuid>.yaml
  bodies/<hash16>
  headers/<hash16>
```

- `<uuid>.yaml` is a structured request entry (see [`yaml_adapter.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/yaml_adapter.py)); uuid is the filename, not a field:
  - request: `method`, `url`, `http_version`, `timestamp`, `headers` (YAML mapping)
  - nested `response`: `status`, `latency`, `http_version`, `timestamp`, `headers`
- Non-empty bodies are written under `bodies/<content-hash>` (16-char truncated SHA-256 hex).
- Dedup-list request/response headers are written under `headers/<content-hash>` ([`header_ref.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/header_ref.py)); missing dedup-list names are omitted.
- Refs in the YAML `headers` maps: `X-Stoobly-Header-Ref: headers/<hash>` and `X-Stoobly-Body-Ref: bodies/<hash>` ([`joined_request_ref.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/joined_request_ref.py)).
- On read, the entry is rebuilt into joined HTTP and headers/bodies are reconstituted so apply/diff/list still see full joined bytes.

### v1 on-disk layout (`RequestSnapshotV1`)

```
.stoobly/snapshots/requests/<uuid[0:2]>/<uuid>
```

Single extensionless file of joined request+response with bodies inline.

### History line (request)

Space-delimited under `snapshots/history/`:

| Format | Class | Line |
|--------|-------|------|
| v2 | `LogEventV2` | `<event-uuid> <ms> PUT request <locator>` |
| v1 / legacy | `LogEventV1` | `<event-uuid> request <locator> PUT <ms>` |

| Format | `<locator>` |
|--------|-------------|
| v2 | `GET-api-users/<request-uuid>` |
| v1 / legacy | `<request-uuid>` |

v2 puts `resource_id` last so it may contain spaces. Apply passes the locator into `RequestSnapshot.create(...)` for O(1) path resolve; collapse/ORM identity is always the UUID suffix (`resource_id`).

## Scenario snapshot create (`PUT`)

Orchestration: [`snapshot_scenario`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_service.py).

1. Resolve write format.
2. Construct `ScenarioSnapshotV2` (with scenario name) or `ScenarioSnapshotV1`.
3. Backup metadata (and later request payloads).
4. `write_metadata` / remove stale request snapshots (respecting shared refs via scenario inverted index) / `write_requests` (uses matching `RequestSnapshotV1` or `RequestSnapshotV2` for each request). On rename, v2 relocates `{old-stem}.yaml` → `{new-stem}.yaml` and removes the orphan (same idea as request slug changes).
5. Append `Log.put(scenario)`.
6. Return metadata path.

### v2 on-disk layout (`ScenarioSnapshotV2`)

```
.stoobly/snapshots/scenarios/<sanitized-name>.yaml   # collisions → name-2.yaml, …
.stoobly/snapshots/requests/<METHOD>-<path-slug>/
  bodies/<hash16>
  headers/<hash16>
```

YAML fields (requests are an **embedded** uuid-keyed dict of structured entries — no per-request `<uuid>.yaml` for scenario members; uuid is the dict key, not a field on the entry):

```yaml
uuid: <scenario-uuid>
description: <str>
requests:
  <request-uuid>:
    method: GET
    url: https://example.com/api
    http_version: "1.1"
    timestamp: ...
    headers: { ... }
    response:
      status: 200
      latency: ...
      http_version: "1.1"
      timestamp: ...
      headers: { ... }
```

Body/header files are still written under each request’s slug dir. Display name is the YAML stem (ORM names are required to equal the sanitized stem).

### v1 on-disk layout (`ScenarioSnapshotV1`)

```
.stoobly/snapshots/scenarios/<scenario-uuid>              # JSON {name, description}
.stoobly/snapshots/scenarios/requests/<scenario-uuid>     # newline-joined request UUIDs
.stoobly/snapshots/requests/<uuid[0:2]>/<uuid>            # request bodies
```

### History line (scenario)

| Format | Class | Line |
|--------|-------|------|
| v2 | `LogEventV2` | `<event-uuid> <ms> PUT scenario <locator>` |
| v1 / legacy | `LogEventV1` | `<event-uuid> scenario <locator> PUT <ms>` |

| Format | `<locator>` |
|--------|-------------|
| v2 | `<yaml-stem>/<scenario-uuid>` (stem is filesystem-safe name; spaces kept; `-2`, `-3`, … on collision) |
| v1 / legacy | `<scenario-uuid>` |

Apply passes the full locator into `ScenarioSnapshot.create(...)` for O(1) path resolve; collapse/ORM identity is the UUID suffix (`resource_id`), matching requests. DELETE apply passes `resource_id` (UUID) so it still works after the YAML is removed.

## Delete action

`--action DELETE`:

- **Request:** remove file only if no scenario still references it; always append a DELETE history event.
- **Scenario:** remove its request snapshots (unless still referenced elsewhere), remove metadata, append DELETE history event.

Request snapshot backup/rollback still applies around the log append for request create.

## After create: verify / hooks

Both CLIs call `update_request_snapshots` with the written path and `with_snapshot=False` (does not append another history event). That path:

- Resolves request vs scenario from the file path and builds the matching V1/V2 snapshot via `.create(..., format=...)`.
- Optionally verifies/normalizes raw joined content (V2 always re-externalizes on rewrite).
- Optionally runs lifecycle hooks when `--lifecycle-hooks-path` is set.

## Related paths

| Path | Role |
|------|------|
| `snapshots/history/` | Append-only event shards |
| `snapshots/log` | Locked/committed event copy (gitignored) |
| `snapshots/VERSION` | Apply cursor (processed **event** UUIDs), not storage schema version |

See also [snapshot migrate](snapshot-migrate.md).

## Key source files

| File | Role |
|------|------|
| [`request_cli.py`](../stoobly_agent/app/cli/request_cli.py) / [`scenario_cli.py`](../stoobly_agent/app/cli/scenario_cli.py) | CLI entrypoints |
| [`snapshot_format_service.py`](../stoobly_agent/app/cli/helpers/snapshot_format_service.py) | Migrate prompt + write format |
| [`snapshot_service.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_service.py) | Create/delete orchestration; constructs V1/V2 classes |
| [`request_snapshot.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/request_snapshot.py) | `RequestSnapshot` + `RequestSnapshotV1` / `RequestSnapshotV2` (locator parse + v2 naming helpers) |
| [`scenario_snapshot.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/scenario_snapshot.py) | `ScenarioSnapshot` + `ScenarioSnapshotV1` / `ScenarioSnapshotV2` (locator parse + v2 filename sanitize) |
| [`log_event.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/log_event.py) | `LogEvent` + `LogEventV1` / `LogEventV2` (locators); `.create()` / `.snapshot()` → snapshot `.create()` |
| [`body_ref.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/body_ref.py) | v2 body content-addressed storage |
| [`header_ref.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/header_ref.py) | v2 header content-addressed storage + dedup lists |
| [`joined_request_ref.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/joined_request_ref.py) | v2 joined-message externalize/reconstitute |
| [`snapshot_migrate.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/snapshot_migrate.py) | v1 ↔ v2 migrate ([docs](snapshot-migrate.md)) |
