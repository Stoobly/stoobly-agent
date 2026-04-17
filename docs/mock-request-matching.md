# Mock request matching

## Background

How an **incoming proxied request** is matched to a **recorded row** in the local DB for mocks: **hash-based** identity, optional **match rules** that drop hash dimensions, and optional **`compute`** to re-hash stored `raw` when **ignored components** change between record time and the retry path. Custom status codes: **`IGNORE_COMPONENTS = 498`**, **`NOT_FOUND = 499`** ([`custom_response_codes`](../stoobly_agent/app/proxy/constants/custom_response_codes.py)) — not standard HTTP 404/498.

### Remote project key and `compute`

When **local** + **remote project key**: **`compute='1'`** is attached only if **`retry`** and non-empty **`ignored_components`** after [`eval_request`](../stoobly_agent/app/proxy/mock/eval_request_service.py) ([`COMPUTE`](../stoobly_agent/config/constants/query_params.py)). That widens the ORM query and runs [`filter_requests_by_hashes`](../stoobly_agent/app/models/factories/resource/local_db/helpers/filter_requests_by_hashes_service.py) so stored **`raw`** is re-hashed with the same ignores as the live request.

### Hash dimensions

[`HashedRequestDecorator`](../stoobly_agent/app/proxy/mock/hashed_request_decorator.py): MD5 over **headers**, **query params** (multi-value), **body** as params or raw text per [`__build_request_params`](../stoobly_agent/app/proxy/mock/eval_request_service.py). Typed **ignored components** (`HEADER`, `QUERY_PARAM`, `BODY_PARAM`, …) exclude matching parts before hashing.

---

## Diagram: mock handler, ignored components, and `eval_request_with_retry`

[`eval_request_with_retry`](../stoobly_agent/app/proxy/handle_mock_service.py) merges **ignore rules** into `ignored_components` earlier in [`handle_request_mock_generic`](../stoobly_agent/app/proxy/handle_mock_service.py) (same list used for both attempts).

```mermaid
flowchart TB
  subgraph prep [Optional prep — handle_request_mock_generic]
    IG{ignore_rules non-empty?}
    IG -->|yes| MERGE[Merge rewrite → ignored_components]
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
    E2["eval_request(..., infer=infer, retry=1)"]
    APP --> E2
  end

  subgraph opt_retry [Options inside eval_request on retry]
    CP{Add COMPUTE=1?}
    CP -->|yes| WCOMP["COMPUTE=1: local resource AND remote project key AND retry option AND ignored_components non-empty"]
    CP -->|no| NOCOMP[Query without COMPUTE]
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

Supplements the diagram (not drawn above): **498** is “no row yet, but remote endpoint search returned suggested ignores” → [`IgnoreComponentsResponseBuilder`](../stoobly_agent/app/proxy/mock/ignored_components_response_builder.py) in [`request_adapter.response`](../stoobly_agent/app/models/factories/resource/local_db/request_adapter.py). **499** is the custom not-found response ([`CustomNotFoundResponseBuilder`](../stoobly_agent/app/proxy/mock/custom_not_found_response_builder.py)) for cases such as no usable match / no ignores from `endpoint_promise`, missing response row, or **invalid project or scenario key** before the DB path runs ([`eval_request`](../stoobly_agent/app/proxy/mock/eval_request_service.py)). If the **retry** response is still **498**, there is **no** third lookup. **`COMPUTE`** conditions and behavior are covered under [Remote project key and `compute`](#remote-project-key-and-compute) and in the diagram’s **Add COMPUTE=1?** branch. Outer mock policy **`FOUND`** may still **forward upstream** on **499** ([`handle_request_mock_generic`](../stoobly_agent/app/proxy/handle_mock_service.py)); lifecycle hooks and `pass_on` apply there.

---

## Diagram: local DB `response` when no `request_id`

```mermaid
flowchart TB
  Start[response kwargs]
  Col[request_columns copy strip internal keys]
  Snap[component_hashes from kwargs]
  Comp{compute equals 1?}
  Start --> Col --> Snap --> Comp
  Comp -->|no| ORM1[where_for with hash columns]
  ORM1 --> Rows1[rows]
  Comp -->|yes| Strip[drop hash keys from request_columns]
  Strip --> ORM2[where_for coarse only]
  ORM2 --> Rows2[candidates]
  Rows2 --> Res[endpoint_promise to ignored_components]
  Res --> Filt[filter_requests_by_hashes on raw]
  Filt --> Rows3[rows]
  Rows1 --> Pick[pick row or scenario tiebreak]
  Rows3 --> Pick
  Pick --> Got{row found?}
  Got -->|yes| OK[transform stored response]
  Got -->|no| NFD[handle_request_not_found]
  NFD --> EP2{endpoint_promise yields ignores?}
  EP2 -->|yes| R498[498 IgnoreComponentsResponseBuilder]
  EP2 -->|no| R499[499 CustomNotFoundResponseBuilder]
```

---

## Primary code references

| Concern | Location |
|--------|----------|
| Mock entry, retry, fixtures | [`handle_mock_service.py`](../stoobly_agent/app/proxy/handle_mock_service.py) |
| Query / hashes / match rules / `compute` | [`eval_request_service.py`](../stoobly_agent/app/proxy/mock/eval_request_service.py) |
| Local DB lookup, strip columns, not found 498/499 | [`request_adapter.py`](../stoobly_agent/app/models/factories/resource/local_db/request_adapter.py) |
| Candidate filtering | [`filter_requests_by_hashes_service.py`](../stoobly_agent/app/models/factories/resource/local_db/helpers/filter_requests_by_hashes_service.py) |
| Hashing | [`hashed_request_decorator.py`](../stoobly_agent/app/proxy/mock/hashed_request_decorator.py) |
