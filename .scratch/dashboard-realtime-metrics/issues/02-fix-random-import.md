# 02 — Fix Python Random Module Import

## What to build
Backend generates valid random metrics without `AttributeError` when the endpoint is called.

## Acceptance criteria
- [ ] Import statement correctly accesses `random.randint` and `random.uniform`
- [ ] No `AttributeError: 'builtin_function_or_method' object has no attribute 'randint'` errors
- [ ] Endpoints return valid JSON responses

## Blocked by
None — can start immediately (can be done in parallel with 01)