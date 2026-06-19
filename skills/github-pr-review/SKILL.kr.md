---
name: github-pr-review
description: "PR 리뷰 초안 작성, PRF-* 항목 제출, GitHub review payload 검수/승인. Use when drafting a GitHub pull request review, or when submitting selected findings from an existing PR review draft."
---

# GitHub PR Review

GitHub pull request를 explicit mode로 review한다. Draft, selected draft finding submit, 또는 user가 명시적으로 opt-in한 YOLO draft-and-submit/request-changes/approve를 수행한다.

## Non-Negotiables

```text
REVIEW 작업 전 DRAFT VS SUBMIT VS YOLO MODE를 먼저 결정.
DRAFT MODE 중 GITHUB MUTATION 없음.
YOLO MODE의 SAME-RUN DRAFT 외에는 기존 PRF-* DRAFT 없이 SUBMISSION 없음.
explicit YOLO mode 밖에서는 user approval bypass 금지.
`scripts/detect_mode.py`가 mode `yolo`를 반환할 때만 YOLO MODE.
NORMAL SUBMIT MODE 중 새 FINDING 없음.
YOLO MODE에서 ACTIONABLE FINDING이 0개면 APPROVAL이 금지되지 않는 한 PR을 APPROVE한다.
YOLO MODE는 REVIEW EVENT를 판단한다.
YOLO MODE에서 blocking Must Fix가 있으면 REQUEST_CHANGES를 사용한다.
항상 한국어로 답변.
```

## Supporting References

현재 mode에 필요한 reference만 연다.

- `references/mode-selection.md` — user intent를 Draft, Submit, YOLO, ambiguous로 분류.
- `references/draft-mode.md` — read-only PR review workflow와 draft output contract.
- `references/submit-mode.md` — selected finding submission workflow와 GitHub mutation guardrail.
- `references/yolo-mode.md` — user inspection 없는 same-run draft와 review-event submission/approval workflow.
- `scripts/detect_mode.py` — explicit `draft`/`submit`/`yolo` mode keyword classifier.
- `references/payload-approval.md` — normal Submit mode의 exact preview와 mandatory `ask` approval gate.

## Use When

다음에 사용한다.

- GitHub pull request review draft 작성
- PR number, branch name, current branch에서 PR resolve
- 추후 제출할 수 있는 stable review finding ID 생성
- existing draft의 selected `PRF-*` finding 제출
- explicit `yolo` draft-and-submit/request-changes/approve를 한 번에 수행
- future reviewer를 위한 excluded review context 보존

GitHub PR context가 없는 generic code review workflow에는 사용하지 않는다.

## Step 1 — Resolve Mode From User Input

PR inspect, diff read, payload 준비 전에 user의 latest request를 먼저 분류한다.

```text
첫 단어가 정확히 `draft` 또는 `draft,`
    └─ Draft mode

첫 단어가 정확히 `submit` 또는 `submit,`
    └─ Submit mode

첫 단어가 정확히 `yolo` 또는 `yolo,`
    └─ YOLO mode: payload approval 없이 draft, review event 선택, submit/approve를 한 번에 수행

사용자가 review analysis를 원하는지 GitHub publication을 원하는지 불명확함
    └─ Ambiguous: ask tool로 묻고, 선택된 mode를 이어서 수행
```

Exact classifier는 `references/mode-selection.md`를 사용한다. 먼저 `scripts/detect_mode.py`를 실행한다. Explicit `draft`, `submit`, `yolo` keyword는 LLM inference보다 우선하고, explicit keyword가 없으면 기존 intent resolution으로 fallback한다.

Mode가 ambiguous하면 일반 prose로 묻고 종료하지 않는다. `ask` tool로 mode choice를 받고, answer 뒤 선택된 workflow를 계속 수행한다.

## YOLO Mode Summary

YOLO mode는 Draft mode를 실행한 뒤 GitHub Review API event를 직접 판단한다. Clean PR은 approve하고, high-confidence blocking Must Fix는 request changes로 제출하며, 그 외에는 comment한다.

Hard boundaries:

- user의 latest input에 대해 `scripts/detect_mode.py`가 mode `yolo`를 반환할 때만 사용한다.
- uppercase `YOLO`, `yolox` 같은 suffix, `XXX yolo` 같은 later word, “auto”, “바로 제출”, “검수 없이” 같은 synonym에서 YOLO mode를 infer하지 않는다. `yolo,`만 punctuation form으로 허용한다.
- payload approval을 위해 `ask` tool을 호출하지 않는다.
- submit 전 PR context, anchor, file path, payload shape, GitHub mutation scope는 여전히 validate한다.
- selected finding을 faithful하게 submit할 수 없으면 mutation 전에 멈추고 blocker를 보고한다.
- same-run draft에서 actionable finding이 없고 validation에서 failing/pending merge-blocking check가 보이지 않으면, 같은 request가 approval을 명시적으로 금지하지 않는 한 approval 요청 없이 정확히 하나의 `APPROVE` review를 submit한다.
- selected finding 중 high-confidence blocking `Must Fix`가 있으면 approval 요청 없이 정확히 하나의 `REQUEST_CHANGES` review를 submit한다.
- non-blocking finding, uncertain evidence, pending/unclear validation, explicit comment-only behavior에는 `COMMENT`를 사용한다.

YOLO mode는 같은 YOLO request에서 ID/category include/exclude가 명시되지 않는 한 모든 actionable draft finding을 submit한다. User가 `COMMENT` vs `REQUEST_CHANGES`를 미리 고를 필요는 없고, `references/yolo-mode.md`의 Event Mode가 결정한다.

Full workflow는 `references/yolo-mode.md`를 사용한다.

## Global Language Rule

- 항상 user에게 한국어로 답변한다.
- Draft finding은 기본적으로 한국어다.
- GitHub review comment는 기본적으로 한국어다.
- 현재 invocation에서 user가 명시적으로 English를 요청한 경우에만 GitHub comment를 영어로 쓴다.
- file path, function name, API, command, branch name, `PRF-*` ID는 그대로 둔다.

## Draft Mode Summary

Draft mode는 PR을 분석하고 user에게만 finding을 보고한다.

Hard boundaries:

- GitHub를 절대 mutate하지 않는다.
- submit, approve, request changes, comment, edit, merge, close, reopen, label, assign을 하지 않는다.
- `gh pr review`, `gh pr comment`, `gh pr merge`, `gh pr edit`, mutating `gh api`를 실행하지 않는다.
- `git commit` 또는 `git push`로 local change를 publish하지 않는다.

Draft mode는 다음을 해야 한다.

1. non-mutating check로 local repository context 확인
2. target PR resolve
3. diff보다 existing PR context 먼저 읽기
4. diff와 validation evidence inspect
5. stable `PRF-*` ID가 있는 actionable finding 보고
6. 모든 actionable finding에 submission target 부여: `inline`, `file`, `general`

Full workflow와 output format은 `references/draft-mode.md`를 사용한다.

## Draft Finding Contract

나중에 제출될 수 있는 모든 actionable finding은 다음을 포함해야 한다.

```md
- `PRF-001` [Must Fix] <summary>
  - Submission target: inline | file | general
  - Inline anchor: `path/to/file.ts:42` (`side: RIGHT`) <!-- inline only -->
  - File: `path/to/file.ts` <!-- file only -->
  - Risk: <what can go wrong>
  - Suggested fix: <concrete fix>
```

Rules:

- 새 ID 부여 전에 existing `PRF-*` ID를 수집한다.
- 새 ID는 관찰된 가장 큰 numeric suffix 다음부터 시작한다.
- 다른 concern에 ID를 재사용하지 않는다.
- metadata, context summary, validation observation, final assessment에는 ID를 부여하지 않는다.
- faithful inline diff anchor가 없으면 `Inline anchor: unavailable`을 쓰고 이유를 설명한다.

## Submit Mode Summary

Submit mode는 existing draft에서 selected finding을 publish한다. 두 번째 review pass가 아니다.

Submit mode는 current conversation에 actionable `PRF-*` ID가 있는 completed draft가 필요하다.

Hard boundaries:

- 새 finding을 만들지 않는다.
- draft finding을 materially rewrite하거나 strengthen하지 않는다.
- Diff는 selected anchor와 file path validation에만 inspect한다.
- `ask`를 통한 exact payload approval 뒤 정확히 하나의 GitHub PR review만 submit한다.
- approve, merge, close, reopen, label, assign, edit, commit, push를 하지 않는다.

Submit mode는 다음을 해야 한다.

1. usable draft 존재 확인
2. user instruction에서 included/excluded `PRF-*` ID resolve
3. selected submission target validate
4. submitted되지 않는 finding의 excluded review context 보존
5. exact inline comment, top-level body, API payload compose
6. exact preview 표시
7. exact payload approval을 위해 `ask` tool 호출
8. approval 뒤에만 submit
9. 관찰된 submission result 보고

Selection, validation, excluded-context, result rule은 `references/submit-mode.md`를 사용한다.
Normal Submit mode의 approval preview와 `ask` gate는 `references/payload-approval.md`를 사용한다.
