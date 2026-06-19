# YOLO Mode

YOLO mode drafts a PR review, then submits actionable findings or approves the PR when the draft is clean.

Use it only when the mandatory classifier script confirms the user's latest raw input has explicit mode `yolo`.

```sh
python scripts/detect_mode.py -- "<raw latest user input>"
```

Only exit code `0` and JSON field `"mode": "yolo"` permit YOLO mode. Do not classify YOLO mode by LLM judgment alone.

The script's match is case-sensitive and word-exact: the first whitespace-delimited word equals lowercase `yolo` or exactly `yolo,`.

Examples that enable YOLO mode:

- `yolo`
- `yolo review PR #123`
- `yolo #123 리뷰하고 올려`
- `yolo, review PR #123`

Examples that do not enable YOLO mode:

- `YOLO`
- `yolox`
- `yolomode`
- `yolo모드로 진행`
- `yolo,review PR #123`
- `XXX yolo`
- `draft부터 submit까지 한번에 진행`
- `사용자 검수 없이 제출`
- `auto submit all findings`
- `리뷰하고 바로 올려`

## Hard Boundaries

No user inspection gate. The user already opted into this by making exact `yolo` or `yolo,` the first input word.

Do not call the `ask` tool for payload approval.

Still stop before mutation when required information is missing or unsafe:

- target PR cannot be resolved
- multiple PRs match and no target can be selected safely
- GitHub repository context cannot be confirmed
- a selected finding cannot be faithfully submitted
- inline anchors or file paths cannot be validated
- GitHub Review API payload cannot be built exactly

YOLO mode bypasses only the payload approval gate. It does not bypass PR resolution, existing-context review, anchor validation, payload construction, or GitHub mutation limits.

Approve only when Event Mode permits `APPROVE`. Otherwise never approve while submitting actionable findings, and never merge, close, reopen, label, assign, edit, commit, or push.

## Workflow

Run Draft mode first.

1. Resolve the target PR from the user input or current branch.
2. Read existing PR context before the diff.
3. Inspect the diff and validation evidence.
4. Produce actionable findings with stable `PRF-*` IDs and submission targets.
5. Choose the GitHub Review API event with Event Mode below.
6. If Event Mode chooses `APPROVE`, validate that the current `headRefOid` still matches the reviewed commit, then submit exactly one GitHub PR review with event `APPROVE`, no inline comments, and a concise Korean body saying no actionable findings were found.

If Event Mode chooses `COMMENT` or `REQUEST_CHANGES`, submit from the just-created draft.

When `COMMENT` is chosen with no actionable findings because validation is pending or unclear, submit a top-level body only. Do not invent `PRF-*` IDs; state the validation uncertainty plainly.

1. Submit every actionable draft finding by default.
2. Apply explicit include/exclude instructions only if they appear in the same YOLO request.
3. Validate every selected target using Submit mode target validation.
4. Compose the exact inline comments, top-level body, API payload, and selected event.
5. Submit exactly one GitHub PR review with `gh api`.
6. Report the observed submission result in Korean.

## Selection In YOLO Mode

Default selection:

```text
all actionable draft findings
```

The user may narrow the set in the same request:

- `yolo PRF-001만 올려`
- `yolo PRF-002 제외`
- `yolo Must Fix만 제출`

If the requested subset is ambiguous after the draft is produced, stop before mutation and report the ambiguity. Do not ask for payload approval; the issue is selection safety, not content approval.

## Event Mode

In YOLO mode, the agent owns the GitHub review event.

Decision order:

1. Stop before mutation when PR resolution, repository context, target validation, payload construction, or head-commit validation is unsafe.
2. Use `APPROVE` only when the same-run Draft mode found no actionable findings and validation shows no failing or pending merge-blocking checks.
3. Use `REQUEST_CHANGES` when at least one selected finding is a high-confidence blocking `Must Fix`.
4. Use `COMMENT` for non-blocking findings, uncertain evidence, pending or unclear validation, or explicit comment-only behavior.

Blocking `Must Fix` means a finding that should prevent merge until fixed:

- correctness regression
- security issue
- data loss, migration corruption, or irreversible state risk
- backward compatibility break
- race condition or concurrency bug
- PR-caused required check failure
- production or user-visible severe regression
- missing required test only when the missing coverage leaves a concrete regression risk

Do not use `REQUEST_CHANGES` for style-only feedback, refactor preference, low-confidence risk, nice-to-have tests/docs, or subjective maintainability comments.

Explicit event wording in the same YOLO request can only narrow this policy:

- `yolo request changes로 제출해` may use `REQUEST_CHANGES` only when a blocking `Must Fix` exists; do not manufacture blocking severity.
- `yolo comment only`, `코멘트만`, or equivalent approval/request-changes bans force `COMMENT` when there is content to submit.
- If approval is explicitly forbidden and the draft is clean, do not approve; report that no GitHub review was submitted unless the same request explicitly asks for a top-level no-findings comment.

Never approve a PR while submitting actionable findings.

## Preview Handling

Do not show a pre-submission inspection preview and wait for user approval.

After submission or a no-submission decision, include enough detail for audit:

- submitted `PRF-*` IDs, or `없음` when approving with no findings
- inline locations
- top-level body IDs
- excluded IDs, if any
- GitHub Review API event, or `none` when no review was submitted
- review event decision
- whether the PR was approved because no actionable findings were found
- whether any finding was not submitted and why

## Result Format

Answer in Korean.

```md
## YOLO 제출 결과

- PR: #<number> <url>
- 제출한 인라인 항목: <PRF-001 or 없음>
- 제출한 상위 본문 항목: <PRF-003 or 없음>
- 인라인 위치: <PRF-001 path/to/file.ts:42 RIGHT or 없음>
- 제외한 항목: <PRF-002 or 없음>
- 제출 방식: <review comments | request changes | approval | no submission>
- GitHub Review API event: <COMMENT | REQUEST_CHANGES | APPROVE | none>
- Review event decision: <clean | blocking Must Fix | non-blocking/uncertain | comment-only | no safe submission>

## Draft 요약

- <draft context and finding summary>

## 비고

- <failure details, skipped finding reason, or omitted if not needed>
```
