---
name: quality-gates
description: "Use before claiming work is done, fixed, passing, ready, reviewed, or mergeable. Require fresh verification evidence, request review for substantial changes, evaluate review feedback technically, apply fixes one item at a time, and report only observed results. 한국어: 작업이 완료됨, 수정됨, 통과함, 준비됨, 리뷰됨, 병합 가능함을 말하기 전에 사용한다. 신선한 검증 증거를 요구하고, 중요한 변경에는 리뷰를 요청하고, 리뷰 피드백을 기술적으로 평가하고, 항목별로 수정하며, 관찰된 결과만 보고한다."
---

# Quality Gates

Do not declare success from confidence, intent, or agent reports. Declare only what fresh evidence proves.

## Non-Negotiables

```text
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.
NO MERGE-READY CLAIMS WITHOUT REVIEW WHEN REVIEW IS WARRANTED.
NO BLIND IMPLEMENTATION OF REVIEW FEEDBACK.
```

Evidence comes before claims. Review is a quality gate, not a ceremony. Feedback is evaluated technically, not accepted performatively.

## Supporting References

Keep this file as the operating checklist. Open supporting references when needed:

- `references/verification-evidence.md` — mapping claims to proof and reading command output.
- `references/code-review-request.md` — when and how to request focused code review.
- `references/review-feedback-handling.md` — evaluating and applying review feedback rigorously.

## Use When

Use this before:

- saying work is done, fixed, passing, ready, complete, clean, reviewed, or mergeable
- marking a task complete
- moving to another task after a meaningful change
- creating a commit, PR, or merge request
- accepting subagent work as complete
- responding to code review feedback
- closing a bug or claiming a regression is fixed

## Phase 1 — Identify The Claim

Before speaking, identify the exact claim you are about to make.

Examples:

- “tests pass”
- “bug is fixed”
- “requirements are met”
- “review feedback is addressed”
- “ready to merge”

If the claim is vague, rewrite it into something verifiable.

Bad:

```text
Looks good.
```

Better:

```text
The targeted unit tests pass, and the original repro no longer fails.
```

## Phase 2 — Match Claim To Evidence

Every claim needs specific proof.

| Claim | Required evidence |
|---|---|
| Tests pass | fresh test command output with 0 failures |
| Build succeeds | fresh build command exit 0 |
| Lint/typecheck clean | corresponding command output with 0 errors |
| Bug fixed | original repro or regression test passes |
| Regression test works | test failed before fix and passes after fix |
| Requirements met | checklist against requirements, not just tests |
| Agent completed task | inspect diff/output; do not trust report alone |
| Review feedback addressed | each item mapped to fix, rejection, or clarification |
| Ready to merge | relevant verification and review gates passed |

Run the full relevant command, not a convenient subset, unless the claim is explicitly scoped to that subset.

Use `references/verification-evidence.md` for claim-to-proof rules.

## Phase 3 — Run And Read Verification

Run fresh verification in the current state.

Then read:

- exit code
- failure count
- skipped tests if relevant
- warnings or errors
- whether the command actually covered the claim
- whether output was truncated or filtered

If verification fails, report the actual failure. Do not soften it into “almost done.”

If verification is partial, scope the claim honestly:

```text
Targeted parser tests pass. Full suite was not run.
```

## Phase 4 — Request Review When Warranted

Request review for:

- major features
- security, data, migration, auth, payments, or infra changes
- complex bug fixes
- broad refactors
- work produced by subagents that affects production code
- anything that will be merged or handed off as complete

A review request must include:

- what changed
- requirements or plan
- diff/range or files to inspect
- what kind of review is needed
- known risks or areas of uncertainty

Use `references/code-review-request.md` for the review request template.

## Phase 5 — Handle Review Feedback

Read all feedback before implementing any item.

For each item:

1. understand the technical request
2. verify it against the codebase
3. decide: fix, reject with reason, or ask clarification
4. implement one item or coherent group
5. test the affected behavior
6. mark the item resolved with evidence

Do not blindly implement review comments. Do not perform agreement. Technical correctness wins over social comfort.

Use `references/review-feedback-handling.md` for multi-item feedback and pushback rules.

## Phase 6 — Final Report

Only after verification and required review gates, report:

```md
## Status

## Evidence

## Review

## Changes

## Remaining Risk
```

Every statement in the report must be backed by observed evidence.

If something was not run, say so. If review was not requested because the change was small, state the reason.

## Red Flags

Stop and verify if you are about to say:

- “done”
- “fixed”
- “passes”
- “looks good”
- “should work”
- “probably”
- “ready”
- “review addressed”
- “agent completed it”

Stop and reassess if:

- you are trusting a previous run
- a subagent says success but you have not inspected evidence
- tests pass but requirements were not checked
- review feedback is unclear
- review suggestion may break compatibility
- you want to batch many feedback items without testing between them
- you are tempted to thank or agree instead of technically evaluating

Quality gates exist to prevent false completion.
