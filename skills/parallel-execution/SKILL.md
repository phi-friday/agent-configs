---
name: parallel-execution
description: Use when work contains two or more independent tasks, failures, files, subsystems, reviews, or investigations that can proceed without shared mutable state or sequential dependency. Decompose work, dispatch focused subagents with self-contained prompts, integrate results, review conflicts, and run final verification centrally. 한국어: 작업에 서로 독립적인 task, failure, file, subsystem, review, investigation이 둘 이상 있고 공유 mutable state나 순차 의존 없이 진행할 수 있을 때 사용한다. 작업을 분해하고, self-contained prompt로 focused subagent를 dispatch하고, 결과를 통합하고, conflict를 검토하고, 최종 검증은 중앙에서 수행한다.
---

# Parallel Execution

Use parallel agents to reduce wall-clock time without losing control of scope, quality, or integration.

## Non-Negotiables

```text
PARALLELIZE ONLY INDEPENDENT WORK.
EVERY SUBAGENT GETS A SELF-CONTAINED CONTRACT.
THE CONTROLLER OWNS INTEGRATION AND FINAL VERIFICATION.
```

Do not dispatch agents into the same unclear problem and hope they converge. Decompose first.

## Supporting References

Keep this file as the operating checklist. Open supporting references when needed:

- `references/task-decomposition.md` — deciding what can run in parallel and what must be sequenced.
- `references/subagent-prompts.md` — writing self-contained assignments with scope, constraints, and output contracts.
- `references/review-integration.md` — reviewing agent output, resolving conflicts, and verifying the combined result.

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

Before dispatching, group work by domain and dependency.

For each candidate task, identify:

- exact files or subsystem
- goal and non-goals
- dependencies on other tasks
- expected output
- whether it can succeed without seeing another agent's result
- likely conflicts with other tasks

Parallelize only when tasks can complete correctly with the context provided up front.

Use `references/task-decomposition.md` for the decision rules.

## Phase 2 — Create Focused Contracts

Each subagent assignment must be self-contained.

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

## Phase 3 — Dispatch In Parallel

Dispatch independent tasks together.

Keep batches small enough to integrate safely. Prefer two to five focused agents over one broad agent.

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
- multiple agents need to edit the same file
- assignment says “update all” or uses broad globs without file boundaries
- subagent prompt depends on hidden conversation history
- agent returns work outside its scope
- agent asks a question that reveals missing requirements
- two agents solve the same concept differently
- review finds spec gaps but integration proceeds anyway
- final verification is skipped because agents “said it passed”

Parallel execution is a coordination technique, not a substitute for ownership.
