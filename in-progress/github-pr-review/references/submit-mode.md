# Submit Mode

Normal Submit mode publishes selected findings from an existing draft. It must never be used as an independent review command. YOLO mode is defined separately in `yolo-mode.md`.

## Prerequisite

A usable draft must already exist in the current conversation.

Stop immediately if:

- no completed draft exists for the target PR
- the draft has no actionable `PRF-*` IDs
- the target PR or repository is ambiguous
- requested IDs are unknown
- selected inline findings lack exact anchors
- selected file/general findings lack enough text to submit faithfully
- an ID collision maps one `PRF-*` ID to different concerns

Never inspect the diff to discover or revise findings. Diff inspection is allowed only to validate selected anchors and file paths.

## Selection Rules

Parse the user's latest instruction plus any command arguments.

Supported intents:

- include only: `PRF-001만`, `PRF-001 PRF-003만 포함`, `include PRF-002`
- exclude: `PRF-002 제외`, `except PRF-003`, `PRF-001 빼고`
- mixed: include set minus exclude set
- submit/post/upload with no explicit selection: include all actionable current draft findings

If the user indirectly refers to a finding, such as `그것만` or `그건 제외`, resolve it only when the current conversation makes the target ID unambiguous.

If selection is ambiguous, ask one concise clarification question before any GitHub mutation.

If selection resolves to an empty set, stop and report that there is nothing to submit.

Selectable IDs include:

- current actionable draft IDs
- prior excluded-context IDs surfaced by the latest draft, when there is enough text to submit faithfully

Do not include draft sections that are not review points: PR metadata, context summaries, validation observations, or final assessment, unless the user explicitly asks to include them in the top-level review body.

## Context Confirmation

Before preparing the payload, re-confirm with non-mutating checks:

```sh
pwd
git status --short --branch
git branch --show-current
git remote -v
gh repo view --json nameWithOwner,url
gh pr view <number> --json number,title,state,isDraft,author,baseRefName,headRefName,headRefOid,url,reviewDecision,mergeStateStatus
```

Use these commands only to validate selected inline anchors and file paths against the PR diff:

```sh
gh api "repos/{owner}/{repo}/pulls/<number>/files" --paginate --jq '.[].filename'
gh pr diff <number> --patch --color never
```

## Target Validation

For each selected finding, extract `Submission target: inline | file | general` from the draft.

`inline` requires:

- `path`
- `line`
- `side: RIGHT | LEFT`
- optional `start_line` and `start_side` together for ranges

Confirm the path exists in the PR diff and the target line is on the requested side. Do not move anchors, choose nearby lines, or infer missing fields during Submit mode.

Record the `headRefOid` used for validation and include it as `commit_id` in the payload. If the PR head changes before submission, stop, rebuild the payload, and repeat approval.

`file` requires:

- `path` exactly as it appears in the PR diff or selected draft context

Do not invent a line number for `file` findings.

`general` requires enough draft text to submit faithfully without a file or line anchor.

If validation fails, stop before approval and report the blocked IDs.

## Compose Review Content

Inline comment bodies:

- include only selected `inline` findings
- preserve each selected `PRF-*` ID at the start
- preserve severity, file/function context, risk, and suggested fix from the draft when present
- do not mention excluded IDs unless a prior excluded-context ID is now selected for visible submission
- do not add new findings
- do not renumber IDs

Top-level review body:

- must be non-empty when `event` is `COMMENT` or `REQUEST_CHANGES`
- includes selected `file` findings
- includes selected `general` findings
- includes excluded-context details when needed
- does not duplicate selected inline findings already in `comments[]`
- if there are only inline findings and no excluded context, use `인라인 리뷰 코멘트를 남겼습니다.`

## Excluded Review Context

If one or more draft IDs are excluded, preserve a compact note in the top-level body.

Carry forward still-relevant prior excluded-context entries unless the same ID is selected for visible submission or the latest draft says the exclusion is obsolete.

Default Korean block:

```md
<details>
<summary>제외된 리뷰 컨텍스트 (제출하지 않음)</summary>

이 draft 리뷰 항목들은 검토했지만 의도적으로 제출하지 않았습니다. 새로운 근거가 제외 결정을 무효화하지 않는 한 후속 리뷰에서 다시 제기하지 마세요.

이번 리뷰에서 새로 제외:

- `PRF-002` — 사용자 선택으로 제외됨; 기술적 판단은 제공되지 않았습니다. 원본 draft: <severity/file/summary>.

이전 제출에서 유지:

- `PRF-004` — <recorded exclusion reason>. 원본 draft: <severity/file/summary>.

</details>
```

Rules:

- Use the user's stated exclusion reason when provided.
- If the user excludes an ID without a reason, use `사용자 선택으로 제외됨; 기술적 판단은 제공되지 않았습니다.`
- Never invent a technical resolution for an excluded item.
- Omit the block when there are no newly excluded IDs and no carried-forward prior exclusions.

## Mutation Scope

After the mandatory approval gate in `payload-approval.md`, submit exactly one GitHub PR review. This approval gate applies to normal Submit mode only; explicit YOLO mode follows `yolo-mode.md`.

Immediately before the mutation, re-read `headRefOid`. If it differs from the approved payload's `commit_id`, do not submit; rebuild the payload and repeat the approval gate.

```sh
gh api -X POST "repos/{owner}/{repo}/pulls/<number>/reviews" --input <payload-file>
```

Rules:

- Use `COMMENT` by default.
- Use `REQUEST_CHANGES` only when the user explicitly requests it and approves that exact mode in the payload preview.
- Do not approve the PR.
- Do not use `gh pr review` for inline comments; it cannot submit the `comments[]` inline-review payload.
- Do not use `gh pr comment` unless the user explicitly approves a separate fallback plan.
- Never merge, close, reopen, label, assign, edit, commit, or push.

## Result Format

Answer in Korean.

```md
## 제출 결과

- PR: #<number> <url>
- 제출한 인라인 항목: <PRF-001 or 없음>
- 제출한 상위 본문 항목: <PRF-003 or 없음>
- 인라인 위치: <PRF-001 path/to/file.ts:42 RIGHT or 없음>
- 제외한 항목: <PRF-002 or 없음>
- 유지한 이전 제외 컨텍스트: <PRF-004 or 없음>
- 제출 방식: <review comments | request changes>
- GitHub Review API event: <COMMENT | REQUEST_CHANGES>

## 비고

- <failure details, fallback note, or omitted if not needed>
```
