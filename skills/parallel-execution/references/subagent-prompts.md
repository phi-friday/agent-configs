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

Do not ask a subagent to infer its task from a large plan. Paste the exact slice.

## Implementation Assignment Template

```md
# Target

<Exact files/symbols/artifacts. Explicit non-goals.>

# Change

<Step-by-step change. Existing patterns to follow. Boundaries not to cross.>

# Constraints

- Do not touch <files/areas>.
- Do not run project-wide build/test/lint or formatters.
- Do not perform final verification; report suggested checks instead.
- Ask if requirements are unclear instead of guessing.

# Acceptance

<Observable result the controller can inspect.>

# Report

Return:
- Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
- Files changed
- What changed
- Concerns or assumptions
- Suggested verification for controller
```

## Investigation Assignment Template

```md
# Question

<Specific question to answer.>

# Scope

<Files/subsystem/logs/tests to inspect.>

# Constraints

- Read-only: do not edit files.
- Do not run project-wide gates.
- Do not broaden beyond this subsystem unless required to answer the question.

# Report

Return:
- Answer
- Evidence with file paths and line references
- Unknowns
- Recommended next step
```

## Review Assignment Template

```md
# Review Target

<Files, diff, artifact, or implementation report.>

# Review Goal

<Spec compliance | code quality | integration risk | test quality.>

# Criteria

<List specific requirements or quality bars.>

# Constraints

- Read-only unless explicitly asked to patch.
- Do not run project-wide gates.

# Report

Return:
- Approved or issues found
- Critical / Important / Minor issues
- Evidence with file paths and line references
- Required fixes
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
