---
name: test-driven-development
description: "Use when implementing any feature, bug fix, refactor, behavior change, public API, CLI flow, UI behavior, or regression fix before writing production code. 기능, 버그수정, 리팩터링, 동작변경, 공개 API, CLI, UI, 회귀 수정 구현 전에."
---

# Test-Driven Development

Build behavior one verified slice at a time.

## Non-Negotiables

```text
NO PRODUCTION CODE BEFORE A FAILING TEST.
NO GREEN WITHOUT WATCHING RED FAIL FOR THE RIGHT REASON.
NO REFACTOR WHILE RED.
```

If production code was written first, do not keep adapting it as “reference.” Remove it from the path and restart from a failing test.

## Supporting References

Keep this file as the operating checklist. Open supporting references when the topic appears:

- `references/test-quality.md` — behavior tests, public interfaces, and bad test smells.
- `references/mocking-guidelines.md` — when to mock and how not to test mocks.
- `references/interface-design.md` — designing public interfaces that are easy to test and use.
- `references/refactoring.md` — cleanup after green without changing behavior.

## Use When

Use this for:

- new features
- bug fixes
- behavior changes
- refactors that need safety
- new public APIs or command/UI flows
- edge cases discovered during implementation

For a bug with unknown root cause, use root-cause debugging first to reproduce and identify the cause. Then use TDD to lock the fix with a failing regression test.

## Phase 0 — Choose One Behavior

Before writing the test, name exactly one externally observable behavior.

Good behavior statements:

- “rejects empty email”
- “returns cached result until the TTL expires”
- “shows validation errors without submitting the form”
- “retries a transient failure three times, then returns success”

Avoid implementation statements:

- “calls `validateEmail`”
- “sets `isValid` to false”
- “invokes payment service with cart total”

If the public interface is unclear, design the smallest interface the test should use. Prefer small surface area and real caller vocabulary.

Use `references/interface-design.md` when the test is hard to write because the interface is hard to use.

## Phase 1 — RED: Write One Failing Test

Write one minimal test for one behavior through the public interface.

Rules:

- one behavior per test
- test name describes what the caller/user observes
- use real code paths where practical
- mock only system boundaries, not internal collaborators
- assertion proves the behavior, not the implementation path

Run the specific test and watch it fail.

Confirm:

- it fails, not passes
- it fails for the expected reason
- it fails because behavior is missing, not because the test has a typo, bad setup, or wrong import

If it passes immediately, the test is not proving new behavior. Fix the test or choose the next missing behavior.

Use `references/test-quality.md` and `references/mocking-guidelines.md` before adding mocks or test utilities.

## Phase 2 — GREEN: Minimal Production Code

Write the smallest production change that makes the current failing test pass.

Do not add:

- future options
- generalized configuration
- unrelated validation
- speculative branches
- refactors outside the current path
- extra behavior not demanded by the current test

Run the same test and watch it pass.

If it fails, fix production code, not the test, unless the RED failure was wrong.

Then run the directly affected tests needed to catch local regressions.

## Phase 3 — REFACTOR: Improve While Green

Refactor only after the test is green.

Allowed:

- remove duplication
- improve names
- extract helpers behind the same public interface
- simplify conditionals
- deepen modules by hiding complexity behind a smaller interface
- move logic to where the data or responsibility belongs

Not allowed:

- changing behavior without a new failing test
- broad cleanup unrelated to the tested behavior
- changing tests to match implementation details

Run tests after each refactor step or small batch. If anything turns red, stop refactoring and restore green.

Use `references/refactoring.md` for cleanup candidates.

## Phase 4 — Repeat Vertically

Do not write all tests first, then all implementation.

Use vertical slices:

```text
RED test 1 → GREEN code 1 → REFACTOR
RED test 2 → GREEN code 2 → REFACTOR
RED test 3 → GREEN code 3 → REFACTOR
```

Each next test should reflect what was learned from the previous cycle.

## Completion Checklist

Before declaring the work complete:

- every new behavior has a test
- each test was seen failing for the expected reason before implementation
- tests exercise public behavior, not private implementation
- mocks are only at system boundaries and are not the subject of assertions
- edge cases and error paths relevant to the behavior are covered
- production code contains no test-only methods or test-only branches
- all temporary scaffolding is removed
- directly affected tests pass

## Red Flags

If any of these happen, stop and return to RED:

- implementation before test
- test passes immediately
- cannot explain why the test failed
- test name describes implementation, not behavior
- mocking internal collaborators
- asserting that a mock was called instead of asserting behavior
- adding test-only production methods
- mock setup larger than the behavior being tested
- refactoring while red
- adding “just in case” options or branches
- writing a batch of tests before any implementation

These are not style issues. They are how tests stop protecting behavior.
