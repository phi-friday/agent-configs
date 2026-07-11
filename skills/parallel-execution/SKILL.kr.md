---
name: parallel-execution
description: "독립적인 작업, 파일, 실패, 서브시스템, 리뷰, 조사, 구현 slice가 둘 이상일 때. Use when work has two or more independent tasks, files, failures, subsystems, reviews, investigations, or implementation slices that can proceed without shared state or sequential dependency."
---

# Parallel Execution

parallel agent를 사용해 wall-clock time을 줄이되, scope, quality, integration 통제는 잃지 않는다.

## Non-Negotiables

```text
독립적인 작업만 PARALLELIZE한다.
모든 SUBAGENT는 SELF-CONTAINED CONTRACT를 받는다.
CONTROLLER가 통합과 최종 검증을 소유한다.
한 wave의 독립 task는 한 번의 `task` 호출에서 여러 `tasks[]`로 dispatch한다.
사용자 explicit parallelize 요청은 여러 번의 task 호출이나 단순 tool 병렬 호출로 대신할 수 없다.
현재 `task` 스키마가 지원하지 않는 `model:` 등은 넣지 않는다.
```

불명확한 같은 문제에 여러 agent를 던져놓고 수렴하길 기대하지 않는다. 먼저 분해한다.

## 보조 reference

이 파일은 실행 checklist로 유지한다. 필요할 때 supporting reference를 연다.

- `references/task-decomposition.md` — 무엇을 병렬로 실행하고 무엇을 순차화해야 하는지 결정.
- `references/subagent-prompts.md` — scope, constraints, output contract가 있는 self-contained assignment 작성.
- `references/review-integration.md` — agent output 검토, conflict 해결, 통합 결과 검증.

## 사용 시점

다음에 사용한다.

- 여러 독립 implementation task
- 서로 다른 file 또는 subsystem으로 묶이는 failure
- 독립적인 codebase investigation
- 별도 artifact에 대한 parallel review
- 겹치지 않는 파일의 mechanical edit
- task들이 서로의 output을 기다리지 않는 plan execution

다음에는 사용하지 않는다.

- 한 task가 다른 task가 소비할 API, schema, contract를 정의할 때
- agent들이 같은 file 또는 shared state를 수정해야 할 때
- 여러 failure의 root cause가 공통일 수 있을 때
- 문제가 아직 안전하게 나눌 만큼 명확하지 않을 때
- 구현 전에 하나의 coherent design decision이 필요할 때

## Phase 1 — 독립성 매핑

dispatch 전에 작업을 domain과 dependency로 묶고, **pre-flight conflict gate**를 한 번 수행한다.

각 candidate task에 대해 확인한다.

- 정확한 file 또는 subsystem
- goal과 non-goal
- 다른 task와 API/schema/output overlap
- 다른 task에 대한 dependency
- expected output
- 다른 agent 결과를 보지 않고도 성공할 수 있는지
- 다른 task와 conflict 가능성이 있는지

앞에서 제공한 context만으로 올바르게 완료할 수 있는 task만 병렬화한다.

게이트에서 overlap이 보이면:

- 도메인별로 나눈다
- 의존형 task를 먼저 완료 후 다음 wave로 순차 dispatch
- 독립 task만 묶어 한 wave로 보낸다

결정 규칙은 `references/task-decomposition.md`를 사용한다.

## Phase 2 — Focused Contracts 작성

각 subagent assignment는 self-contained여야 한다.

현재 `task` schema를 정확히 따른다:

- batch `context`: `# Goal`, `# Constraints`, `# Contract`
- 각 `tasks[].assignment`: `# Target`, `# Change`, `# Acceptance`

포함한다.

- target file 또는 symbol
- 구체적 change 또는 investigation goal
- constraints와 non-goals
- 재탐색을 줄이는 context
- acceptance criteria
- expected response format
- project-wide gate, formatter, final verification을 건너뛰라는 지시

subagent에게 큰 plan을 읽고 자기 slice를 추론하게 하지 않는다. 정확한 slice를 추출해서 준다.

assignment template은 `references/subagent-prompts.md`를 사용한다.

큰 task brief는 message에 붙여넣지 말고 `local://...` 파일 handoff로 전달한다.

## Phase 3 — 병렬 Dispatch

독립 task를 함께 dispatch한다.

각 assignment는 안전하게 통합할 수 있을 만큼 좁게 유지하되, 독립적인 fan-out 전체를 한 batch로 dispatch한다. 임의의 batch 크기를 맞추려고 작업을 순차화하지 않는다. 실제 dependency, shared contract, 또는 도구의 concurrency 경계가 있을 때만 wave를 나눈다.

독립성 규칙:

- dependency 있는 task는 wave를 나눠 순차 dispatch한다
- 순수 독립 task는 한 번의 `task` 호출에서 여러 `tasks[]`로 dispatch한다

controller가 책임진다:
- subagent 질문에 답하기
- scope drift 방지
- overlap 발견 시 조정
- follow-up work를 순차화할지 결정
- todo로 status 추적

Subagent status 처리:

- **DONE**: output과 changed files를 검토한다.
- **DONE_WITH_CONCERNS**: work를 받아들이기 전에 concern을 확인한다.
- **NEEDS_CONTEXT**: 누락 context를 제공하거나 task를 좁힌다.
- **BLOCKED**: context 추가, task 축소, approach 변경, 순차화 중 하나를 바꾼다.

blocked agent에게 같은 조건으로 재시도만 강요하지 않는다.

## Phase 4 — Review 및 통합

agent들이 돌아오면 더 수정하기 전에 모든 결과를 읽는다.

확인한다.

- 각 task가 acceptance criteria를 만족했는가?
- agent가 scope를 넘었는가?
- 두 agent가 같은 file 또는 contract를 수정했는가?
- 한 결과가 다른 결과를 무효화했는가?
- 중복 abstraction 또는 inconsistent naming이 생겼는가?
- 이제 순차화해야 하는 follow-up task가 있는가?

큰, production 영향이 큰 slice는 필요 시 read-only reviewer를 한 번 dispatch할 수 있다.

리뷰 입력은 로컬 handoff 계약으로 전달한다:

- task brief 파일 (`local://...` 또는 `artifact://...`)에 정확한 target/scope 및 제약을 기재
- implementer report 파일 (`local://...` 또는 `artifact://...`)에 finding과 근거 evidence를 기재
- review package 파일 (`local://...` 또는 `artifact://...`)에 정확한 target/evidence와 diff/evidence 번들 제공

모든 작은 task에 reviewer를 강제하지 않는다.

spec compliance가 code quality보다 먼저다. 먼저 assignment와 일치하는지 확인하고, 그 다음 maintainability를 검토한다.

통합 gate는 `references/review-integration.md`를 사용한다.

## Phase 5 — 중앙 검증

subagent는 final verification을 소유하지 않는다. controller가 combined work를 통합한 뒤 final check를 실행한다.

사용자가 더 넓은 검증을 요청하지 않았다면 changed scope에 관련된 test/check만 실행한다.

최종 output에는 다음을 적는다.

- 무엇을 병렬화했는가
- 무엇이 변경됐는가
- 무엇을 검증했는가
- 남은 risk 또는 follow-up decision이 있는가

## Red Flags

다음이 보이면 멈추고 다시 묶는다.

- agent들이 서로의 미완성 output을 필요로 한다
- 여러 agent가 같은 file을 수정해야 한다
- assignment가 file boundary 없이 “update all” 또는 broad glob을 사용한다
- subagent prompt가 숨은 conversation history에 의존한다
- agent가 scope 밖 work를 반환한다
- agent 질문이 누락 requirement를 드러낸다
- 두 agent가 같은 concept를 다르게 해결한다
- review가 spec gap을 찾았는데도 integration을 진행한다
- agent가 “통과했다”고 해서 final verification을 건너뛴다

parallel execution은 coordination technique이지 ownership 대체물이 아니다.
