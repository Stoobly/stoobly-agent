# Scaffold `.env` behavior

This document describes how environment variables are loaded and merged for scaffold workflows across three entry points:

- **Local** — `stoobly-agent scaffold workflow …` with a local (non-Docker) runtime
- **Docker CLI** — the same commands when the app is configured with `--runtime docker`
- **Docker Makefile** — generated app Makefile targets such as `make record`, `make test/up`, etc.

## `.env` file locations

Scaffold uses three distinct `.env` files. They serve different purposes and are merged at different stages.

| File | Path | Created by |
|------|------|------------|
| **App dotenv** | `{app_dir}/.stoobly/services/.env` | `scaffold app create --env NAME=VALUE` |
| **Namespace dotenv** | `{app_dir}/.stoobly/tmp/{namespace}/.env` | Copied from the project `.env` (see below) |
| **Workflow dotenv** | `{app_dir}/.stoobly/services/{service}/{workflow}/.env` | Generated on `workflow up` by `write_env()` |

`App.dotenv_path` resolves the app dotenv path (`services/.env`).

The namespace defaults to the workflow name (for example `record`, `test`) unless `--namespace` is set.

## User-visible sources

These are the sources you control. Priority numbers below are **1 = highest**. Fold order into the generated workflow `.env` still determines priority when those sources are not read again at runtime.

| Source | How you set it | Stored / applied as |
|--------|----------------|---------------------|
| **Shell env vars** | `export NAME=VALUE` before running a command | Current process environment |
| **App create env vars** | `scaffold app create --env NAME=VALUE` | Env vars written to `{app_dir}/.stoobly/services/.env` |
| **`STOOBLY_DOTENV_FILE` env var** | Project `.env` file, or `export STOOBLY_DOTENV_FILE=/path/to/.env` | File copied to `{app_dir}/.stoobly/tmp/{namespace}/.env` |
| **Generated workflow `.env`** | Written automatically on `workflow up` | Env vars in `{app_dir}/.stoobly/services/{service}/{workflow}/.env` |

The generated workflow `.env` also includes scaffold-computed env vars (for example `APP_DIR`, `CONTEXT_DIR`, `WORKFLOW_NAME`, `SERVICE_DNS`) as a base layer. You do not edit that file by hand — it is regenerated on each `workflow up`.

### Other sources

| Source | When it applies |
|--------|-----------------|
| **`STOOBLY_APP_DIR` / `STOOBLY_CONTEXT_DIR` env vars** | Always set by the agent on local subprocesses (`exec_command`), regardless of the sources above |
| **CLI flags** | Options such as `--app-dir-path` and `--context-dir-path` determine path values before env merging |
| **Compose `environment:`** | Inside Docker containers, an explicit `environment:` entry overrides the same env var from `env_file` |
| **Docker Compose interpolation** | For `${VAR}` in compose YAML on the host, shell env vars win over compose project `.env` (Docker Compose default) |

Not every source participates at every stage. The tables below show which sources apply for each entry point. Priority `1` is highest.

---

## Writing the workflow `.env` (`write_env`)

On `workflow up`, the agent writes the workflow dotenv. Shell env vars are not involved. Fold order:

| Priority | Source |
|----------|--------|
| 1 | Env vars from **`STOOBLY_DOTENV_FILE`** (namespace copy at `.stoobly/tmp/{namespace}/.env`) |
| 2 | Env vars from **app create** (`services/.env`, from `--env NAME=VALUE`) |
| 3 | **Generated scaffold env vars** (for example `APP_DIR`, `CONTEXT_DIR`, `WORKFLOW_NAME`, `SERVICE_DNS`) |

The result is the **generated workflow `.env`** file. Docker Compose loads those env vars via `env_file`. Local and container init/run scripts also source the file.

---

## Local workflow (CLI)

**Command example:**

```bash
stoobly-agent scaffold workflow up record --app-dir-path .
```

### Namespace dotenv bootstrap

When a workflow run command starts, `WorkflowNamespace.copy_dotenv()` copies a project `.env` into the namespace directory if it exists:

- Source: path from the **`STOOBLY_DOTENV_FILE`** env var, or `.env` in the current working directory if unset
- Destination: `{app_dir}/.stoobly/tmp/{namespace}/.env`

### On `workflow up`

1. `write_env()` writes the workflow dotenv (merge order above).
2. Service init/run scripts source `./.env` in the workflow directory (`set -a; . ./.env; set +a`), exporting those env vars into the script.
3. `LocalWorkflowRunCommand.exec_command()` builds the subprocess environment:
   - Start from shell env vars (`os.environ`)
   - Fill in missing keys from the **workflow dotenv** env vars
   - Force **`STOOBLY_APP_DIR`** and **`STOOBLY_CONTEXT_DIR`**
   - Apply any explicit `env=` kwargs last

### Precedence (local host subprocess)

At subprocess exec time, shell env vars win over the generated workflow `.env`. Values already folded into that file keep the fold order from `write_env()`:

| Priority | Source |
|----------|--------|
| 1 | **`STOOBLY_APP_DIR` / `STOOBLY_CONTEXT_DIR` env vars** (set by agent) |
| 2 | **Shell env vars** |
| 3 | Env vars from **`STOOBLY_DOTENV_FILE`** (folded into generated workflow `.env`) |
| 4 | Env vars from **app create** (`services/.env`) (folded into generated workflow `.env`) |
| 5 | **Generated scaffold env vars** (base of generated workflow `.env`) |

Local init/run scripts source the generated workflow `.env` directly (`set -a; . ./.env`). In that script context there is no prior shell export, so priorities 3–5 apply as written in the file.

---

## Docker with CLI

**Command example:**

```bash
stoobly-agent scaffold workflow up record --app-dir-path . --runtime docker
```

### Namespace dotenv bootstrap

Same as local: `copy_dotenv()` on command init copies the file from **`STOOBLY_DOTENV_FILE`** (or cwd `.env`) → namespace dotenv.

### On `workflow up`

1. `write_env()` writes the workflow dotenv (same merge order as local).
2. `exec_setup()` builds the Stoobly base image on the host using `merged_app_env()`:
   - Shell env vars win over app create env vars (`services/.env`)
   - Used for build-arg env vars such as **`STOOBLY_IMAGE`**
3. Docker Compose starts services with `env_file` pointing at the **workflow dotenv**.
4. Init/run scripts inside containers source `./.env` in the workflow directory.

### Precedence by layer

**Host process (image build):**

Only shell env vars and app create env vars participate. Env vars from **`STOOBLY_DOTENV_FILE`** and the generated workflow `.env` are not read at build time.

| Priority | Source |
|----------|--------|
| 1 | **Shell env vars** |
| 2 | Env vars from **app create** (`services/.env`) (fills unset keys only) |

**Docker Compose file interpolation** (`${VAR}` in compose YAML):

| Priority | Source |
|----------|--------|
| 1 | **Shell env vars** |
| 2 | Env vars from compose project `.env` (Docker Compose default; not a Stoobly-managed file) |

**Inside containers** (via compose `env_file` and workflow init scripts):

Shell env vars are not applied inside containers unless compose references a host variable. App create env vars and env vars from **`STOOBLY_DOTENV_FILE`** participate through their fold order into the generated workflow `.env`:

| Priority | Source |
|----------|--------|
| 1 | Env vars from **Compose `environment:`** (explicit per-service entry) |
| 2 | Env vars from **`STOOBLY_DOTENV_FILE`** (folded into generated workflow `.env`) |
| 3 | Env vars from **app create** (`services/.env`) (folded into generated workflow `.env`) |
| 4 | **Generated scaffold env vars** (base of generated workflow `.env`) |

---

## Docker with Makefile

**Command example:**

```bash
make -f .stoobly/services/.Makefile record
```

The generated Makefile lives at `{app_dir}/.stoobly/services/.Makefile`.

### Makefile-specific env vars

| Env var | Default | Purpose |
|---------|---------|---------|
| `STOOBLY_DOTENV_FILE` | `.env` (cwd) | Path to dotenv file copied to namespace dotenv |
| `STOOBLY_APP_DIR` | Makefile parent dirs | Application root |
| `STOOBLY_CONTEXT_DIR` | Same as app dir default | Context directory |
| `STOOBLY_IMAGE` | (unset) | Base image build arg |
| `STOOBLY_IMAGE_USE_LOCAL` | (unset) | When set, skips `--pull` on image build |

App dotenv path in the Makefile:

```
{app_dir}/.stoobly/services/.env
```

### Namespace dotenv (`dotenv` target)

Before `workflow/up` and `workflow/down`, the Makefile runs the `dotenv` target:

```makefile
dotenv: workflow/namespace
	@if [ -f "$(dotenv_file)" ]; then cp "$(dotenv_file)" $(workflow_namespace_dir)/.env; fi
```

This copies the file pointed to by the **`STOOBLY_DOTENV_FILE`** env var (default: cwd `.env`) to
`{app_dir}/.stoobly/tmp/{namespace}/.env`.

Equivalent to the CLI `copy_dotenv()` step, but driven by the Makefile before each workflow command.

### Host image build (`stoobly_app_dotenv`)

Before `docker compose run`, the Makefile builds the Stoobly base image:

```makefile
stoobly_app_dotenv=_saved=$$(export -p); set -a; if [ -f "$(app_dotenv_file)" ]; then . "$(app_dotenv_file)"; fi; set +a; eval "$$_saved"
```

This sources app dotenv (`services/.env`) and then restores the original shell exports, so **shell env vars win** over app create env vars — matching `merged_app_env()` in the CLI.

Build-arg env vars such as **`STOOBLY_IMAGE`** and **`STOOBLY_IMAGE_USE_LOCAL`** come from the resulting environment.

### Workflow execution

1. `workflow/up` depends on `dotenv` (namespace copy).
2. `stoobly_exec` runs `docker compose run` inside the Stoobly UI container.
3. The container executes `stoobly-agent scaffold workflow up …`, which follows the **Docker CLI** path above (`write_env`, compose `env_file`, etc.).

### Precedence by layer

**Host process (image build via `stoobly_app_dotenv`):**

Only shell env vars and app create env vars participate. Env vars from **`STOOBLY_DOTENV_FILE`** and the generated workflow `.env` are not read at build time. The Makefile sources app dotenv then restores original shell exports, so shell wins — matching `merged_app_env()` in the CLI.

| Priority | Source |
|----------|--------|
| 1 | **Shell env vars** |
| 2 | Env vars from **app create** (`services/.env`) (fills unset keys only) |

**Docker Compose file interpolation** (`${VAR}` in compose YAML):

| Priority | Source |
|----------|--------|
| 1 | **Shell env vars** |
| 2 | Env vars from compose project `.env` (Docker Compose default; not a Stoobly-managed file) |

**Inside containers** (via compose `env_file` and workflow init scripts):

After `stoobly_exec`, the container runs `stoobly-agent scaffold workflow up …` on the Docker CLI path. Shell env vars are not applied inside containers unless compose references a host variable. App create env vars and env vars from **`STOOBLY_DOTENV_FILE`** participate through their fold order into the generated workflow `.env` (namespace copy happens earlier via the Makefile `dotenv` target):

| Priority | Source |
|----------|--------|
| 1 | Env vars from **Compose `environment:`** (explicit per-service entry) |
| 2 | Env vars from **`STOOBLY_DOTENV_FILE`** (folded into generated workflow `.env`) |
| 3 | Env vars from **app create** (`services/.env`) (folded into generated workflow `.env`) |
| 4 | **Generated scaffold env vars** (base of generated workflow `.env`) |

---

## Quick reference

### Where to put variables

| Goal | Where to set it |
|------|-----------------|
| Persistent app defaults from scaffold create | `scaffold app create --env NAME=VALUE` → env vars in `services/.env` |
| Per-project overrides (copied each workflow run) | cwd `.env`, or set **`STOOBLY_DOTENV_FILE`** to another path → namespace dotenv |
| One-off override for a single command | `export NAME=VALUE` in shell before running |
| Workflow/runtime config (generated) | Env vars written to `services/{service}/{workflow}/.env` on up — do not edit by hand |

### Precedence summary

Priority `1` is highest. Folded sources keep their fold order inside the generated workflow `.env`.

| Stage | Order (priority 1 first) |
|-------|--------------------------|
| Host subprocess (local) | 1 `STOOBLY_APP_DIR` / `STOOBLY_CONTEXT_DIR` → 2 Shell env vars → 3 env vars from `STOOBLY_DOTENV_FILE` → 4 app create env vars → 5 generated scaffold env vars |
| Host image build (Docker CLI / Makefile) | 1 Shell env vars → 2 app create env vars |
| Writing workflow `.env` (`write_env`) | 1 env vars from `STOOBLY_DOTENV_FILE` → 2 app create env vars → 3 generated scaffold env vars |
| Inside Docker containers | 1 Compose `environment:` env vars → 2 env vars from `STOOBLY_DOTENV_FILE` → 3 app create env vars → 4 generated scaffold env vars |
| Compose YAML interpolation | 1 Shell env vars → 2 compose project `.env` env vars |

---

## Related commands

```bash
# Create app dotenv entries
stoobly-agent scaffold app create my-app --env STOOBLY_IMAGE=stoobly/agent:1.0.0

# Local workflow
stoobly-agent scaffold workflow up record --app-dir-path .

# Docker workflow (CLI)
stoobly-agent scaffold workflow up record --app-dir-path . --runtime docker

# Docker workflow (Makefile)
make -f .stoobly/services/.Makefile record
```
