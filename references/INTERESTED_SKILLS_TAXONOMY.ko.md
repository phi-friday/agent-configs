# 관심 스킬 분류

이 문서는 `references/`의 외부 저장소들 중 현재 관심 있는 스킬만 골라 내 전용 스킬 설계 관점에서 분류한 것이다.

## 관심 목록

### `mattpocock/skills`

- `caveman`
- `zoom-out`
- `to-prd`
- `tdd`
- `prototype`
- `diagnose`

### `obra/superpowers`

- `brainstorming`
- `subagent-driven-development`
- `dispatching-parallel-agents`
- `using-git-worktrees`
- `test-driven-development`
- `verification-before-completion`
- `systematic-debugging`
- `requesting-code-review`
- `receiving-code-review`

### `Fission-AI/OpenSpec`

- `openspec-explore`

---

## 1. 대화/작업 스타일

| 스킬 | 출처 | 역할 |
|---|---|---|
| `caveman` | `mattpocock/skills` | 짧고 밀도 높은 응답 모드. 토큰 절약, 불필요한 설명 제거, 직접적인 커뮤니케이션에 유용하다. |

독립 유틸리티에 가깝고, 다른 스킬들과 조합해서 사용할 수 있다.

---

## 2. 탐색 / 문제 정의 / 방향 잡기

| 스킬 | 출처 | 역할 |
|---|---|---|
| `brainstorming` | `obra/superpowers` | 요구사항, 목표, 제약을 대화로 정리한다. |
| `openspec-explore` | `Fission-AI/OpenSpec` | 구현 없이 아이디어, 가설, 설계 방향을 탐색한다. |
| `zoom-out` | `mattpocock/skills` | 낯선 코드베이스나 기능 영역을 큰 구조로 파악한다. |
| `to-prd` | `mattpocock/skills` | 대화와 탐색 결과를 PRD로 정리한다. |

가능한 흐름:

```text
brainstorming
→ openspec-explore
→ zoom-out
→ to-prd
```

단, `zoom-out`은 기존 코드가 있을 때 특히 유용하고, `openspec-explore`는 변경 아이디어를 구조화할 때 좋다.

---

## 3. 불확실성 제거 / 실험

| 스킬 | 출처 | 역할 |
|---|---|---|
| `prototype` | `mattpocock/skills` | 설계가 애매할 때 작게 만들어 검증한다. |
| `diagnose` | `mattpocock/skills` | 버그, 성능 저하, 이상 동작의 원인을 추적한다. |
| `systematic-debugging` | `obra/superpowers` | 가설 기반 디버깅 절차를 강제한다. |

구분:

```text
prototype = 만들기 전 불확실성 제거
diagnose + systematic-debugging = 망가진 뒤 원인 제거
```

`diagnose`와 `systematic-debugging`은 중복과 보완 관계가 강하므로 하나의 내 전용 스킬로 합치는 것을 고려할 만하다.

후보 이름:

- `systematic-diagnosis`
- `debug-root-cause`
- `root-cause-debugging`

---

## 4. 구현 규율 / TDD

| 스킬 | 출처 | 역할 |
|---|---|---|
| `tdd` | `mattpocock/skills` | Matt Pocock식 실무 TDD 워크플로우. |
| `test-driven-development` | `obra/superpowers` | RED-GREEN-REFACTOR 원칙을 강제하는 TDD 워크플로우. |

두 스킬은 중복도가 높으므로 따로 둘 필요가 적다.

추천 방향:

```text
test-driven-development
  + mattpocock/tdd의 실무 디테일 흡수
```

즉, 내 전용 스킬에서는 하나로 합치는 것이 좋다.

---

## 5. 병렬화 / 작업 분해 / 격리

| 스킬 | 출처 | 역할 |
|---|---|---|
| `subagent-driven-development` | `obra/superpowers` | 하위 에이전트로 구현, 리뷰, 검증을 분리한다. |
| `dispatching-parallel-agents` | `obra/superpowers` | 독립 작업을 병렬 에이전트에 분산한다. |
| `using-git-worktrees` | `obra/superpowers` | 병렬 작업을 안전하게 격리된 worktree에서 수행한다. |

이 셋은 강하게 연결된다.

추천 구조:

```text
parallel-development
├─ subagent-driven-development
├─ dispatching-parallel-agents
└─ using-git-worktrees
```

하나의 큰 스킬로 만들거나, 최소한 서로 참조하게 만드는 방식이 적합하다.

---

## 6. 검증 / 완료 선언 방지

| 스킬 | 출처 | 역할 |
|---|---|---|
| `verification-before-completion` | `obra/superpowers` | “끝났다”고 말하기 전에 실제 검증을 강제한다. |
| `requesting-code-review` | `obra/superpowers` | 병합이나 마감 전 리뷰 요청 절차를 제공한다. |
| `receiving-code-review` | `obra/superpowers` | 리뷰 피드백을 검증하고 항목별로 반영한다. |

가능한 흐름:

```text
verification-before-completion
→ requesting-code-review
→ receiving-code-review
```

고신뢰 작업에서 핵심 품질 게이트로 볼 수 있다.

---

## 추천 상위 분류

```text
1. communication
   - caveman

2. discovery
   - brainstorming
   - openspec-explore
   - zoom-out
   - to-prd

3. validation-by-experiment
   - prototype
   - diagnose
   - systematic-debugging

4. implementation-discipline
   - tdd
   - test-driven-development

5. parallel-execution
   - subagent-driven-development
   - dispatching-parallel-agents
   - using-git-worktrees

6. quality-gates
   - verification-before-completion
   - requesting-code-review
   - receiving-code-review
```

## 내 전용 스킬화 우선순위

```text
1. verification-before-completion
2. systematic-debugging + diagnose
3. test-driven-development + tdd
4. zoom-out
5. subagent-driven-development + dispatching-parallel-agents
6. openspec-explore
7. prototype
8. using-git-worktrees
9. requesting-code-review + receiving-code-review
10. caveman
11. to-prd
12. brainstorming
```
