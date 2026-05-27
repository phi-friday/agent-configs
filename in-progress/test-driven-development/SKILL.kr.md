---
name: test-driven-development
description: 기능, 버그 수정, 리팩터링, 동작 변경, 새 public interface를 test-first로 구현할 때 사용한다. red-green-refactor를 강제한다: 동작 테스트 하나를 먼저 쓰고, 올바른 이유로 실패하는 것을 보고, 최소 production code로 통과시키고, 통과 상태에서만 리팩터링한다. English: Use when implementing a feature, bug fix, refactor, behavior change, or new public interface with test-first discipline. Enforce red-green-refactor: write one failing behavior test, watch it fail for the right reason, write minimal production code, watch it pass, then refactor while green.
---

# Test-Driven Development

동작을 검증된 slice 하나씩 만든다.

## Non-Negotiables

```text
실패하는 테스트 전에 PRODUCTION CODE 없음.
올바른 이유로 RED를 보지 않으면 GREEN 없음.
RED 상태에서 REFACTOR 없음.
```

production code를 먼저 썼다면 그것을 “reference”로 계속 고쳐 쓰지 않는다. 구현 경로에서 제거하고 실패하는 테스트부터 다시 시작한다.

## Supporting References

이 파일은 실행 checklist로 유지한다. 해당 주제가 나오면 supporting reference를 연다.

- `references/test-quality.md` — behavior test, public interface, 나쁜 test smell.
- `references/mocking-guidelines.md` — 언제 mock하고, mock을 테스트하지 않는 방법.
- `references/interface-design.md` — 테스트하고 사용하기 쉬운 public interface 설계.
- `references/refactoring.md` — green 이후 behavior를 바꾸지 않는 cleanup.

## Use When

다음에 사용한다.

- 새 기능
- 버그 수정
- 동작 변경
- 안전망이 필요한 refactor
- 새 public API 또는 command/UI flow
- 구현 중 발견한 edge case

root cause를 모르는 bug라면 먼저 root-cause debugging으로 재현하고 원인을 확인한다. 그 다음 TDD로 실패하는 regression test를 만들어 fix를 고정한다.

## Phase 0 — Choose One Behavior

테스트를 쓰기 전에 외부에서 관찰 가능한 동작 하나를 정확히 이름 붙인다.

좋은 behavior statement:

- “rejects empty email”
- “returns cached result until the TTL expires”
- “shows validation errors without submitting the form”
- “retries a transient failure three times, then returns success”

피할 implementation statement:

- “calls `validateEmail`”
- “sets `isValid` to false”
- “invokes payment service with cart total”

public interface가 불명확하면 테스트가 사용할 가장 작은 interface를 설계한다. 작은 surface area와 실제 caller vocabulary를 선호한다.

interface가 쓰기 어려워 테스트도 어렵다면 `references/interface-design.md`를 사용한다.

## Phase 1 — RED: Write One Failing Test

public interface를 통해 동작 하나에 대한 최소 테스트 하나를 쓴다.

규칙:

- 테스트 하나에 동작 하나
- 테스트 이름은 caller/user가 관찰하는 것을 설명
- 가능한 한 real code path 사용
- system boundary만 mock하고 internal collaborator는 mock하지 않음
- assertion은 implementation path가 아니라 behavior를 증명

해당 테스트만 실행하고 실패를 본다.

확인한다.

- 통과가 아니라 실패한다
- 예상한 이유로 실패한다
- typo, 잘못된 setup, import 문제가 아니라 behavior가 없어서 실패한다

즉시 통과하면 새 behavior를 증명하지 못한 것이다. 테스트를 고치거나 다음 누락 behavior를 고른다.

mock이나 test utility를 추가하기 전에는 `references/test-quality.md`와 `references/mocking-guidelines.md`를 사용한다.

## Phase 2 — GREEN: Minimal Production Code

현재 실패하는 테스트를 통과시키는 가장 작은 production change를 쓴다.

추가하지 않는다.

- 미래 option
- 일반화된 configuration
- 관련 없는 validation
- speculative branch
- 현재 path 밖의 refactor
- 현재 테스트가 요구하지 않는 추가 behavior

같은 테스트를 실행하고 통과를 본다.

실패하면 RED failure 자체가 틀린 경우가 아닌 한 테스트가 아니라 production code를 고친다.

그 다음 local regression을 잡기 위해 직접 영향받는 테스트를 실행한다.

## Phase 3 — REFACTOR: Improve While Green

테스트가 green인 뒤에만 refactor한다.

허용:

- duplication 제거
- 이름 개선
- 같은 public interface 뒤로 helper 추출
- conditional 단순화
- 작은 interface 뒤로 complexity를 숨겨 module을 deep하게 만들기
- data나 responsibility가 있는 곳으로 logic 이동

금지:

- 새 failing test 없이 behavior 변경
- 테스트된 behavior와 무관한 broad cleanup
- implementation detail에 맞추기 위한 test 변경

각 refactor step 또는 작은 batch 뒤에 테스트를 실행한다. red가 되면 refactor를 멈추고 green을 복구한다.

cleanup 후보는 `references/refactoring.md`를 사용한다.

## Phase 4 — Repeat Vertically

모든 테스트를 먼저 쓰고 모든 구현을 나중에 쓰지 않는다.

vertical slice를 사용한다.

```text
RED test 1 → GREEN code 1 → REFACTOR
RED test 2 → GREEN code 2 → REFACTOR
RED test 3 → GREEN code 3 → REFACTOR
```

다음 테스트는 이전 cycle에서 배운 것을 반영해야 한다.

## Completion Checklist

완료를 말하기 전에 확인한다.

- 모든 새 behavior에 test가 있다
- 각 test는 구현 전에 예상한 이유로 실패하는 것을 봤다
- test는 private implementation이 아니라 public behavior를 실행한다
- mock은 system boundary에만 있고 assertion 대상이 아니다
- behavior와 관련된 edge case와 error path가 커버됐다
- production code에 test-only method나 test-only branch가 없다
- temporary scaffolding이 제거됐다
- 직접 영향받는 테스트가 통과한다

## Red Flags

다음이 보이면 멈추고 RED로 돌아간다.

- test 전 implementation
- test가 즉시 통과
- 왜 test가 실패했는지 설명할 수 없음
- test 이름이 behavior가 아니라 implementation을 설명
- internal collaborator mock
- behavior assertion 대신 mock 호출 assertion
- test-only production method 추가
- mock setup이 테스트하는 behavior보다 큼
- red 상태에서 refactor
- “혹시 몰라” option이나 branch 추가
- 구현 없이 test를 batch로 먼저 작성

이것들은 style 문제가 아니다. 테스트가 behavior를 보호하지 못하게 되는 방식이다.
