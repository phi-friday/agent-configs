# Mode Selection

Resolve the user's latest request before doing review work.

## Classifier

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

Recommended default: `Draft review only`.

After the user answers:

- If Draft is selected, continue Draft mode in the same turn.
- If Submit is selected, validate the Submit mode prerequisite, then continue Submit mode.
- If the typed answer gives a third path, follow it only when it is specific enough and does not bypass safety gates.

## Do Not Infer Publication Permission

These are not approval to submit GitHub comments:

- the user invoked this skill
- the user said `review this PR`
- the user selected Submit mode
- the user selected `PRF-*` IDs
- a previous message sounded positive

GitHub mutation still requires the exact payload preview and `ask` approval gate from `payload-approval.md`.
