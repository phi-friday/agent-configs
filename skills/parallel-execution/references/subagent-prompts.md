# Subagent Prompts

Subagents start without the controller's conversation history. Every assignment must be self-contained.

## Prompt Requirements

Each prompt must include:

- exact target files, symbols, tests, or artifacts
- task goal
- relevant context and existing patterns
- constraints and non-goals
- expected output format
- whether edits are allowed or read-only
- instruction to skip project-wide gates, formatters, and final verification
- file handoff for large prompts (`local://...`) to avoid transcript duplication

Do not ask a subagent to infer its task from a large plan. Paste the exact slice.

For production-like larger slices, hand off large prompts as files:

- task brief file (`local://...`) for implementers, with exact target and constraints
- implementation report file (`local://...` or `artifact://...`) for status and findings, with concrete evidence
- review artifact or diff-evidence package file (`local://...` or `artifact://...`) for reviewer assignments, with exact target/evidence

## Batch Context Template

The shared `task.context` uses exactly these top-level headings:

```md
# Goal

<What the whole batch accomplishes.>

# Constraints

<Rules and decisions shared by every task.>

# Contract

<Shared interfaces, boundaries, and output expectations.>
```

## Implementation Assignment Template

Every `tasks[].assignment` uses exactly the required `# Target`, `# Change`, and `# Acceptance` top-level headings:

```md
# Target

<Exact files/symbols/artifacts. Explicit non-goals.>

# Change

<Step-by-step change, relevant context, existing patterns, and boundaries.>

- Do not touch <files/areas>.
- Do not run project-wide build/test/lint or formatters.
- Do not perform final verification; report suggested checks instead.
- Ask if requirements are unclear instead of guessing.
- Use local file handoff for large requirement/report artifacts.

# Acceptance

<Observable result the controller can inspect.>

Return:
- Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
- Files changed
- What changed
- Concerns or assumptions
- Suggested verification for controller
```

## Investigation Assignment Template

```md
# Target

<Exact files/subsystem/logs/artifacts to inspect. Mark the task read-only and state explicit non-goals.>

# Change

<Specific question to answer and context required to answer it.>

- Read-only: do not edit files.
- Do not run project-wide gates.
- Do not broaden beyond this subsystem unless required to answer the question.

# Acceptance

Return:
- Answer
- Evidence with file paths and line references
- Unknowns
- Recommended next step
```

## Review Assignment Template

```md
# Target

<Exact files, diff, artifact, or implementation report. State explicit non-goals.>

# Change

Read-only review. Include the self-contained review goal, requirements, criteria, focus, known risks, and compatibility constraints.

- Do not edit unless explicitly asked to patch in a later task.
- Do not run project-wide gates.
- Keep transcript size low: point to `local://...` or `artifact://...` for larger context.

# Acceptance

For every actionable finding, return:
- Severity: Critical | Important | Minor
- Exact `file:line` or artifact evidence
- Concrete risk
- Required action

Also return strengths and assessment: approved | with fixes | not ready.
```

## Status Meanings

- **DONE**: task completed within scope.
- **DONE_WITH_CONCERNS**: completed, but correctness/scope/maintainability concern remains.
- **NEEDS_CONTEXT**: cannot proceed without specific missing information.
- **BLOCKED**: task cannot be completed as assigned.

Treat `DONE_WITH_CONCERNS` as requiring controller review before integration.

## Common Prompt Failures

- too broad: “fix all tests”
- hidden context: “use the approach we discussed”
- missing boundaries: no files or non-goals
- missing output contract: no way to integrate result
- asking subagent to verify the whole project
- asking multiple agents to own the same file
