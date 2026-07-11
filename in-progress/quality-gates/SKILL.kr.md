---
name: quality-gates
description: "완료, 수정됨, 통과, 준비됨, 리뷰됨, 병합가능, 커밋, PR, 버그 종료, 서브에이전트 결과 수락, 성공 보고 전. Use before claiming work is done, fixed, passing, ready, reviewed, mergeable, or before committing, opening a PR, closing a bug, accepting subagent work, or reporting success."
---

# Quality Gates

confidence, intent, agent report만으로 성공을 선언하지 않는다. fresh evidence가 증명하는 것만 말한다.

## Non-Negotiables

```text
FRESH VERIFICATION EVIDENCE 없이 COMPLETION CLAIM 없음.
REVIEW가 필요한 변경은 REVIEW 없이 MERGE-READY CLAIM 없음.
REVIEW FEEDBACK을 BLIND IMPLEMENTATION하지 않음.
```

claim보다 evidence가 먼저다. review는 ceremony가 아니라 quality gate다. feedback은 performative하게 수용하지 않고 기술적으로 평가한다.

## Supporting References

이 파일은 실행 checklist로 유지한다. 필요할 때 supporting reference를 연다.

- `references/verification-evidence.md` — claim을 proof에 매핑하고 command output을 읽는 기준.
- `references/code-review-request.md` — focused code review를 언제/어떻게 요청할지.
- `references/review-feedback-handling.md` — review feedback을 엄격하게 평가하고 적용하는 방법.

## Use When

다음 전에 사용한다.

- done, fixed, passing, ready, complete, clean, reviewed, mergeable이라고 말하기
- task 완료 표시
- 의미 있는 변경 뒤 다음 task로 이동
- commit, PR, merge request 생성
- subagent work를 complete로 받아들이기
- code review feedback에 응답하기
- bug를 닫거나 regression이 고쳐졌다고 말하기

## Phase 1 — Identify The Claim

말하기 전에 하려는 claim을 정확히 식별한다.

예시:

- “tests pass”
- “bug is fixed”
- “requirements are met”
- “review feedback is addressed”
- “ready to merge”

claim이 모호하면 검증 가능한 문장으로 바꾼다.

나쁨:

```text
Looks good.
```

나음:

```text
Targeted unit tests pass, and the original repro no longer fails.
```

## Phase 2 — Match Claim To Evidence

모든 claim에는 구체적 proof가 필요하다.

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

claim이 명시적으로 subset에 한정된 것이 아니라면 편한 subset이 아니라 관련 full command를 실행한다.

claim-to-proof 규칙은 `references/verification-evidence.md`를 사용한다.

## Phase 3 — Run And Read Verification

현재 상태에서 fresh verification을 실행한다.

그 다음 읽는다.

- exit code
- failure count
- 관련 있을 때 skipped tests
- warnings 또는 errors
- command가 claim을 실제로 cover했는지
- output이 truncated 또는 filtered됐는지

verification이 실패하면 실제 failure를 보고한다. “almost done”으로 완화하지 않는다.

verification이 partial이면 claim scope를 정직하게 제한한다.

```text
Targeted parser tests pass. Full suite was not run.
```

## Phase 4 — Request Review When Warranted

다음에는 review를 요청한다.

- major feature
- security, data, migration, auth, payments, infra change
- complex bug fix
- broad refactor
- production code에 영향을 주는 subagent output
- merge되거나 complete로 handoff될 work

review request에는 아래를 포함한다.

- 정확한 review target (아래 중 하나):
  - `[BASE]..[HEAD]` commit 범위
  - GitHub PR (`https://github.com/<owner>/<repo>/pull/<n>` 또는 `owner/repo#n`)
  - 명시적 파일 집합(경로, glob, 혹은 hunk)
  - artifact URI
- 무엇이 바뀌었는지
- requirements 또는 plan
- review focus
- known risks 또는 uncertainty
- reviewer 계약:
  - 기본은 read-only
  - hidden conversation에서 context 추론 금지
  - requirements, focus, risks를 요청 본문 안에 self-contained하게 전달
- finding 결과 형식 요구:
  - 각 finding에 severity, `file:line` 또는 artifact 증거, risk, required action을 모두 포함

review request template과 finding/증거 형식은 `references/code-review-request.md`를 사용한다.

## Phase 5 — Handle Review Feedback

어떤 item도 구현하기 전에 전체 feedback을 읽는다.

각 item마다:

1. technical request를 이해한다
2. codebase에 비춰 검증한다
3. fix, reject with reason, ask clarification 중 결정한다
4. 한 item 또는 coherent group을 구현한다
5. 영향받은 behavior를 테스트한다
6. evidence와 함께 item을 resolved로 표시한다

review comment를 blind implementation하지 않는다. performative agreement도 하지 않는다. social comfort보다 technical correctness가 우선이다.

multi-item feedback과 pushback 규칙은 `references/review-feedback-handling.md`를 사용한다.

## Phase 6 — Final Report

verification과 필요한 review gate가 끝난 뒤에만 보고한다.

```md
## Status

## Evidence

## Review

## Changes

## Remaining Risk
```

보고의 모든 문장은 observed evidence로 뒷받침되어야 한다.

실행하지 않은 것은 실행하지 않았다고 말한다. change가 작아서 review를 요청하지 않았다면 이유를 적는다.

## Red Flags

다음 말을 하려 하면 멈추고 verify한다.

- “done”
- “fixed”
- “passes”
- “looks good”
- “should work”
- “probably”
- “ready”
- “review addressed”
- “agent completed it”

다음이면 멈추고 재평가한다.

- 이전 run을 믿고 있다
- subagent가 success라고 했지만 evidence를 직접 확인하지 않았다
- tests는 pass하지만 requirements를 확인하지 않았다
- review feedback이 불명확하다
- review suggestion이 compatibility를 깨뜨릴 수 있다
- 여러 feedback item을 테스트 없이 batch 처리하고 싶다
- 기술적으로 평가하지 않고 감사/동의 표현을 하고 싶다

quality gate는 false completion을 막기 위해 존재한다.
