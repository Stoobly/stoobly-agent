# Lifecycle Hooks by Intercept Mode

This document lists lifecycle hooks called for each intercept mode, in call order.

## `record` mode

### Standard path (no fixture match)

1. `handle_before_request`
2. `handle_before_develop`
3. `handle_after_develop`
4. `handle_before_record`
5. `handle_after_record`
6. `handle_before_response`

### Fixture / public-dir match path

When `fixtures.yml` or the `public` directory matches the request, the agent short-circuits upstream and recording and follows the mock success lifecycle instead:

1. `handle_before_request`
2. `handle_before_develop`
3. `handle_before_mock`
4. `handle_after_develop`
5. `handle_after_mock`
6. `handle_before_response`

Notes:
- `record` mode reuses develop request/response handling, so develop hooks run before record (or mock) hooks.
- Fixture matching uses the same [`eval_fixtures`](../stoobly_agent/app/proxy/mock/eval_fixtures_service.py) logic as mock mode (`fixtures.yml`, then `public`). There is no DB mock lookup on the record path.
- `handle_before_mock` runs only after a fixture match; unmatched record traffic does not fire mock hooks.
- Matched fixture responses set `X-Stoobly-Fixture-Path`; the response phase uses that to divert to mock hooks and skip upload.

## `mock` mode

1. `handle_before_request`
2. `handle_before_develop`
3. `handle_before_mock`
4. `handle_after_develop`
5. `handle_after_mock`
6. `handle_before_response`

Notes:
- `handle_after_mock_not_found` may also run when no mock match is found. It is a specialized hook, not part of the standard success path above.

## `develop` mode

1. `handle_before_request`
2. `handle_before_develop`
3. `handle_after_develop`
4. `handle_before_response`

## `test` mode

Standard `test_policy=found` path:

1. `handle_before_request`
2. `handle_before_develop`
3. `handle_after_develop`
4. `handle_before_mock`
5. `handle_after_mock`
6. `handle_before_test`
7. `handle_after_test`
8. `handle_before_response`

Notes:
- Additional `record` hooks (`handle_before_record`, `handle_after_record`) can run during test result upload flows (non-standard/conditional path).
- With `test_policy=none`, develop/test hooks are skipped and the flow is handled by mock logic.
