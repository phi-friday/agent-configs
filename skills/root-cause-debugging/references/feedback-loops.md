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
