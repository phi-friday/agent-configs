# Code Review Request

Request review when independent technical judgment would reduce risk before work cascades.

## When Review Is Warranted

Request review for:

- major features
- security, auth, payments, data, migration, or infrastructure changes
- complex bug fixes
- broad refactors
- public API or schema changes
- production code produced by subagents
- work that will be merged or handed off as complete

For very small mechanical changes, review can be skipped if verification is strong and risk is low. State that reason in the final report.

## Review Request Template

```md
# Review Target

<Exact one target is required. Choose one:
- `[BASE]..[HEAD]` commit range (for scoped repo history)
- GitHub PR (`https://github.com/<owner>/<repo>/pull/<n>` or `owner/repo#n`)
- explicit file set (paths, globs, or hunks)
- artifact URI
>

# What Changed

<Brief factual summary of what changed in the target.>

# Requirements

<Plan, acceptance criteria, issue, or user request — self-contained; do not depend on hidden context.>

# Review Focus

<Spec compliance | code quality | security | tests | integration risk.>

# Known Risks

<Uncertainty, tricky files, compatibility concerns, skipped checks.>

# Reviewer Contract

- Reviewer is read-only by default.
- Do not infer context from hidden conversations or prior chat.
- Report only against the provided target and request text.

# Requested Output

For each finding, return:

- Severity (`critical` | `important` | `minor`)
- Location: `file:line` or artifact evidence
- Why it is a risk
- Required action

Also include strengths and final assessment:

- Strengths
- Critical issues
- Important issues
- Minor issues
- Assessment: approved / with fixes / not ready
```

## What Reviewer Should Check

- implementation matches requirements
- no missing or extra behavior
- clean separation of concerns
- error handling and edge cases
- compatibility and migration risk
- security or data-loss risk
- tests verify real behavior
- no over-broad or speculative changes
- findings include severity, `file/line` evidence, risk, and required action

## Acting On Review

- Critical: fix before proceeding.
- Important: fix before merge/completion unless technically rejected with evidence.
- Minor: fix if cheap; otherwise note as non-blocking.

Review feedback is not automatically correct. Evaluate it using `review-feedback-handling.md`.

## Bad Review Requests

Avoid:

- “please review” with no exact target
- asking reviewer to infer context from hidden conversation
- no self-contained requirements
- no review focus
- no known risks / compatibility notes
- asking for approval after already declaring done
