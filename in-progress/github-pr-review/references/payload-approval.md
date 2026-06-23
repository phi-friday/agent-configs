# Payload Approval

Normal Submit mode requires exact content approval through the `ask` tool before any GitHub-mutating command runs.

This approval gate does not apply to explicit YOLO mode. YOLO mode is enabled only when `scripts/detect_mode.py` returns `"mode": "yolo"` for the user's latest input and follows `yolo-mode.md`.

Selecting IDs is not approval to submit. Submit wording in the user's request is not approval. Ordinary chat text is not approval.

## Required Preview

Before calling `ask`, show the exact payload that will be posted.

Use this structure:

````md
## 리뷰 제출 전 검수

- PR: #<number> <url>
- Head commit: <headRefOid used as `commit_id`>
- 제출 예정 항목: <PRF-001, PRF-003>
- 인라인 항목: <PRF-001 or 없음>
- 상위 본문 항목: <PRF-003 or 없음>
- 제외 항목: <PRF-002 or 없음>
- Requested GitHub Review API event: <COMMENT | REQUEST_CHANGES | APPROVE>
- Effective GitHub Review API event: <COMMENT | REQUEST_CHANGES | APPROVE>
- 제출 방식: <review comments | request changes | approval; explain self-authored PR fallback when requested/effective differ>
- 제출 언어: <Korean by default; English only if explicitly requested>
- 인라인 코멘트 수: <n>
- 제외 컨텍스트: <details block included | 없음>
- Review body first line: `리뷰 상태: 코멘트(COMMENT)` | `리뷰 상태: 수정 요청(REQUEST_CHANGES)` | `리뷰 상태: 승인(APPROVE)`
- API: `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews`

## 실제 GitHub 인라인 코멘트

### `PRF-001` — `path/to/file.ts:42` (`side: RIGHT`)

```md
<exact GitHub inline comment body to submit>
```

## 실제 GitHub 상위 리뷰 본문

```md
<exact non-empty top-level review body to submit>
```

## 실제 GitHub API payload

```json
{
  "event": "COMMENT",
  "body": "<exact top-level review body above>",
  "commit_id": "<headRefOid>",
  "comments": [
    {
      "path": "path/to/file.ts",
      "line": 42,
      "side": "RIGHT",
      "body": "<exact inline comment body above>"
    }
  ]
}
```
````

If there are no inline comments, omit `comments` from the payload.

If the PR head SHA changes after preview approval, do not submit the old payload; rebuild the payload and ask again.

If the requested event differs from the effective event because a self-authored PR cannot receive `APPROVE` or `REQUEST_CHANGES`, the preview must show `COMMENT` in the actual payload and explicitly state that approval submits review comments instead of the requested event.

If the submission language is not Korean, include a Korean inspection section before the actual GitHub content. If the submission language is Korean, do not duplicate the same content in a separate Korean inspection copy.

## Ask Gate

Immediately after the preview, call the `ask` tool. Do not add extra prose between the preview and the tool call.

The approval question must state that approval posts the exact shown inline comments, top-level body, and API payload to the target PR.

Offer at least these choices:

1. `Approve this exact GitHub review payload and submit to GitHub`
2. `Do not submit`

Recommended default: `Do not submit`.

Only the first option permits the GitHub-mutating command.

## If The User Does Not Approve

Do not submit when:

- the user chooses `Do not submit`
- the user asks for wording changes
- the user adds or removes IDs
- the user changes submission mode or language
- the response is ambiguous
- the response arrives as ordinary chat instead of the `ask` approval

If the user requests changes, revise the payload, show the full exact preview again, and call `ask` again.

## Payload Shape

Use `line`/`side` anchors, plus `start_line`/`start_side` for ranges. Do not use diff `position` when a line/side anchor is available.

With inline comments:

```json
{
  "event": "COMMENT",
  "body": "리뷰 상태: 코멘트(COMMENT)\n\n인라인 리뷰 코멘트를 남겼습니다.",
  "commit_id": "<headRefOid>",
  "comments": [
    {
      "path": "path/to/file.ts",
      "line": 42,
      "side": "RIGHT",
      "body": "`PRF-001` ..."
    }
  ]
}
```

With only file/general findings:

```json
{
  "event": "COMMENT",
  "body": "리뷰 상태: 코멘트(COMMENT)\n\n<selected file/general findings>",
  "commit_id": "<headRefOid>"
}
```

For range comments, include both optional fields:

```json
{
  "path": "path/to/file.ts",
  "start_line": 40,
  "start_side": "RIGHT",
  "line": 42,
  "side": "RIGHT",
  "body": "`PRF-001` ..."
}
```
