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

<Files, diff range, PR, or artifact to review.>

# What Changed

<Brief factual summary.>

# Requirements

<Plan, acceptance criteria, issue, or user request.>

# Review Focus

<Spec compliance | code quality | security | tests | integration risk.>

# Known Risks

<Uncertainty, tricky files, compatibility concerns, skipped checks.>

# Requested Output

Return:
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

## Acting On Review

- Critical: fix before proceeding.
- Important: fix before merge/completion unless technically rejected with evidence.
- Minor: fix if cheap; otherwise note as non-blocking.

Review feedback is not automatically correct. Evaluate it using `review-feedback-handling.md`.

## Bad Review Requests

Avoid:

- “please review” with no requirements
- asking reviewer to infer context from hidden conversation
- no diff/range/files
- no review focus
- asking for approval after already declaring done
