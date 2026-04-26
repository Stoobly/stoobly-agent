# Intercept Mode Test Matrix

This matrix summarizes behavior for test mode based on combinations of `test_policy` and `mock_policy`.

| Test policy | Mock policy | Mocks response | Tests | Returns live response | Follows mock flow exactly |
|---|---|---|---|---|---|
| `none` | `none` | Mock disabled in request phase. | No. | Yes. | Yes (normal mock handler behavior for `none`). |
| `none` | `found` | Mock if found; otherwise fallback upstream. | No. | Conditional. | Yes (normal `found` behavior). |
| `none` | `all` | Strict mock path. | No. | No. | Yes (normal `all` behavior). |
| `found` | `none` | Test path forces lookup with `mock=all` on copied flow. | Conditional (only when expected mock found). | Yes. | No (explicitly overrides incoming `none` to `all` for test evaluation). |
| `found` | `found` | Test path forces lookup with `mock=all` on active flow. | Conditional. | No. | No (does not keep `found`; coerces to `all`). |
| `found` | `all` | Test path uses `all` for expected-response lookup. | Conditional. | No. | No (test path still applies test side effects). |

## Notes

- Supported test policies: `none`, `found`.
- Supported mock policies: `none`, `found`, `all`.
- For `test_policy=found`, response handling forces `mock_policy=all` during expected-response lookup in the test path.
- "Follows mock flow exactly" means no test side effects; therefore it is only `Yes` when `test_policy=none`.
