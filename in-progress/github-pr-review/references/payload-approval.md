# Payload Approval

Submit mode requires exact content approval through the `ask` tool before any GitHub-mutating command runs.

Selecting IDs is not approval to submit. Submit wording in the user's request is not approval. Ordinary chat text is not approval.

## Required Preview

Before calling `ask`, show the exact payload that will be posted.

Use this structure:

````md
## 리뷰 제출 전 검수

- PR: #<number> <url>
- 제출 예정 항목: <PRF-001, PRF-003>
- 인라인 항목: <PRF-001 or 없음>
- 상위 본문 항목: <PRF-003 or 없음>
- 제외 항목: <PRF-002 or 없음>
- 제출 방식: <review comments | request changes>
- 제출 언어: <Korean by default; English only if explicitly requested>
- 인라인 코멘트 수: <n>
- 제외 컨텍스트: <details block included | 없음>
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

With inline comments:

```json
{
  "event": "COMMENT",
  "body": "인라인 리뷰 코멘트를 남겼습니다.",
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
  "body": "<selected file/general findings>"
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
