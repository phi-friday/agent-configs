# Task Decomposition

Parallel execution starts by proving tasks are independent.

## Independence Test

A task can run in parallel when all are true:

- it has a clear target file, artifact, subsystem, or failure group
- it can complete without another task's unfinished output
- it does not edit the same files as another task
- it does not change a shared contract another task depends on
- success can be reviewed independently
- final integration can be verified after all tasks return

If any answer is uncertain, sequence the tasks or split further.

## Grouping Patterns

Good parallel groups:

| Work | Split by |
|---|---|
| Failing tests | test file, feature area, or root-cause domain |
| Codebase investigation | subsystem or question |
| Mechanical edits | disjoint files or packages |
| Reviews | artifact, diff range, or concern type |
| Implementation | independent plan tasks with stable interfaces |

Bad parallel groups:

- multiple agents editing the same core module
- one agent defining types while another consumes those types
- several agents investigating symptoms that may share one root cause
- broad “fix all tests” tasks
- tasks with unclear ownership boundaries

## Sequencing Rules

Sequence when:

```text
Task B needs Task A's output to be correct.
Task A changes a public contract Task B consumes.
Tasks need the same file or migration.
One decision should govern all implementations.
```

Parallelize when:

```text
Tasks touch different files.
Tasks answer independent questions.
Tasks can coordinate through a small explicit contract.
Tasks only need final integration after completion.
```

## Fan-Out

Dispatch the full set of independent tasks together, up to the tool's concurrency boundary. Do not serialize independent work merely to keep a batch small.

Control integration risk with narrow assignments, explicit ownership, and the pre-flight conflict gate. Split into later waves only for real dependencies, shared contracts, or work beyond the concurrency boundary.

## Task Card Shape

Before dispatch, each task should fit this shape:

```md
## Target

Exact files, symbols, tests, or subsystem.

## Goal

One concrete outcome.

## Constraints

Non-goals, files not to touch, behavior not to change.

## Context

Existing pattern, relevant decisions, expected interface.

## Acceptance

Observable result the controller can review.
```
