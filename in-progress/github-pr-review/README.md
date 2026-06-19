# github-pr-review

[English](README.md) | [한국어](README.kr.md)

`github-pr-review` is an in-progress skill for GitHub PR review drafting and controlled review submission.

It treats review drafting and GitHub publication as separate modes. The mode is resolved from the user's input first; ambiguous requests are clarified with the `ask` tool and then continued in the selected mode.

## File Layout

```text
github-pr-review/
├─ SKILL.md
├─ SKILL.kr.md
├─ README.md
├─ README.kr.md
└─ references/
   ├─ mode-selection.md
   ├─ draft-mode.md
   ├─ submit-mode.md
   └─ payload-approval.md
```

## File Roles

- `SKILL.md`: Base skill definition, mode summary, and safety-critical contracts.
- `SKILL.kr.md`: Korean translation of `SKILL.md`.
- `README.md`: English README.
- `README.kr.md`: Korean README.
- `references/mode-selection.md`: Rules for classifying user input as Draft, Submit, or ambiguous.
- `references/draft-mode.md`: Read-only PR review workflow and draft output format.
- `references/submit-mode.md`: Selected `PRF-*` submission workflow and mutation scope.
- `references/payload-approval.md`: Exact preview format and mandatory `ask` approval gate.

## Scope

Use this skill when:

- reviewing a GitHub PR without submitting comments
- creating stable `PRF-*` review finding IDs
- preparing a handoff from draft findings to later submission
- submitting selected findings from an existing draft
- preserving intentionally excluded review context

Do not use it as a generic code review skill without a GitHub PR target.

## Core Flow

```text
user input
    │
    ▼
resolve mode
    │
    ├─ Draft mode ──▶ read context → review diff → report PRF-* findings in chat only
    │
    └─ Submit mode ─▶ select PRF-* → validate anchors → preview exact payload → ask approval → submit
```

Core rule:

```text
resolve mode → draft safely or submit from existing draft → never mutate GitHub without exact ask approval
```
