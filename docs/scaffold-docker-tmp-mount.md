# Scaffold Docker: `.stoobly/tmp` mount (APP_DIR vs CONTEXT_DIR)

This document explains how the scaffold workflow uses `tmp` under `.stoobly`, how host paths are resolved, and what to consider when mounting `${APP_DIR}/.stoobly/tmp` into containers (for example at `/home/stoobly/.stoobly/tmp`) alongside the broader `${CONTEXT_DIR}/.stoobly` mount.

## Background

In `.docker-compose.base.yml`, services typically mount:

- `${CONTEXT_DIR}/.stoobly:/home/stoobly/.stoobly`

A repo has one **APP_DIR** (application / scaffold root) but may use multiple **CONTEXT_DIR** values (Stoobly data directories). Host-side scaffold code does **not** always write temporary workflow state under `CONTEXT_DIR`; it writes under **APP_DIR**’s data directory. Aligning the container mount with that behavior avoids subtle mismatches.

## What lives in `tmp`

All paths below use `DataDir` resolved from the `App` constructor path. For non-containerized `scaffold workflow up`, that path is **`app_dir_path` (APP_DIR)**. Therefore:

**Host canonical location:** `APP_DIR/.stoobly/tmp/`

| Component | Path / behavior |
|-----------|-----------------|
| **Context lock** (`context_lock.py`) | `.{md5(CONTEXT_DIR)}.access` and `.{md5(CONTEXT_DIR)}.lock` — keyed by **host context directory**, not by namespace |
| **Workflow namespace** (`workflow_namespace.py`) | `APP_DIR/.stoobly/tmp/{namespace}/` — `.env`, `run.sh`, `nameservers`, `traefik.yml`, `.timestamp`, `.pid`, logs |
| **Active workflow scan** (`docker/local` `workflow/run_command.py`) | Scans subdirectories of `app.data_dir.tmp_dir_path` for `.timestamp` files to detect conflicting runs |

The Makefile template aligns with this: `app_tmp_dir=$(app_data_dir)/tmp` where `app_data_dir` is under `app_dir`.

## Why an explicit `APP_DIR` tmp mount helps

If only `${CONTEXT_DIR}/.stoobly` is mounted:

- When **CONTEXT_DIR == APP_DIR** (default), `tmp` inside the container matches where the CLI writes on the host.
- When **CONTEXT_DIR ≠ APP_DIR**, the CLI still writes workflow state to **`APP_DIR/.stoobly/tmp`**, while the container sees **`CONTEXT_DIR/.stoobly/tmp`**. Those can diverge.

Adding a bind mount such as:

```text
${APP_DIR}/.stoobly/tmp:/home/stoobly/.stoobly/tmp
```

after (or as an override to) the broad `.stoobly` mount ensures the container’s `/home/stoobly/.stoobly/tmp` matches the host paths the scaffold actually uses.

*(Exact compose ordering and merge semantics depend on your Docker Compose version; the last matching mount for a given path wins.)*

## Parallel `workflow up` with different `--namespace` values

### Namespace directories

Each run uses `APP_DIR/.stoobly/tmp/{namespace}/`. Different namespaces → separate `.env`, scripts, and marker files. Parallel runs with **distinct namespaces** do not collide on those files.

### Access / lock files

Filenames include `md5(CONTEXT_DIR)`:

- Different **CONTEXT_DIR** → different `.access` / `.lock` files → independent access counts per context (as intended for coordinating operations that must run once per context).
- Same **CONTEXT_DIR** → shared access file → coordinated count across parallel runs on that context.

See the section **`.access` file: conflicts and the tmp mount** below for a fuller analysis.

### Active workflow detection

The runner scans all namespace subfolders under `tmp` for `.timestamp` files. For another run with the **same workflow name** but a **different namespace**, the implementation allows coexistence (same workflow name is not treated as a hard conflict in that check). Namespaces are the primary knob for parallel isolation.

## Constraint: namespace uniqueness per APP_DIR

With a single shared `APP_DIR/.stoobly/tmp/`, the **namespace** must be unique among **concurrent** workflow runs that share the same **APP_DIR**, even if they use **different CONTEXT_DIR** values.

If two runs use the **same `--namespace`** but **different `--context-dir-path`**, they target the same directory `APP_DIR/.stoobly/tmp/{namespace}/` and can overwrite each other’s `.env` and related files. That was less of an issue when each context had its own `CONTEXT_DIR/.stoobly/tmp/` tree; with APP_DIR–centralized `tmp`, operators should treat namespace as **globally unique per app** for parallel work.

## `options.json`: conflicts and the tmp mount

`mitmproxy_options_json_path` resolves to `{data_dir}/tmp/options.json` — a flat file in the tmp root, **not** inside a namespace subdirectory. It is written by the mitmproxy proxy process running **inside the container** via `MitmproxyConfig.dump()`, and deleted by the **host** `scaffold workflow down --containerized` (`scaffold_cli.py:517`). This makes it a cross-boundary file: container writes, host deletes.

### Conflict table

| Scenario | Old mount (CONTEXT_DIR only) | New mount (+ APP_DIR/tmp) |
|----------|------------------------------|---------------------------|
| **CONTEXT_DIR == APP_DIR** (default) | Parallel containers already share `CONTEXT_DIR/.stoobly/tmp/options.json` — conflict pre-existed | No change |
| **Different CONTEXT_DIRs, same APP_DIR** | Each container writes to its own `CONTEXT_DIR/.stoobly/tmp/options.json` — no conflict | All containers write to `APP_DIR/.stoobly/tmp/options.json` — **new conflict introduced** |

### What `options.json` contains

`MitmproxyConfig.dump()` is called at **agent startup** (`run.py`), immediately after applying all CLI arguments. It writes the full mitmproxy options snapshot for that run — every key mitmproxy knows about, including `listen_host`, `listen_port`, `mode`, `confdir`, `ssl_insecure`, `block_global`, `scripts`, `upstream_cert`, `certs`, `connection_strategy`, etc.

Notably, this is a **write-only-at-startup** operation. The file is not read back to initialize the agent; the agent already has all options in memory from CLI args.

### What actually gets read back

Only one key is ever retrieved via `MitmproxyConfig.get()`:

- **`ssl_insecure`** — read by `replay_request_service.py` and `proxy_controller.py` to decide whether to skip upstream TLS verification.

`get()` falls back to reading the file **only when `__master` is `None`** (no live mitmproxy instance). During a running workflow, the singleton has a live master and reads from in-memory `master.options` directly, never from disk.

### Practical impact

Because `options.json` is overwritten fresh at every agent startup from CLI args and the only value read back (`ssl_insecure`) is typically consistent across runs sharing the same APP_DIR, **the conflict risk is very low in practice**. A clobber would only matter if a container's API or replay code ran `get('ssl_insecure')` without a live master while a parallel container had already overwritten the file with a different `ssl_insecure` value — a narrow edge case.

### Mitigation

`options.json` is the one file in `tmp` that is not namespace-scoped. Moving it into the namespace subdirectory (alongside `.env`, `run.sh`, etc.) would fully isolate parallel runs. Until then, if parallel workflows use **different CONTEXT_DIRs** under the same APP_DIR with `--containerized`, they share this file.

### Other tmp files during container runtime

| File | Location | Conflict risk |
|------|----------|---------------|
| Overwrite lock files (`overwrite_scenario_service.py`) | `tmp/.{scenario_id}_{hash}.overwrite.lock` | Keyed by scenario ID + hash; `FileLock` serializes any overlap — safe |
| Request logs (`scaffold_logger.py`) | `tmp/{namespace}/logs/{workflow}.requests.json` | Namespace-scoped — no conflict with distinct namespaces |

---

## `.access` file: conflicts and the tmp mount

### Who reads and writes it

The `.access` file (and companion `.lock`) are used only on the **host** during scaffold workflow commands (`context_lock.py`). Before `docker compose` runs, the host calls `access()` / `access_count()`; the resulting count is written into workflow `.env` as `WORKFLOW_ACCESS_COUNT` (`workflow_run_command.py` → `write_env`). **Containers do not read `.access` directly** — they receive the value via environment variables.

### Filename collisions between parallel runs

Paths are `APP_DIR/.stoobly/tmp/.{md5(CONTEXT_DIR)}.access` (and `.lock`).

| Scenario | Result |
|----------|--------|
| **Different `--context-dir-path`** | Different `md5(CONTEXT_DIR)` → **different filenames** → no collision; each context has its own access tracking. |
| **Same CONTEXT_DIR, different `--namespace`** | **Same filename** → **intentional** shared coordination for “how many workflow instances are using this Stoobly data directory?” |

So parallel runs with different namespaces do **not** conflict on `.access` because of namespace; they share or split `.access` **only** based on whether `CONTEXT_DIR` matches.

### Concurrent host processes on the same file

`access()`, `access_count()`, and `release()` use `filelock.FileLock` on `.{hash}.lock` before reading or writing `.access`, so multiple host processes touching the **same** `.access` file serialize correctly.

### Does binding `APP_DIR/.stoobly/tmp` introduce new `.access` conflicts?

**No.** The host always wrote `.access` under `APP_DIR/.stoobly/tmp` (via `app.data_dir.tmp_dir_path`). Adding an explicit bind mount only aligns the container’s `/home/stoobly/.stoobly/tmp` with that directory. It does not change how many processes write, which hashes are used, or lock behavior.

When `CONTEXT_DIR ≠ APP_DIR`, the **old** mount (`CONTEXT_DIR/.stoobly` only) could expose a **different** `tmp` tree in the container than the one the host updated; that mismatch did not create host-side `.access` races, but it meant the container filesystem was not the source of truth for host-written tmp state. The APP_DIR `tmp` mount fixes alignment; it does not add cross-process contention on `.access`.

## Summary

| Topic | Takeaway |
|-------|----------|
| **Where host writes `tmp`** | `APP_DIR/.stoobly/tmp` (via `app.data_dir.tmp_dir_path`) |
| **Mount alignment** | Bind `APP_DIR/.stoobly/tmp` into the container’s `.stoobly/tmp` when CONTEXT_DIR can differ from APP_DIR |
| **Parallel runs** | Use distinct `--namespace` values; access files remain per-CONTEXT_DIR via hash |
| **`.access` file** | Host-only; keyed by CONTEXT_DIR hash; `FileLock` on `.lock`; no new conflicts from the APP_DIR `tmp` mount |
| **`options.json`** | Written fresh at every agent startup; only `ssl_insecure` is ever read back, and only without a live master; conflict risk is very low in practice |
| **Gotcha** | Reusing the same namespace across different CONTEXT_DIRs in parallel can clobber shared namespace dir contents |
