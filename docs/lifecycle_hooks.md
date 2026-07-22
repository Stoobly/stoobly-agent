# Lifecycle Hooks by Intercept Mode

This document lists lifecycle hooks called for each intercept mode, in call order.

## `record` mode

1. `handle_before_request`
2. `handle_before_develop`
3. `handle_after_develop`
4. `handle_before_record`
5. `handle_after_record`
6. `handle_before_response`

Notes:
- `record` mode reuses develop request/response handling, so develop hooks run before record hooks.

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
