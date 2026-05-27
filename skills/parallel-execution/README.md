# parallel-execution

[English](README.md) | [한국어](README.kr.md)

`parallel-execution` is an in-progress skill for splitting independent work across subagents while the controller owns integration and final verification.

## Layout

```text
parallel-execution/
├─ SKILL.md
├─ SKILL.kr.md
├─ README.md
├─ README.kr.md
└─ references/
   ├─ task-decomposition.md
   ├─ subagent-prompts.md
   └─ review-integration.md
```

## File Roles

- `SKILL.md`: Base skill definition and parallel-execution checklist.
- `SKILL.kr.md`: Korean translation of `SKILL.md`.
- `README.md`: English source README.
- `README.kr.md`: Korean translation of this README.
- `references/task-decomposition.md`: Criteria for separating parallelizable tasks from tasks that must remain sequential.
- `references/subagent-prompts.md`: Criteria and templates for self-contained subagent assignments.
- `references/review-integration.md`: Standards for reviewing subagent results, checking conflicts, and doing final verification.

## Scope

Use this skill when:

- There are multiple independent implementation tasks.
- Failures in different files or subsystems can be investigated separately.
- Codebase investigation or review can be parallelized.
- Mechanical edits to non-overlapping files can be distributed.

Core rule:

```text
decompose → self-contained dispatch → review results → integrate → central verification
```

Subagents perform and report on their own tasks. The controller performs integration and final verification.

## Reference Sources

This skill is based on these references:

- `obra/superpowers/skills/subagent-driven-development`
- `obra/superpowers/skills/dispatching-parallel-agents`

## Reference Files

Review this skill again when these files change:

- `references/obra/superpowers/skills/subagent-driven-development/SKILL.md`
- `references/obra/superpowers/skills/subagent-driven-development/implementer-prompt.md`
- `references/obra/superpowers/skills/subagent-driven-development/spec-reviewer-prompt.md`
- `references/obra/superpowers/skills/subagent-driven-development/code-quality-reviewer-prompt.md`
- `references/obra/superpowers/skills/dispatching-parallel-agents/SKILL.md`

<!-- publish-skills:reference-commits:start -->
## Reference Commits

Published against these submodule commits.

- `references/obra/superpowers`: `f2cbfbefebbfef77321e4c9abc9e949826bea9d7`
<!-- publish-skills:reference-commits:end -->

License notices for the original repositories are covered by the root `NOTICE.md`.
