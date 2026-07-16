# Mock request matching

## Background

How an **incoming proxied request** is matched to a **recorded row** in the local DB for mocks: **endpoint identity** (host / path / port / method), optional **hash dimensions** enabled by **match-rule allowlists**, **scenario tiebreak** when multiple rows remain, and optional **`compute`** to re-hash stored `raw` when **ignored components** change between record time and the retry path. Custom status codes: **`IGNORE_COMPONENTS = 498`**, **`NOT_FOUND = 499`** ([`custom_response_codes`](../stoobly_agent/app/proxy/constants/custom_response_codes.py)) — not standard HTTP 404/498.

### Endpoint lookup and `compute`

When mocking against **local DB**, [`eval_request`](../stoobly_agent/app/proxy/mock/eval_request_service.py) may attach an `endpoint_promise` from either:

- remote project endpoint search via [`search_endpoint`](../stoobly_agent/app/proxy/mock/search_endpoint.py), or
- OpenAPI endpoint search via [`search_open_api_endpoint`](../stoobly_agent/app/proxy/mock/search_open_api_endpoint.py).

If `endpoint_promise` exists, and the request is on **retry** with non-empty ignored components, **`compute='1'`** is attached ([`COMPUTE`](../stoobly_agent/config/constants/query_params.py)). That widens the ORM query and runs [`filter_requests_by_hashes`](../stoobly_agent/app/models/factories/resource/local_db/helpers/filter_requests_by_hashes_service.py) so stored **`raw`** is re-hashed with the same ignores as the live request.

### Endpoint cache behavior (remote + OpenAPI)

[`endpoint_cache`](../stoobly_agent/app/proxy/mock/endpoint_cache.py) is a singleton used by both search paths. It:

- caches parsed OpenAPI specs by normalized absolute path,
- caches remote endpoint index calls by `(project_id, index_params)`,
- merges both layers into one endpoint-id map, where **latest merge wins** on ID collisions,
- returns OpenAPI-derived ignored components from optional/nondeterministic fields (query/header/body/response-header),
- prefetches remote endpoints from settings when remote mode is enabled.

### Hash dimensions

[`HashedRequestDecorator`](../stoobly_agent/app/proxy/mock/hashed_request_decorator.py): MD5 over **headers**, **query params** (multi-value), **body** as params or raw text per [`__build_request_params`](../stoobly_agent/app/proxy/mock/eval_request_service.py). Typed **ignored components** (`HEADER`, `QUERY_PARAM`, `BODY_PARAM`, …) exclude matching parts before hashing.

Hashes are always **computed**, but only dimensions **kept** by a match rule are passed to the ORM lookup (see below).

### Match rules (component allowlists)

Match rules are **allowlists**, not denylists. [`__matched_components`](../stoobly_agent/app/proxy/mock/eval_request_service.py) starts with every hash dimension **off** (`Header`, `Query Param`, `Body Param` → `False`). For each rule whose **method** and **URL pattern** match the live request, the rule’s `components` list becomes the keep set (**last matching rule wins**; rules do not merge).

| Situation | Hash columns sent to ORM | Live tiebreak params |
|-----------|--------------------------|----------------------|
| **No** matching rule (default) | None — identity is host / path / port / method only | Live query params + headers (when present) |
| Rule lists e.g. `Query Param` | Only `query_params_hash` | Live headers only (query already hashed) |
| Rule lists all three components | All component hashes | None (exact hash already distinguishes) |

[`__filter_by_match_rules`](../stoobly_agent/app/proxy/mock/eval_request_service.py) deletes hashes for dimensions not kept. The same keep set drives [`__build_tiebreak_params`](../stoobly_agent/app/proxy/mock/eval_request_service.py):

- Dimension **not** kept → attach live value for fuzzy overlap (`QUERY_PARAMS` / `HEADERS`). Body is never scored in tiebreak—only hashed when allowlisted.
- Dimension **kept** → skip the corresponding live param (exact hash already distinguishes candidates).

### Scenario tiebreak

When local DB lookup returns **multiple** rows for a scenario, [`tiebreak_scenario_request`](../stoobly_agent/app/models/factories/resource/local_db/helpers/tiebreak_scenario_request.py) picks one:

1. Score candidates by live query-param overlap (if `QUERY_PARAMS` present); unique best score wins.
2. Else score by live header overlap (if `HEADERS` present); unique best score wins.
3. Else fall back to session order (next request after last served id; candidates are ordered by `id` ascending).

Without a scenario, multiple matches resolve to the **highest id** (most recent).

---

## Diagram: mock handler, ignored components, and `eval_request_with_retry`

[`eval_request_with_retry`](../stoobly_agent/app/proxy/handle_mock_service.py) merges **ignore rules** into `ignored_components` earlier in [`handle_request_mock_generic`](../stoobly_agent/app/proxy/handle_mock_service.py) (same list used for both attempts).

```mermaid
flowchart TB
  subgraph prep [Optional prep — handle_request_mock_generic]
    IG{ignore_rules non-empty?}
    IG -->|yes| MERGE[Merge ignore rules → ignored_components]
    IG -->|no| IG0[Use ignored_components as-is]
    MERGE --> INIT
    IG0 --> INIT
    INIT["infer ← bool options.infer<br/>used only on retry path"]
  end

  INIT --> E1["eval_request(request, ignored_components)"]

  E1 --> K1{kwargs include retry?}
  K1 -->|no — first call| D498{status 498?}

  subgraph retry_once [Retry at most once — only after 498]
    APP[Append res.content to ignored_components]
    E2["eval_request(..., retry=1)"]
    APP --> E2
  end

  subgraph opt_retry [Options inside eval_request on retry]
    CP{Add compute=1?}
    CP -->|yes| WCOMP["compute=1: local resource AND endpoint_promise AND retry AND len(ignored_components) > 0"]
    CP -->|no| NOCOMP[Query without compute]
    WCOMP --> RES2[response]
    NOCOMP --> RES2
  end

  E2 --> CP

  D498 -->|yes| APP
  D498 -->|no| RES1[res from first attempt]

  RES1 --> D499
  RES2 --> D499

  D499{status 499?}

  D499 -->|yes| EF["eval_fixtures(...)"]
  D499 -->|no| OUT[Return res]

  EF --> FX{fixture returned?}
  FX -->|yes| USEFX[res ← fixture]
  FX -->|no| KEEP499[Keep 499 response]
  USEFX --> OUT
  KEEP499 --> OUT
```

---

## Diagram: local DB `response` when no `request_id`

[`LocalDBRequestAdapter.response`](../stoobly_agent/app/models/factories/resource/local_db/request_adapter.py) reads **`retry`** from `query_params` (used only when **no row** matches). **`COMPUTE`** is stripped from ORM columns in [`__filter_request_response_columns`](../stoobly_agent/app/models/factories/resource/local_db/request_adapter.py).

```mermaid
flowchart TB
  Start[response kwargs]
  Col[request_columns copy strip internal keys]
  Snap[component_hashes from kwargs]
  Comp{COMPUTE equals 1?}
  Start --> Col --> Snap --> Comp
  Comp -->|no| ORM1["where_for + order_by(id asc)"]
  ORM1 --> Rows1[rows as list]
  Comp -->|yes| Strip[drop component hash keys from request_columns]
  Strip --> ORM2["where_for coarse + order_by(id asc)"]
  ORM2 --> Rows2[candidates]
  Rows2 --> IG[ignored_components from ENDPOINT_PROMISE]
  IG --> CF{ignored_components non-empty?}
  CF -->|yes| Filt[filter_requests_by_hashes on raw]
  CF -->|no| Rows3[rows]
  Filt --> Rows3[rows]
  Rows1 --> Multi
  Rows3 --> Multi
  Multi{multiple rows and scenario_id?}
  Multi -->|yes| TB["tiebreak_scenario_request<br/>1. live query params score<br/>2. live headers score<br/>3. session order"]
  Multi -->|no| Last[last row = highest id, or none]
  TB --> Got
  Last --> Got
  Got{row found?}
  Got -->|yes| OK[transform stored response]
  Got -->|no| NFD[no matching row]
  NFD --> RY{retry truthy?}
  RY -->|yes| R499[499 CustomNotFoundResponseBuilder]
  RY -->|no| EP2{not retry AND component hashes exist AND endpoint yields ignores?}
  EP2 -->|yes| R498[498 IgnoreComponentsResponseBuilder]
  EP2 -->|no| R499
```

---

## Diagram: match rules → hashes and live tiebreak params

Inside [`eval_request`](../stoobly_agent/app/proxy/mock/eval_request_service.py), before calling `request_model.response`. Keep flags default **off**; a matching rule’s `components` are an **allowlist** (last match wins).

```mermaid
flowchart TB
  Build["build request hashes + optional params"]
  Keep["__matched_components<br/>default all false; matching rule allowlists keep dims"]
  Build --> Keep
  Keep --> TB["__build_tiebreak_params"]
  TB --> QP{query param kept?}
  QP -->|no| LQP[attach QUERY_PARAMS]
  QP -->|yes| SkipQ[skip live query params]
  TB --> HD{header kept?}
  HD -->|no| LH[attach HEADERS]
  HD -->|yes| SkipH[skip live headers]
  LQP --> Filter
  SkipQ --> Filter
  LH --> Filter
  SkipH --> Filter
  Filter["__filter_by_match_rules<br/>drop hashes for dimensions not allowlisted"]
  Filter --> Resp[request_model.response]
```

---

## Primary code references

| Concern | Location |
|--------|----------|
| Mock entry, retry, fixtures | [`handle_mock_service.py`](../stoobly_agent/app/proxy/handle_mock_service.py) |
| Query / hashes / match rules / live tiebreak params / `compute` | [`eval_request_service.py`](../stoobly_agent/app/proxy/mock/eval_request_service.py) |
| Endpoint cache + OpenAPI ignored-component derivation | [`endpoint_cache.py`](../stoobly_agent/app/proxy/mock/endpoint_cache.py) |
| Remote endpoint search adapter | [`search_endpoint.py`](../stoobly_agent/app/proxy/mock/search_endpoint.py) |
| OpenAPI endpoint search adapter | [`search_open_api_endpoint.py`](../stoobly_agent/app/proxy/mock/search_open_api_endpoint.py) |
| Local DB lookup, strip columns, not found 498/499 | [`request_adapter.py`](../stoobly_agent/app/models/factories/resource/local_db/request_adapter.py) |
| Scenario multi-row tiebreak | [`tiebreak_scenario_request.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/tiebreak_scenario_request.py) |
| Candidate filtering | [`filter_requests_by_hashes_service.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/filter_requests_by_hashes_service.py) |
| Hashing | [`hashed_request_decorator.py`](../stoobly_agent/app/proxy/mock/hashed_request_decorator.py) |
