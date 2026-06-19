# github-pr-review

[English](README.md) | [한국어](README.kr.md)

`github-pr-review` is an in-progress skill for GitHub PR review drafting, controlled review submission, and explicit YOLO draft-and-submit.

It treats review drafting, normal GitHub publication, and YOLO publication as separate modes. The mode is resolved from the user's input first; ambiguous requests are clarified with the `ask` tool and then continued in the selected mode.

## File Layout

```text
github-pr-review/
├─ SKILL.md
├─ SKILL.kr.md
├─ README.md
├─ README.kr.md
├─ references/
│  ├─ mode-selection.md
│  ├─ draft-mode.md
│  ├─ submit-mode.md
│  ├─ yolo-mode.md
│  └─ payload-approval.md
└─ scripts/
   └─ detect_yolo_mode.py
```

## File Roles

- `SKILL.md`: Base skill definition, mode summary, and safety-critical contracts.
- `SKILL.kr.md`: Korean translation of `SKILL.md`.
- `README.md`: English README.
- `README.kr.md`: Korean README.
- `references/mode-selection.md`: Rules for classifying user input as Draft, Submit, YOLO, or ambiguous.
- `references/draft-mode.md`: Read-only PR review workflow and draft output format.
- `references/submit-mode.md`: Selected `PRF-*` submission workflow and mutation scope.
- `references/yolo-mode.md`: Same-run draft and submit workflow, enabled only when the first user-input word is exactly `yolo`.
- `references/payload-approval.md`: Exact preview format and mandatory `ask` approval gate for normal Submit mode.
- `scripts/detect_yolo_mode.py`: Runtime classifier for whether the raw user input enables YOLO mode.

## Scope

Use this skill when:

- reviewing a GitHub PR without submitting comments
- creating stable `PRF-*` review finding IDs
- preparing a handoff from draft findings to later submission
- submitting selected findings from an existing draft
- running first-word `yolo` draft-and-submit without a user inspection gate
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
    ├─ Submit mode ─▶ select PRF-* → validate anchors → preview exact payload → ask approval → submit
    │
    └─ YOLO mode ───▶ draft → validate all selected findings → submit without ask approval
```

Core rule:

```text
resolve mode → draft safely, submit from existing draft, or first-word yolo → never bypass approval unless the input starts with exact `yolo`
```
