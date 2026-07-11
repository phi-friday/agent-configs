# Feedback Loops

A debugging loop is an agent-runnable pass/fail signal for the reported failure. Build this before changing code.

## Loop Choices

Use the narrowest loop that still reaches the real failing path.

| Situation | Preferred loop |
|---|---|
| Pure function or domain behavior | Unit test at the real call seam |
| Cross-module behavior | Integration test |
| UI behavior | Browser automation asserting DOM, console, and network |
| API behavior | HTTP script with fixed request and checked response |
| CLI behavior | Command with fixture input and checked stdout/stderr/files |
| Production-only payload | Replay captured request/event/log/trace through the same path |
| Timing or concurrency issue | Stress loop that raises reproduction rate |
| Regression window exists | Bisection loop over commits, versions, configs, or data |
| Manual action unavoidable | Structured human-in-the-loop script that captures answers |

## Quality Bar

A usable loop is:

- **Real**: reproduces the user-reported failure, not a nearby failure.
- **Sharp**: asserts the specific symptom.
- **Repeatable**: can run multiple times without hidden manual state.
- **Fast enough**: narrow enough to run after each hypothesis.
- **Inspectable**: captures the symptom when it fails.
- **Phase-advance safe**: before moving to the next phase, one fixed command and exact-symptom assertion demonstrate RED before the fix and can be rerun unchanged to confirm GREEN after the fix.
- **Pressure-capable when flaky**: the same command repeats the trigger enough to establish reproducible RED and a measured reproduction rate.

## Completion Contract

For every failure, this is the minimum contract:

1. Keep one command with a fixed exact-symptom assertion.
2. Confirm that command and assertion produce RED on the reported symptom before diagnosis.
3. After RED, reduce the repro one axis at a time when useful: input, caller, config, data, steps. Preserve the original command and scenario.
4. Rerun each reduced repro with the same exact-symptom assertion; keep a reduction only while it still produces RED.
5. Use the minimized repro for hypothesis work only.
6. Re-run the **same fixed assertion** on the original **unminimized** command as the final proving GREEN signal.

For flaky failures, step 2 must use the pressure-capable command repeatedly enough to establish reproducible RED and record the reproduction rate.

## Flaky Failures

For nondeterministic failures, first raise the reproduction rate.

Try:

- run the trigger many times in one command
- run cases in parallel when safe
- add load or timing pressure
- isolate filesystem, network, clock, and shared state
- log event ordering with a unique debug prefix
- reduce unrelated setup that hides timing

A 50% failure is debuggable. A 1% failure usually needs a better loop first.

## When No Loop Exists

Do not guess. State exactly what is missing:

- environment access
- captured payload, request, HAR file, log, trace, core dump, or screen recording with timestamps
- permission to add temporary instrumentation
- credentials or external system access required to reproduce
