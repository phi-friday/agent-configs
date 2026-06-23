---
name: github-pr-review
description: "Use when drafting a GitHub pull request review, or when submitting selected findings from an existing PR review draft. PR 리뷰 초안 작성, PRF-* 항목 제출, GitHub review payload 검수/승인."
---

# GitHub PR Review

Review GitHub pull requests in explicit modes: draft, submit selected draft findings, or YOLO draft-and-submit/request-changes/approve when the user explicitly opts in.

## Non-Negotiables

```text
RESOLVE DRAFT VS SUBMIT VS YOLO MODE BEFORE REVIEW WORK.
NO GITHUB MUTATION DURING DRAFT MODE.
NO SUBMISSION WITHOUT AN EXISTING PRF-* DRAFT, EXCEPT YOLO MODE'S SAME-RUN DRAFT.
NO USER-APPROVAL BYPASS OUTSIDE EXPLICIT YOLO MODE.
YOLO MODE ONLY WHEN `scripts/detect_mode.py` RETURNS MODE `yolo`.
NO NEW FINDINGS DURING NORMAL SUBMIT MODE.
YOLO MODE WITH ZERO ACTIONABLE FINDINGS MUST APPROVE THE PR UNLESS APPROVAL IS FORBIDDEN, EXCEPT SELF-AUTHORED PRS MUST FALL BACK TO COMMENT.
YOLO MODE OWNS THE REVIEW EVENT.
YOLO MODE WITH BLOCKING MUST FIX MUST REQUEST CHANGES, EXCEPT SELF-AUTHORED PRS MUST FALL BACK TO COMMENT.
ALWAYS ANSWER THE USER IN KOREAN.
```

## Supporting References

Open only the reference needed for the current mode:

- `references/mode-selection.md` — classify user intent as Draft, Submit, YOLO, or ambiguous.
- `references/draft-mode.md` — read-only PR review workflow and draft output contract.
- `references/submit-mode.md` — selected finding submission workflow and GitHub mutation guardrails.
- `references/yolo-mode.md` — same-run draft and review-event submission/approval workflow without user inspection.
- `scripts/detect_mode.py` — explicit `draft`/`submit`/`yolo` mode keyword classifier.
- `references/payload-approval.md` — exact preview and mandatory `ask` approval gate for normal Submit mode.

## Use When

Use this skill for:

- drafting a GitHub pull request review
- resolving a PR from a number, branch name, or current branch
- producing stable review finding IDs for later submission
- submitting selected `PRF-*` findings from an existing draft
- running explicit `yolo` draft-and-submit/request-changes/approve in one pass
- preserving excluded review context for future reviewers

Do not use this as a generic code review workflow when there is no GitHub PR context.

## Step 1 — Resolve Mode From User Input

Before inspecting the PR, reading a diff, or preparing a payload, classify the user's latest request.

```text
first word is exact `draft` or `draft,`
    └─ Draft mode

first word is exact `submit` or `submit,`
    └─ Submit mode

first word is exact `yolo` or `yolo,`
    └─ YOLO mode: draft, choose review event, and submit/approve in one run without payload approval

unclear whether the user wants review analysis or GitHub publication
    └─ Ambiguous: ask with the ask tool, then continue in the selected mode
```

Use `references/mode-selection.md` for the exact classifier. Run `scripts/detect_mode.py` first; explicit `draft`, `submit`, and `yolo` keywords override LLM inference, while no explicit keyword falls back to normal intent resolution.

If mode is ambiguous, do not ask in ordinary prose and stop. Use the `ask` tool with mode choices, then continue the chosen workflow after the answer.

## YOLO Mode Summary

YOLO mode runs Draft mode, then owns the GitHub Review API event: approve clean PRs, request changes for high-confidence blocking `Must Fix` findings, and comment otherwise. If a self-authored PR would require `APPROVE` or `REQUEST_CHANGES`, submit the review with `COMMENT` instead.

Hard boundaries:

- only use when `scripts/detect_mode.py` returns mode `yolo` for the user's latest input
- do not infer YOLO mode from uppercase `YOLO`, suffixes like `yolox`, later words like `XXX yolo`, or synonyms such as “auto”, “바로 제출”, or “검수 없이”; `yolo,` is the only allowed punctuation form
- do not call the `ask` tool for payload approval
- still validate PR context, anchors, file paths, payload shape, and GitHub mutation scope before submitting
- if any selected finding cannot be faithfully submitted, stop before mutation and report the blocker
- if the same-run draft finds no actionable findings and validation shows no failing or pending merge-blocking checks, submit exactly one `APPROVE` review without asking, unless the same request explicitly forbids approval or the self-authored PR fallback below applies
- if any selected finding is a high-confidence blocking `Must Fix`, submit exactly one `REQUEST_CHANGES` review without asking, unless the self-authored PR fallback below applies
- if the PR author login equals the current viewer login, GitHub may reject `APPROVE` and `REQUEST_CHANGES`; when Event Mode would choose either event for a self-authored PR, use `COMMENT` instead and still submit the review content
- use `COMMENT` for non-blocking findings, uncertain evidence, pending or unclear validation, or explicit comment-only behavior

YOLO mode submits every actionable draft finding by default unless the same YOLO request explicitly includes or excludes IDs/categories. It does not require the user to preselect `COMMENT` vs `REQUEST_CHANGES`; Event Mode in `references/yolo-mode.md` controls that decision.

Use `references/yolo-mode.md` for the full workflow.

## Global Language Rule

- Always answer the user in Korean.
- Draft findings are Korean by default.
- GitHub review comments are Korean by default.
- Use English for GitHub comments only when the user explicitly requests English in the current invocation.
- Keep identifiers unchanged: file paths, function names, APIs, commands, branch names, and `PRF-*` IDs.

## Draft Mode Summary

Draft mode analyzes a PR and reports findings to the user only.

Hard boundaries:

- never mutate GitHub
- never submit, approve, request changes, comment, edit, merge, close, reopen, label, or assign
- never run `gh pr review`, `gh pr comment`, `gh pr merge`, `gh pr edit`, or mutating `gh api`
- never publish local changes with `git commit` or `git push`

Draft mode must:

1. confirm local repository context with non-mutating checks
2. resolve the target PR
3. read existing PR context before the diff
4. inspect the diff and validation evidence
5. report actionable findings with stable `PRF-*` IDs
6. attach a submission target to every actionable finding: `inline`, `file`, or `general`

Use `references/draft-mode.md` for the full workflow and output format.

## Draft Finding Contract

Every actionable finding that might later be submitted must include:

```md
- `PRF-001` [Must Fix] <summary>
  - Submission target: inline | file | general
  - Inline anchor: `path/to/file.ts:42` (`side: RIGHT`) <!-- inline only -->
  - File: `path/to/file.ts` <!-- file only -->
  - Risk: <what can go wrong>
  - Suggested fix: <concrete fix>
```

Rules:

- Collect existing `PRF-*` IDs before assigning new ones.
- New IDs start after the highest observed numeric suffix.
- Never reuse an ID for a different concern.
- Do not assign IDs to metadata, context summaries, validation observations, or final assessment.
- If no faithful inline diff anchor exists, write `Inline anchor: unavailable` and explain why.

## Submit Mode Summary

Submit mode publishes selected findings from an existing draft. It is not a second review pass.

Submit mode requires a completed draft in the current conversation with actionable `PRF-*` IDs.

Hard boundaries:

- never create new findings
- never materially rewrite or strengthen draft findings
- inspect the diff only to validate selected anchors and file paths
- submit exactly one GitHub PR review only after exact payload approval through `ask`
- do not approve, merge, close, reopen, label, assign, edit, commit, or push

Submit mode must:

1. validate that a usable draft exists
2. resolve included and excluded `PRF-*` IDs from the user's instruction
3. validate selected submission targets
4. preserve excluded review context when findings are not submitted
5. compose exact inline comments, top-level body, and API payload
6. show the exact preview
7. call the `ask` tool for exact payload approval
8. submit only after approval
9. report the observed submission result

Use `references/submit-mode.md` for selection, validation, excluded-context, and result rules.
Use `references/payload-approval.md` for the approval preview and `ask` gate in normal Submit mode.
