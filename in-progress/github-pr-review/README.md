# github-pr-review

[English](README.md) | [한국어](README.kr.md)

`github-pr-review` is an in-progress skill for GitHub PR review drafting, controlled review submission, and explicit YOLO draft-and-submit/request-changes/approve.

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
   └─ detect_mode.py
```

## File Roles

- `SKILL.md`: Base skill definition, mode summary, and safety-critical contracts.
- `SKILL.kr.md`: Korean translation of `SKILL.md`.
- `README.md`: English README.
- `README.kr.md`: Korean README.
- `references/mode-selection.md`: Rules for classifying user input as Draft, Submit, YOLO, or ambiguous.
- `references/draft-mode.md`: Read-only PR review workflow and draft output format.
- `references/submit-mode.md`: Selected `PRF-*` submission workflow and mutation scope.
- `references/yolo-mode.md`: Same-run draft and review-event submit/request-changes/approve workflow, enabled only when the classifier returns explicit mode `yolo`.
- `references/payload-approval.md`: Exact preview format and mandatory `ask` approval gate for normal Submit mode.
- `scripts/detect_mode.py`: Runtime classifier for explicit `draft`, `submit`, and `yolo` mode keywords.

## Scope

Use this skill when:

- reviewing a GitHub PR without submitting comments
- creating stable `PRF-*` review finding IDs
- preparing a handoff from draft findings to later submission
- submitting selected findings from an existing draft
- running explicit `yolo`/`yolo,` draft-and-submit/request-changes/approve without a user inspection gate
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
    └─ YOLO mode ───▶ draft → choose event → request changes for blockers, comment otherwise, approve when clean
```

Core rule:

```text
resolve mode → use explicit `draft`/`submit`/`yolo` keywords when present → never bypass approval unless `detect_mode.py` returns mode `yolo`
```
