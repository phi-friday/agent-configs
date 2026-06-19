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

Approve only when the same-run Draft mode finds no actionable findings. Otherwise never approve, merge, close, reopen, label, assign, edit, commit, or push.

## Workflow

Run Draft mode first.

1. Resolve the target PR from the user input or current branch.
2. Read existing PR context before the diff.
3. Inspect the diff and validation evidence.
4. Produce actionable findings with stable `PRF-*` IDs and submission targets.
5. If there are no actionable findings, validate that the current `headRefOid` still matches the reviewed commit, then submit exactly one GitHub PR review with event `APPROVE`, no inline comments, and a concise Korean body saying no actionable findings were found.

If actionable findings exist, submit from the just-created draft.

1. Submit every actionable draft finding by default.
2. Apply explicit include/exclude instructions only if they appear in the same YOLO request.
3. Validate every selected target using Submit mode target validation.
4. Compose the exact inline comments, top-level body, and API payload.
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

Use `APPROVE` only when the same-run Draft mode found no actionable findings.

When actionable findings exist, use `COMMENT` by default.

Use `REQUEST_CHANGES` only when the same YOLO request explicitly asks for request-changes mode, for example:

```text
yolo request changes로 제출해
```

Never approve a PR while submitting actionable findings.

## Preview Handling

Do not show a pre-submission inspection preview and wait for user approval.

After submission, include enough detail for audit:

- submitted `PRF-*` IDs, or `없음` when approving with no findings
- inline locations
- top-level body IDs
- excluded IDs, if any
- GitHub Review API event
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
- 제출 방식: <review comments | request changes | approval>
- GitHub Review API event: <COMMENT | REQUEST_CHANGES | APPROVE>

## Draft 요약

- <draft context and finding summary>

## 비고

- <failure details, skipped finding reason, or omitted if not needed>
```
