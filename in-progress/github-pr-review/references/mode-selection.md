# Mode Selection

Resolve the user's latest request before doing review work. The possible modes are Draft, normal Submit, YOLO, and Ambiguous.

## Classifier

Use YOLO mode only when `scripts/detect_yolo_mode.py` confirms the user's latest raw input has `yolo` as its exact first word.

Mandatory classifier:

```sh
python scripts/detect_yolo_mode.py -- "<raw latest user input>"
```

Only exit code `0` and JSON field `"is_yolo": true` permit YOLO mode. Exit code `1` or `"is_yolo": false` means normal Draft/Submit/Ambiguous handling.

The script's rule is case-sensitive and word-exact: first whitespace-delimited word equals lowercase `yolo`. It accepts `yolo` and `yolo PR #123`. It rejects `YOLO`, `yolox`, `yolomode`, `yolo모드`, `yolo,`, and `XXX yolo`.

Do not infer YOLO mode from uppercase, suffixes, later words, or synonyms such as `auto`, `자동`, `한번에`, `바로 제출`, `검수 없이`, or `no approval`.

Examples:

- `yolo review PR #123`
- `yolo #123 리뷰하고 올려`

YOLO mode means: run Draft mode, then submit every selected actionable draft finding in the same run without payload approval. Use `references/yolo-mode.md`.

Use Draft mode when the user asks to analyze or review a PR without explicit publication wording.

Examples:

- `review this PR`
- `PR #123 봐줘`
- `이 브랜치 리뷰해줘`
- `문제 있는지 확인해줘`
- a PR number or branch name by itself

Use Submit mode when the user asks to publish selected draft findings to GitHub.

Examples:

- `PRF-001 올려`
- `PRF-002 제외하고 제출해`
- `submit the review comments`
- `post all findings`
- `request changes로 제출해`

Treat these as Submit mode only after validating that a usable draft exists in the current conversation. If no usable draft exists, report that the user must run Draft mode first.

## Ambiguous Requests

A request is ambiguous when both interpretations are plausible.

Examples:

- `리뷰 코멘트 달아줘`
- `이거 리뷰해줘, 필요하면 올려줘`
- `저번 것 처리해줘`
- `코멘트 작성해줘`

When ambiguous, use the `ask` tool. Do not ask in ordinary prose and stop.

Ask one mode-selection question with at least these options:

1. `Draft review only` — Analyze the PR and report findings in chat without writing to GitHub.
2. `Submit existing draft findings` — Publish selected `PRF-*` findings from an existing draft after exact payload approval.
3. `YOLO draft and submit` — Valid only if `detect_yolo_mode.py` returns `"is_yolo": true` for the original user input; otherwise explain that YOLO requires first-word `yolo` and do not select it.

Recommended default: `Draft review only`.

After the user answers:

- If Draft is selected, continue Draft mode in the same turn.
- If Submit is selected, validate the Submit mode prerequisite, then continue normal Submit mode.
- If YOLO is selected, run `scripts/detect_yolo_mode.py` against the original user input first. If it does not return `"is_yolo": true`, report that YOLO mode requires first-word `yolo` and fall back to Draft or ask again.
- If the typed answer gives a third path, follow it only when it is specific enough and does not bypass safety gates.

## Do Not Infer Publication Permission

These are not approval to submit GitHub comments:

- the user invoked this skill
- the user said `review this PR`
- the user selected Submit mode
- the user selected `PRF-*` IDs
- a previous message sounded positive
- the user asked for automatic submission without first-word `yolo`

Outside first-word YOLO mode, GitHub mutation still requires the exact payload preview and `ask` approval gate from `payload-approval.md`.
