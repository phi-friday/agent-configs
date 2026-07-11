---
name: parallel-execution
description: "Use when work has two or more independent tasks, files, failures, subsystems, reviews, investigations, or implementation slices that can proceed without shared state or sequential dependency. 독립적인 작업, 파일, 실패, 서브시스템, 리뷰, 조사, 구현 slice가 둘 이상일 때."
---

# Parallel Execution

Use parallel agents to reduce wall-clock time without losing control of scope, quality, or integration.

## Non-Negotiables

```text
PARALLELIZE ONLY INDEPENDENT WORK.
EVERY SUBAGENT GETS A SELF-CONTAINED CONTRACT.
THE CONTROLLER OWNS INTEGRATION AND FINAL VERIFICATION.
Independent tasks in one wave are dispatched in ONE `task` call with multiple `tasks[]` entries.
User "parallelize" requests are not equivalent to scattered turns or simple tool-level parallelization.
Only use fields supported by this schema; do not include unsupported fields such as `model:`.
```

Do not dispatch agents into the same unclear problem and hope they converge. Decompose first.

## Supporting References

Keep this file as the operating checklist. Open supporting references when needed:

- `references/task-decomposition.md` — deciding what can run in parallel and what must be sequenced.
- `references/subagent-prompts.md` — writing self-contained assignments with scope, constraints, and output contracts.
- `references/review-integration.md` — reviewing subagent output, resolving conflicts, and verifying the combined result.

## Use When

Use this for:

- multiple independent implementation tasks
- failures grouped by different files or subsystems
- independent codebase investigations
- parallel review of separate artifacts
- mechanical edits across disjoint files
- plan execution where tasks do not need each other's outputs

Do not use this when:

- one task defines an API, schema, or contract that others must consume
- agents would edit the same files or shared state
- the real root cause may be common across failures
- the problem is still too vague to split safely
- you need one coherent design decision before implementation

## Phase 1 — Map Independence

Before the first dispatch, build candidate tasks and run one **pre-flight conflict gate**.

For each candidate task, identify:

- exact files or subsystem
- goal and non-goals
- API/schema/output overlap with other tasks
- dependencies on other tasks
- expected output
- whether it can succeed without another task's finished output
- likely conflicts with other tasks

Parallelize only when tasks can complete correctly with the context provided up front.

If the gate finds overlap:

- split by domain,
- sequence dependent work first,
- then dispatch non-conflicting tasks in a batch.

Use `references/task-decomposition.md` for the decision rules.

## Phase 2 — Create Focused Contracts

Each subagent assignment must be self-contained.

Use the current `task` schema exactly:

- batch `context`: `# Goal`, `# Constraints`, `# Contract`
- every `tasks[].assignment`: `# Target`, `# Change`, `# Acceptance`

Include:

- target files or symbols
- specific change or investigation goal
- constraints and non-goals
- context needed to avoid re-discovery
- acceptance criteria
- expected response format
- instruction to skip project-wide gates, formatters, and final verification

Do not make a subagent read a large plan and infer its slice. Extract the exact slice for it.

Use `references/subagent-prompts.md` for assignment templates.

For large task briefs, handoff files (`local://...`) instead of pasting large prompts.

## Phase 3 — Dispatch In Parallel

Dispatch independent tasks together in one `task` batch.

Keep every assignment focused enough to integrate safely, but dispatch the full independent fan-out in one batch. Do not serialize work merely to enforce an arbitrary batch size; use separate waves only for real dependencies, shared contracts, or the tool's concurrency boundary.

The controller remains responsible for:

- answering subagent questions
- preventing scope drift
- coordinating if agents discover overlap
- deciding whether to sequence follow-up work
- tracking status with todos

Subagent status handling:

- **DONE**: review output and changed files.
- **DONE_WITH_CONCERNS**: inspect concerns before accepting work.
- **NEEDS_CONTEXT**: provide missing context or narrow the task.
- **BLOCKED**: change something: more context, smaller task, different approach, or sequence it.

Dependencies are sequential:

- same-scope dependent tasks must be separate waves
- independent tasks can be one `task` call with multiple `tasks[]` entries

Never force a blocked agent to retry unchanged.

## Phase 4 — Review and Integrate

When agents return, read every result before editing further.

Check:

- did each task meet its acceptance criteria?
- did any agent exceed scope?
- did two agents edit the same file or contract?
- did one result invalidate another?
- are there duplicated abstractions or inconsistent naming?
- are there follow-up tasks that must now be sequenced?

For large, production-impact slices, optionally dispatch one read-only task reviewer in a separate wave.

Use local file handoff contracts and avoid external runtime script/prompt dependencies.

- task brief file (`local://...`) with exact target files/symbols and constraints
- implementation report file (`local://...` or `artifact://...`) with concrete findings and evidence
- review package file (`local://...` or `artifact://...`) containing exact target/evidence and diff package for that task window

Do not force reviewer dispatch for every small task.

Spec compliance comes before code quality. First verify that the work matches the assignment; then review whether it is maintainable.

Use `references/review-integration.md` for integration gates.

## Phase 5 — Verify Centrally

Subagents do not own final verification. The controller runs the final checks after integrating the combined work.

Run only the relevant tests/checks for the changed scope unless the user asked for broader verification.

Final output must state:

- what was parallelized
- what changed
- what was verified
- unresolved risks or follow-up decisions, if any

## Red Flags

Stop and regroup if any of these appear:

- agents need each other's unfinished outputs
- several agents need to edit the same file
- assignment says “update all” or uses broad globs without file boundaries
- subagent prompt depends on hidden conversation history
- agent returns work outside its scope
- agent asks a question that reveals missing requirements
- two agents solve the same concept differently
- review finds spec gaps but integration proceeds anyway
- final verification is skipped because agents “said it passed”

Parallel execution is a coordination technique, not a substitute for ownership.
