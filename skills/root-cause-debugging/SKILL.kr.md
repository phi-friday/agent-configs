---
name: root-cause-debugging
description: "버그, 테스트 실패, 빌드 실패, 통합 실패, flaky 동작, 성능 저하, 장애, 예상 밖 동작이 나타났을 때 사용한다. 수정 전에 피드백 루프를 만들고, 보고된 실패를 재현하고, 실패 경계를 추적하고, 정상 패턴과 비교하고, 반증 가능한 가설을 세우고, 한 번에 하나의 변수만 계측하고, root cause를 고치고, 회귀 커버리지를 추가하고, 원래 시나리오가 고쳐졌음을 증명한다. English: Use when a bug, test failure, build failure, integration failure, flaky behavior, performance regression, incident, or unexpected behavior appears. Before fixing, build a feedback loop, reproduce the reported failure, trace the failure boundary, compare working patterns, form falsifiable hypotheses, instrument one variable at a time, fix the root cause, add regression coverage, and prove the original scenario is fixed."
---

# Root-Cause Debugging

그럴듯한 수정이 아니라 증거로 디버깅한다.

이것은 technique skill이다. 각 phase가 이미 충족됐음을 명시적으로 증명할 수 없다면 순서대로 따른다. shortcut이 명백해 보일수록 멈추고 증거를 모은다.

## Non-Negotiables

```text
ROOT CAUSE 전에 FIX 없음.
재현 없이 ROOT CAUSE 없음.
원래 시나리오 통과 없이 완료 없음.
```

증상을 먼저 patch하지 않는다. 실패를 재현하고 원인이 증거로 뒷받침되기 전에는 retry, timeout, fallback, warning suppression, config change, broad refactor, “while here” cleanup을 추가하지 않는다.

## Supporting References

이 파일은 실행 checklist로 유지한다. 아래 파일은 해당 technique이 필요할 때만 연다.

- `references/feedback-loops.md` — reproduction loop 선택과 개선.
- `references/root-cause-tracing.md` — bad value, state, component boundary를 source까지 추적.
- `references/condition-based-waiting.md` — fake timer를 먼저 쓰고, real async work가 필요할 때 condition-based wait를 사용.
- `references/defense-in-depth.md` — source를 확인한 뒤 layered guard 추가.
- `references/scripts/hitl-loop.template.sh` — manual reproduction이 불가피할 때 절차화.
- `references/scripts/find-polluter.template.sh` — unwanted state를 만드는 test/command 격리.

## Use When

다음에 사용한다.

- 실패하는 테스트, flaky 테스트, 오염된 test state
- build failure와 CI-only failure
- runtime exception, wrong output, missing data, broken UI, unexpected state
- service, queue, job, CI, auth, storage, deploy, external API 사이의 integration failure
- performance regression, hang, timeout, memory growth, resource surge
- 이미 한 번 수정했는데 살아남은 failure
- 증명 전에 “아마 X일 것”이라고 말하고 싶은 순간

압박은 process를 완화하지 않는다. 압박은 shortcut fix가 가장 큰 피해를 내는 상황이다.

## Phase 1 — Build the Feedback Loop

사용자가 보고한 실패에 대한 agent-runnable pass/fail signal을 만든다. loop는 근처 surrogate가 아니라 실제 failing path에 도달해야 한다.

선호 순서:

1. correct seam의 실패 unit, integration, end-to-end test.
2. fixture input과 checked output을 가진 focused command 또는 CLI invocation.
3. local, staging, test server를 향한 HTTP script.
4. DOM, console, network behavior를 assert하는 browser automation.
5. 캡처된 request, event, payload, trace, log, fixture replay.
6. 최소 setup으로 실제 code path를 호출하는 throwaway harness.
7. flaky, timing, concurrency failure를 위한 stress loop.
8. working/broken, old/new, config A/B를 비교하는 differential loop.
9. commit range, data range, dependency version, polluting test를 찾는 bisection loop.
10. manual step이 불가피할 때만 human-in-the-loop prompt script.

loop를 믿기 전에 개선한다.

- **빠르게**: 관련 없는 setup을 제거하고 path를 좁힌다.
- **날카롭게**: “crash 안 남”이 아니라 정확한 증상을 assert한다.
- **결정적으로**: 시간 고정, randomness seed, filesystem 격리, network 동결, concurrency 제어.

flaky bug에서는 먼저 재현율을 올린다. 더 자주 반복하고, 병렬화하고, stress를 추가하고, timing pressure를 넣고, race를 좁혀 추론 가능한 빈도로 실패하게 만든다.

loop를 만들 수 없다면 멈추고 필요한 artifact나 접근권을 정확히 말한다: environment access, log, trace, core dump, HAR file, timestamp가 있는 screen recording, captured payload, temporary instrumentation 허가.

test, CLI, HTTP, browser, replay, stress, differential, bisection, manual loop 중 무엇을 쓸지 고를 때는 `references/feedback-loops.md`를 사용한다.

## Phase 2 — Reproduce and Observe

loop를 실행한다. 실패가 나타나는 것을 본다.

다음 증거를 캡처하고 넘어간다.

- exact error message, stack trace, status code, wrong value, missing event, bad state, screenshot, request/response, query result, timing, memory profile, log excerpt
- 실패가 사용자가 보고한 증상과 같은지
- 안정적으로 재현되는지, flaky라면 어느 정도 비율로 재현되는지
- recent changes: commits, dependency changes, config changes, data migrations, environment differences, deploys, feature flags

error와 warning을 끝까지 읽는다. stack trace, code, line number가 root cause까지의 가장 짧은 경로일 때가 많다.

더 재현하기 쉽다는 이유로 다른 failure를 디버깅하지 않는다.

## Phase 3 — Trace the Failure Boundary

expected behavior가 actual bad behavior로 처음 바뀌는 지점을 찾는다.

deep stack failure에서는 뒤로 추적한다.

```text
symptom
  ↑ immediate failing operation
  ↑ caller and arguments
  ↑ earlier transformation
  ↑ source of invalid state or assumption
```

각 단계에서 묻는다.

```text
이 bad value/state는 어디서 왔는가?
이 function/component가 건드리기 전부터 이미 나빴는가?
어떤 caller, config, environment, lifecycle event, persisted state가 나쁘게 만들었는가?
```

multi-component failure에서는 각 boundary를 확인한다.

```text
component A ──payload/config/state──▶ boundary ──payload/config/state──▶ component B
              expected? actual?                  expected? actual?
```

각 boundary에서 기록한다.

- input과 output
- visible config와 environment
- 읽은 state와 쓴 state
- ordering과 lifecycle assumption
- data가 처음 diverge한 지점

비슷한 working code가 있으면 수정 전에 비교한다. behavior, configuration, dependencies, ordering, environment, data shape, lifecycle, ownership 차이를 모두 나열한다. 증거가 배제하기 전에는 “상관없다”고 버리지 않는다.

bad state가 시작되는 곳을 고친다. 마지막에 폭발한 줄을 고치는 것이 아니다.

failure가 stack 깊은 곳에서 나타나거나 component를 건너거나 working-vs-broken 비교가 필요하면 `references/root-cause-tracing.md`를 사용한다.

## Phase 4 — Form Ranked Hypotheses

어떤 fix도 테스트하기 전에 3–5개 ranked hypothesis를 쓴다.

각 hypothesis는 반증 가능해야 한다.

```text
만약 <cause>가 참이라면, <probe>가 <observable result>를 보여야 한다.
```

좋은 hypothesis는 mechanism과 prediction을 포함한다.

```text
cache key가 locale을 빠뜨렸다면, fr-FR request 뒤의 en-US request가 같은 key를 재사용할 것이다. cache read/write key와 locale을 기록하면 두 요청의 key가 같게 나타난다.
```

한 번에 하나의 hypothesis만 테스트한다. 하나의 probe, 하나의 variable, 하나의 result.

hypothesis가 실패하면 무엇이 배제됐는지 기록하고 다음 hypothesis를 만든다. fix를 쌓지 않는다.

fix attempt가 세 번 실패하면 local bug처럼 계속 다루지 않는다. design을 다시 묻는다: hidden coupling, shared mutable state, invalid ownership, missing seam, fundamentally wrong pattern이 root cause일 수 있다.

시스템의 일부를 이해하지 못했다면 모른다고 말하고 조사한다. 자신 있는 척하지 않는다.

## Phase 5 — Instrument Precisely

instrumentation은 Phase 4의 hypothesis 하나에 답해야 한다.

선호 순서:

1. debugger, REPL, profiler, query plan, trace viewer, runtime inspector
2. hypothesis를 구분하는 targeted boundary logs
3. invariant가 처음 깨지는 곳의 temporary assertions

모든 temporary diagnostic log에는 `[DEBUG-a4f2]` 같은 고유 cleanup prefix를 붙인다.

“전부 logging하고 나중에 찾기”는 하지 않는다. noise는 evidence가 아니다.

상황별 probe:

- **Performance regression**: baseline과 current measurement를 세우고 profiler output, query plan, allocation data, timing harness, regression bisection을 사용한다.
- **Flaky waiting**: timer-driven behavior면 fake timer/virtual clock을 먼저 사용한다. 그 외에는 guessed sleep이 아니라 실제로 중요한 condition을 기다린다. fixed sleep은 elapsed time 자체가 테스트 대상이고 이유가 문서화될 때만 사용한다.
- **State pollution**: test, input, lifecycle step에 대한 bisection으로 polluter를 격리한다.
- **External/manual step**: structured prompt loop로 사람을 안내하고 답변을 machine-readable output으로 캡처한다.

timer-driven test, flaky async wait, fake timer vs polling 결정에는 `references/condition-based-waiting.md`를 사용한다. state pollution에는 `references/scripts/find-polluter.template.sh`, manual reproduction에는 `references/scripts/hitl-loop.template.sh`를 사용한다.

## Phase 6 — Fix the Root Cause

production code를 바꾸기 전에 correct seam이 있으면 실패하는 regression test를 만든다.

correct seam은 bug를 유발한 실제 chain을 실행한다. triggering path를 칠 수 없는 얕은 테스트는 false confidence다.

correct seam이 없다면 그 사실을 문서화한다. architecture가 이 bug를 고정할 수 없게 만들고 있다.

그 다음:

1. regression test가 실패하는 것을 보거나, test seam이 없으면 captured repro를 실행한다.
2. 확인된 root cause를 해결하는 가장 작은 source-level change를 만든다.
3. 관련 없는 refactor, cleanup, retry, fallback, broad validation, behavior change를 묶지 않는다.
4. invalid data가 여러 layer를 지나면 source를 안 뒤에만 defense-in-depth를 추가한다: boundary validation, domain invariant, environment guard, permanent observability는 각각 서로 다른 failure mode를 잡아야 한다.
5. 원래의 unminimized feedback loop를 다시 실행한다.

layered validation, guard, permanent observability를 추가하기 전에는 `references/defense-in-depth.md`를 사용한다.

crash point만 가리는 fix는 incomplete다.

## Phase 7 — Prove, Clean Up, Report

완료를 말하기 전에 검증한다.

- original feedback loop가 통과한다
- regression test가 통과하거나 missing test seam이 명시적으로 문서화됐다
- original user-described scenario가 실행됐다
- 관련 nearby check가 여전히 통과한다
- 모든 temporary `[DEBUG-...]` instrumentation이 제거됐다
- throwaway harness가 삭제됐거나 명확한 debug artifact로 표시됐다

보고 형식:

```md
## Root Cause

## Evidence

## Fix

## Regression Coverage

## Verification

## Remaining Risk
```

원래 시나리오를 다시 실행하지 않았다면 fixed라고 말하지 않는다.

## Red Flags

다음이 보이면 위반한 가장 이른 phase로 돌아간다.

- “아마 X니까 그냥 고치자.”
- “quick change 하나 해보고 보자.”
- “추적 전에 retry, timeout, fallback을 추가하자.”
- “warning이나 error를 억제하자.”
- “여러 개를 바꾸고 테스트하자.”
- “테스트는 통과했지만 보고된 failure는 아니었다.”
- “왜 됐는지는 모르겠다.”
- 반복된 실패 뒤에 “한 번만 더 고쳐보자.”
- “reference pattern이 길어서 대충 봤다.”
- “working example과 다르지만 상관없을 것이다.”

이것들은 작은 style 문제가 아니다. 버그가 살아남는 방식이다.
