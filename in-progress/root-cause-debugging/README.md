# root-cause-debugging

`root-cause-debugging`은 버그, 실패, 성능 저하, flaky 동작, 통합 문제를 수정하기 전에 root cause를 증거로 확인하도록 강제하는 in-progress 스킬이다.

이름은 `systematic-diagnosis`보다 트리거와 행동이 더 분명한 `root-cause-debugging`으로 잡았다. 이 스킬의 실제 사용자는 “진단”이라는 추상 명사보다 “root cause를 찾아서 debugging한다”는 동작을 더 쉽게 떠올릴 수 있다.

## 파일 구성

- `SKILL.md`: 실제 스킬 정의. description은 영어와 한국어를 모두 포함해 영어/한국어 요청 모두에서 트리거될 수 있게 한다.
- `skill.kr.md`: `SKILL.md`의 한국어 번역본. 한국어로 내용을 검토하거나 수정할 때 기준으로 사용한다.
- `README.md`: 레퍼런스 조사, 누락 여부, 조합 결정을 설명한다.

## 조합 방식

```text
diagnose                  빠르고 결정적인 feedback loop + ranked hypotheses + regression proof
systematic-debugging      root cause 우선 + pattern comparison + shortcut 방지

root-cause-debugging      reproduce → observe → trace → hypothesize → instrument → fix → prove
```

이 스킬은 이미 관찰된 failure를 다룬다. 새 설계의 사전 검증 절차는 이 스킬에 넣지 않았다.

## 원본 레퍼런스 누락 조사

아래 항목을 다시 확인했고, 스킬 본문 또는 README에 반영했다.

| 원본 | 확인한 핵심 | 반영 위치 | 처리 |
|---|---|---|---|
| `mattpocock/skills/skills/engineering/diagnose/SKILL.md` | feedback loop가 핵심, 재현, 3–5개 ranked hypotheses, tagged debug logs, perf 측정, regression test, original repro 재실행 | `SKILL.md` Phase 1, 2, 4, 5, 6, 7 | 핵심 절차 반영 |
| `diagnose/scripts/hitl-loop.template.sh` | manual step이 불가피할 때도 structured prompt/capture loop를 만든다 | `SKILL.md` Phase 1, Phase 5 | 스크립트 복사는 하지 않고 technique만 반영 |
| `systematic-debugging/SKILL.md` | no fixes without root cause, error/stack trace/recent changes 확인, boundary evidence, pattern comparison, one-variable testing, failed fixes 후 architecture 재검토, red flags | `SKILL.md` Non-Negotiables, Phase 2, 3, 4, 6, Red Flags | 핵심 절차 반영 |
| `systematic-debugging/root-cause-tracing.md` | symptom에서 caller/input/source로 뒤로 추적, bad value origin 찾기, source fix | `SKILL.md` Phase 3 | 별도 파일 대신 tracing 절차를 본문에 통합 |
| `systematic-debugging/defense-in-depth.md` | invalid data는 source 확인 후 layer별 validation/guard/observability로 구조적으로 막는다 | `SKILL.md` Phase 6 | 기본 반사 행동이 아니라 조건부 보강으로 제한 |
| `systematic-debugging/condition-based-waiting.md` | flaky/timing bug에서는 guessed sleep이 아니라 condition을 기다린다 | `SKILL.md` Phase 5 | timing/flaky probe 규칙으로 통합 |
| `systematic-debugging/condition-based-waiting-example.ts` | waitForEvent / waitForEventCount / waitForEventMatch류의 domain-specific wait helper | `SKILL.md` Phase 5 | 구체 코드 복사 없이 원칙만 반영 |
| `systematic-debugging/find-polluter.sh` | unwanted state/file을 만드는 test를 bisection으로 찾는다 | `SKILL.md` Phase 1, Phase 5 | state pollution bisection으로 반영 |
| `systematic-debugging/CREATION-LOG.md` | skill은 pressure-resistant language, anti-patterns, phase checklist가 있어야 한다 | `SKILL.md` Non-Negotiables, Red Flags, phase 구조 | 스킬 형태 개선에 반영 |
| `systematic-debugging/test-*.md` | 압박, sunk cost, authority pressure에서도 shortcut을 거부해야 한다 | `SKILL.md` Use When, Non-Negotiables, Red Flags | pressure-resistant phrasing으로 반영 |

누락으로 판단해 보강한 부분:

- state pollution / polluter bisection
- human-in-the-loop loop의 구조화된 capture 개념
- pressure-resistant skill shape 자체
- “모르면 모른다고 말하고 조사한다”는 규칙
- error/warning/stack trace를 끝까지 읽는 규칙
- working example과 broken path의 차이를 전부 목록화하는 규칙

## 레퍼런스별로 가져온 요소

### `diagnose`

가져온 요소:

- “debugging은 feedback loop가 90%”라는 우선순위
- failing test, CLI, HTTP, browser automation, replay, harness, stress, differential, bisection, HITL loop의 재현 전략
- flaky bug에서는 먼저 재현율을 올리는 방식
- 3–5개 가설을 먼저 만들고 prediction을 붙이는 방식
- debug log에 cleanup prefix를 붙이는 규칙
- performance regression은 logging보다 measurement/profiling/bisection을 우선하는 태도
- correct seam에서 failing regression test를 먼저 만들고, 마지막에 original repro를 다시 실행하는 규칙

조정한 점:

- 원본 shell template은 복사하지 않고 “structured prompt loop + machine-readable capture”라는 사용 원칙만 넣었다.
- hypothesis 목록을 사용자 승인 gate로 만들지 않고, 진행 중 evidence artifact로 다루게 했다.

### `systematic-debugging`

가져온 요소:

- root cause 확인 전 fix 금지
- error message, stack trace, reproduction, recent changes, environment/config 확인
- multi-component boundary에서 input/output/config/state를 확인하는 방식
- symptom point가 아니라 source를 고치는 원칙
- working example/reference와 broken path를 비교하는 pattern analysis
- 한 번에 하나의 변수만 검증하는 scientific method
- 반복된 fix 실패 후 architecture/fundamental model을 재검토하는 규칙
- shortcut과 rationalization을 직접 겨냥하는 red flags

조정한 점:

- 원본은 single hypothesis 중심이지만, anchor 방지를 위해 먼저 3–5개 ranked hypotheses를 만든 뒤 하나씩 검증하도록 합쳤다.
- 특정 skill system에 의존하는 cross-reference는 제거하고 일반 절차로 풀었다.

### Supporting references

- `root-cause-tracing.md`는 Phase 3의 backward tracing 절차로 통합했다.
- `defense-in-depth.md`는 Phase 6의 조건부 layer protection으로 통합했다.
- `condition-based-waiting.md`와 example은 Phase 5의 flaky/timing probe 규칙으로 통합했다.
- `find-polluter.sh`는 Phase 1/5의 state pollution bisection으로 통합했다.
- pressure tests와 creation log는 phase checklist, hard gate, red flags의 문체와 구조에 반영했다.

## 최종 스킬 안에서의 역할 분담

```text
1. Non-Negotiables
   - root cause 전 fix 금지
   - reproduction 전 root cause 주장 금지
   - original scenario 재실행 전 완료 금지

2. Build the Feedback Loop
   - diagnose의 핵심 loop 구축 전략
   - polluter/state bisection과 HITL capture 보강

3. Reproduce and Observe
   - exact symptom capture
   - error/stack/recent-change/environment 확인

4. Trace the Failure Boundary
   - backward tracing
   - multi-component boundary evidence
   - working vs broken comparison

5. Ranked Hypotheses
   - 3–5개 가설로 anchoring 방지
   - one-variable-at-a-time 검증

6. Precise Instrumentation
   - debugger/profiler 우선
   - tagged temporary logs
   - perf/flaky/state/manual 전용 probe

7. Fix the Root Cause
   - correct seam regression test
   - source-level minimal fix
   - 조건부 defense-in-depth

8. Prove, Clean Up, Report
   - original repro 재실행
   - regression coverage 확인
   - temporary instrumentation 제거
   - root cause/evidence/fix/verification 보고
```

## 의도적으로 제외한 것

- 특정 shell script, helper implementation, test fixture의 직접 복사
- 특정 skill system 이름에 의존하는 cross-reference
- real-world impact 수치
- 프로젝트 고유 예시
- root cause 확인 전의 retry, fallback, timeout, warning suppression 권장
- 모든 bug에 architecture refactor를 권장하는 방식

## 라이선스 메모

레퍼런스 저장소들은 MIT License다. 원문, 체크리스트, 템플릿, 스크립트를 실질적으로 복사하거나 수정해 포함하는 경우 `NOTICE.md`의 고지를 유지해야 한다.
