---
name: root-cause-debugging
description: Use when a bug, test failure, build failure, integration failure, flaky behavior, performance regression, incident, or unexpected behavior appears. Before fixing, build a feedback loop, reproduce the reported failure, trace the failure boundary, compare working patterns, form falsifiable hypotheses, instrument one variable at a time, fix the root cause, add regression coverage, and prove the original scenario is fixed. 한국어: 버그, 테스트 실패, 빌드 실패, 통합 실패, flaky 동작, 성능 저하, 장애, 예상 밖 동작이 나타났을 때 사용한다. 수정 전에 피드백 루프를 만들고, 보고된 실패를 재현하고, 실패 경계를 추적하고, 정상 패턴과 비교하고, 반증 가능한 가설을 세우고, 한 번에 하나의 변수만 계측하고, root cause를 고치고, 회귀 커버리지를 추가하고, 원래 시나리오가 고쳐졌음을 증명한다.
---

# Root-Cause Debugging

Debug by evidence, not by plausible fixes.

This is a technique skill. Follow the phases in order unless you can explicitly prove a phase is already satisfied. If a shortcut feels obvious, treat that as a signal to slow down and gather evidence.

## Non-Negotiables

```text
NO FIX BEFORE ROOT CAUSE.
NO ROOT CAUSE WITHOUT REPRODUCTION.
NO COMPLETION WITHOUT THE ORIGINAL SCENARIO PASSING.
```

Never patch the symptom first. Do not add retries, timeouts, fallbacks, warning suppression, config changes, broad refactors, or “while here” cleanup until the failure has been reproduced and the cause is supported by evidence.

## Supporting References

Keep this file as the operating checklist. Open the supporting files only when that technique is relevant:

- `references/feedback-loops.md` — choosing and sharpening the reproduction loop.
- `references/root-cause-tracing.md` — tracing bad values, state, and component boundaries back to the source.
- `references/condition-based-waiting.md` — using fake timers first, then condition-based waits when real async work must complete.
- `references/defense-in-depth.md` — adding layered guards after the source is known.
- `references/scripts/hitl-loop.template.sh` — structuring unavoidable manual reproduction.
- `references/scripts/find-polluter.template.sh` — isolating tests or commands that create unwanted state.

## Use When

Use this for:

- failing tests, flaky tests, or polluted test state
- build failures and CI-only failures
- runtime exceptions, wrong output, missing data, broken UI, or unexpected state
- integration failures across services, queues, jobs, CI, auth, storage, deploys, or external APIs
- performance regressions, hangs, timeouts, memory growth, or resource surges
- failures that already survived one attempted fix
- any moment where “it is probably X” appears before proof

Pressure does not relax the process. Pressure is when shortcut fixes do the most damage.

## Phase 1 — Build the Feedback Loop

Create an agent-runnable pass/fail signal for the user-reported failure. The loop must reach the real failing path, not a nearby surrogate.

Prefer loops in this order:

1. Failing unit, integration, or end-to-end test at the correct seam.
2. Focused command or CLI invocation with fixture input and checked output.
3. HTTP script against a local, staging, or test server.
4. Browser automation that asserts DOM, console, and network behavior.
5. Replay of a captured request, event, payload, trace, log, or fixture.
6. Throwaway harness that calls the real code path with minimal setup.
7. Stress loop for flaky, timing, or concurrency failures.
8. Differential loop comparing working vs broken, old vs new, or config A vs B.
9. Bisection loop for commit ranges, data ranges, dependency versions, or polluting tests.
10. Human-in-the-loop prompt script only when a manual step is unavoidable.

Improve the loop before trusting it:

- **Fast**: remove unrelated setup and narrow the path.
- **Sharp**: assert the exact symptom, not “did not crash.”
- **Deterministic**: pin time, seed randomness, isolate filesystem, freeze network, control concurrency.

For flaky bugs, first raise the reproduction rate. Loop more often, parallelize, add stress, inject timing pressure, or isolate the race until the failure is common enough to reason about.

If no loop is possible, stop and state exactly what artifact or access is missing: environment access, logs, trace, core dump, HAR file, screen recording with timestamps, captured payload, or permission for temporary instrumentation.

Use `references/feedback-loops.md` when choosing between test, CLI, HTTP, browser, replay, stress, differential, bisection, or manual loops.

## Phase 2 — Reproduce and Observe

Run the loop. Watch the failure happen.

Capture evidence before moving on:

- exact error message, stack trace, status code, wrong value, missing event, bad state, screenshot, request/response, query result, timing, memory profile, or log excerpt
- whether the failure matches the user-reported symptom
- whether it reproduces consistently, or at what rate if flaky
- recent changes: commits, dependency changes, config changes, data migrations, environment differences, deploys, feature flags

Read errors and warnings completely. Stack traces, codes, and line numbers are often the shortest path to the root cause.

Do not debug a different failure because it is easier to reproduce.

## Phase 3 — Trace the Failure Boundary

Find the first point where expected behavior becomes actual bad behavior.

For a deep stack failure, trace backward:

```text
symptom
  ↑ immediate failing operation
  ↑ caller and arguments
  ↑ earlier transformation
  ↑ source of invalid state or assumption
```

At every step ask:

```text
Where did this bad value/state come from?
Was it already bad before this function/component touched it?
What caller, config, environment, lifecycle event, or persisted state made it bad?
```

For multi-component failures, inspect each boundary:

```text
component A ──payload/config/state──▶ boundary ──payload/config/state──▶ component B
              expected? actual?                  expected? actual?
```

Record at each boundary:

- input and output
- visible config and environment
- state read and state written
- ordering and lifecycle assumptions
- where the data first diverged

When similar working code exists, compare it before fixing. List all differences in behavior, configuration, dependencies, ordering, environment, data shape, lifecycle, and ownership. Do not discard a difference until evidence rules it out.

Fix the source of the bad state, not the line where it finally explodes.

Use `references/root-cause-tracing.md` when the failure appears deep in a stack, crosses components, or requires working-vs-broken comparison.

## Phase 4 — Form Ranked Hypotheses

Before testing any fix, write 3–5 ranked hypotheses.

Each hypothesis must be falsifiable:

```text
If <cause> is true, then <probe> will show <observable result>.
```

Good hypotheses name a mechanism and a prediction:

```text
If the cache key omits locale, then a fr-FR request followed by en-US will reuse the same key. Logging cache read/write keys with locale will show identical keys for both requests.
```

Test one hypothesis at a time. One probe, one variable, one result.

If a hypothesis fails, record what the failure ruled out and form the next hypothesis. Do not stack fixes.

If three fix attempts fail, stop treating the issue as a local bug. Re-question the design: hidden coupling, shared mutable state, invalid ownership, missing seam, or a fundamentally wrong pattern may be the root cause.

If you do not understand a piece of the system, say so and inspect it. Do not pretend confidence.

## Phase 5 — Instrument Precisely

Instrumentation must answer a hypothesis from Phase 4.

Prefer:

1. debugger, REPL, profiler, query plan, trace viewer, or runtime inspector
2. targeted boundary logs that distinguish hypotheses
3. temporary assertions at the first violated invariant

Every temporary diagnostic log must have a unique cleanup prefix, for example `[DEBUG-a4f2]`.

Do not “log everything and search later.” Noise is not evidence.

Use specialized probes when relevant:

- **Performance regression**: establish baseline and current measurements; use profiler output, query plans, allocation data, timing harnesses, or regression bisection.
- **Flaky waiting**: use fake timers/virtual clocks first when behavior is timer-driven; otherwise wait for the condition that matters, not a guessed sleep. Use fixed sleeps only when elapsed time itself is the behavior under test and document why.
- **State pollution**: isolate the polluter with bisection across tests, inputs, or lifecycle steps.
- **External/manual step**: drive the human with a structured prompt loop and capture exact answers as machine-readable output.

Use `references/condition-based-waiting.md` for timer-driven tests, flaky async waits, and the fake-timer vs polling decision. Use `references/scripts/find-polluter.template.sh` for state pollution and `references/scripts/hitl-loop.template.sh` for unavoidable manual reproduction.

## Phase 6 — Fix the Root Cause

Before changing production code, create a failing regression test if a correct seam exists.

A correct seam exercises the real chain that triggered the bug. A shallow test that cannot hit the triggering path is false confidence.

If no correct seam exists, document that finding. The architecture is preventing this bug from being locked down.

Then:

1. Watch the regression test fail, or run the captured repro if no test seam exists.
2. Make the smallest source-level change that addresses the confirmed root cause.
3. Do not bundle unrelated refactors, cleanup, retries, fallbacks, broad validation, or behavior changes.
4. If invalid data crosses multiple layers, add defense-in-depth only after the source is known: boundary validation, domain invariant, environment guard, or permanent observability must each catch a distinct failure mode.
5. Re-run the original unminimized feedback loop.

Use `references/defense-in-depth.md` before adding layered validation, guards, or permanent observability.

A fix that only masks the crash point is incomplete.

## Phase 7 — Prove, Clean Up, Report

Before declaring done, verify:

- original feedback loop passes
- regression test passes, or missing test seam is explicitly documented
- original user-described scenario was exercised
- relevant nearby checks still pass
- all temporary `[DEBUG-...]` instrumentation is removed
- throwaway harnesses are deleted or clearly marked as debug artifacts

Report in this shape:

```md
## Root Cause

## Evidence

## Fix

## Regression Coverage

## Verification

## Remaining Risk
```

Do not say the issue is fixed if the original scenario was not re-run.

## Red Flags

If any of these happen, return to the earliest violated phase:

- “It is probably X; I will just fix it.”
- “Try one quick change and see.”
- “Add a retry, timeout, or fallback before tracing.”
- “Suppress the warning or error.”
- “Change several things, then run tests.”
- “The test passed, but it was not the reported failure.”
- “I do not know why it worked.”
- “One more fix attempt” after repeated failed fixes.
- “The reference pattern is long; I skimmed enough.”
- “The working example differs, but that cannot matter.”

These are not minor style issues. They are how bugs survive.
