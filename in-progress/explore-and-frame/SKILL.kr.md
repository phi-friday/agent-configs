---
name: explore-and-frame
description: "구현 전에 사용자가 막연한 아이디어, 불명확한 문제, 낯선 코드 영역, 선택지 비교, 범위 질문, PRD 요청을 가져왔을 때 사용한다. 구현하지 않고 사고 전용 모드로 조사, 시각화, 가정 검토, 접근안 비교, 코드 맥락 지도화, 결정 프레이밍을 수행한다. English: Use before implementation when the user brings a vague idea, unclear problem, unfamiliar code area, option comparison, scope question, or PRD request. Enter a thinking-only mode: investigate, visualize, question assumptions, compare approaches, map code context, and frame the decision without implementing."
---

# Explore and Frame

사고 모드로 들어간다. 사용자가 문제를 이해하고, 범위를 잡고, 다음에 무엇을 해야 하는지 결정할 수 있도록 돕는다.

이 스킬은 엄격한 순서형 워크플로우가 아니라 stance다. 모든 요청을 같은 체크리스트로 밀어 넣지 않는다. 불확실성을 가장 빠르게 줄이는 흐름을 따른다.

## Hard Gate

이 스킬이 활성화된 동안에는 구현하지 않는다.

파일 읽기, 코드 검색, 문서 확인, 아키텍처 지도화, 선택지 비교, 결정 메모 초안 작성은 가능하다. 애플리케이션 코드 작성, 리팩터링, 테스트 추가, 설정 변경, 구현 스캐폴딩은 하면 안 된다.

사용자가 구현을 요청하면, 먼저 현재까지 확인한 내용을 요약하고 explore mode를 종료할지 묻는다.

## Stance

- **호기심 있게, 단정하지 않기**: 문제에서 자연스럽게 나오는 질문을 한다.
- **근거 있게, 추측하지 않기**: 코드가 중요하면 실제 코드베이스를 확인한 뒤 설명한다.
- **질문 공세가 아니라 열린 thread**: 유망한 방향들을 드러내되 하나의 질문 경로로 몰아가지 않는다.
- **기본은 시각화**: 아키텍처, 흐름, 상태, tradeoff, 의존성, 범위가 더 명확해진다면 ASCII 다이어그램을 적극 사용한다.
- **서두르지 않기**: 해결책에 고정하기 전에 문제의 형태가 드러나게 둔다.
- **범위를 날카롭게 구분하기**: 목표, 비목표, 가정, unknown을 분리한다.
- **결정 지향**: 결론이 “더 탐색하자”이더라도 다음 결정을 더 쉽게 만드는 출력을 낸다.

## Entry Points

진입점에 따라 다르게 처리한다.

| 진입점 | 먼저 할 일 |
|---|---|
| 막연한 아이디어 | 사용자, 문제, 원하는 결과, 성공 기준을 명확히 한다. |
| 구체적인 불편/문제 | 증상, 근본 문제, 원하는 동작, 제약을 분리한다. |
| 낯선 코드 | 한 단계 위에서 모듈, 호출자, 데이터 흐름, 소유권, 통합 지점을 지도화한다. |
| 선택지 비교 | 도구나 설계를 비교하기 전에 실제 제약을 확인한다. |
| PRD/spec 요청 | 이미 아는 맥락을 먼저 종합하고, 범위에 큰 영향을 주는 누락 결정만 질문한다. |
| 기존 변경/설계 | 제안을 하기 전에 기존 artifact를 읽는다. |

## What To Investigate

코드베이스 맥락이 중요하면 해결책을 제안하기 전에 작은 지도를 만든다.

- 관련 모듈과 파일
- 호출자와 진입점
- 데이터 흐름, 상태 흐름, 요청 흐름
- 책임 경계
- 기존 패턴과 네이밍/도메인 어휘
- 주변에서 이미 쓰는 테스트 또는 검증 경로
- 숨은 결합, 마이그레이션 리스크, 호환성 제약

긴 설명보다 작은 다이어그램을 선호한다.

```text
CURRENT FLOW

User action
    │
    ▼
API / command entrypoint
    │
    ▼
Domain service ─────▶ external provider
    │
    ▼
Persistence / state
```

낯선 영역에서는 명시적으로 답한다.

```text
What exists?
Who calls it?
What does it depend on?
What depends on it?
Where are the seams?
What vocabulary does this codebase use for this concept?
```

## Questions

사용자가 명시적으로 설문지를 요청하지 않는 한 한 번에 한 질문만 한다.

좋은 질문은 결정 불확실성을 줄인다.

- 사용자에게 보이는 결과 중 무엇이 가장 중요한가?
- 무엇은 반드시 호환되어야 하는가?
- 어떤 실패 모드는 절대 허용할 수 없는가?
- 이건 오래 유지할 경로인가, 버릴 수 있는 spike인가?
- 어떤 제약이 가장 지배적인가: 정확성, 지연시간, 단순성, 전달 속도, 비용, 운영성, 마이그레이션 리스크?

도구나 저장소 맥락으로 확인할 수 있는 것은 사용자에게 묻지 않는다.

## Visual Thinking

생각을 더 명확하게 만든다면 ASCII 다이어그램을 적극 사용한다. 좋은 다이어그램 하나가 문단 하나보다 낫다.

사용자가 시각화를 요청할 때까지 기다리지 않는다. 흐름, 상태, 경계, 의존성, tradeoff, 범위, 순서가 관련되어 있으면 스케치한다.

좋은 다이어그램 대상:

- 시스템 경계
- 요청, 데이터, 이벤트 흐름
- 상태 머신
- 의존성 그래프
- before/after 아키텍처
- 선택지 tradeoff
- 범위 경계
- unknown과 decision point

### System or flow map

```text
CURRENT AUTH FLOW

        ┌─────────┐     ┌─────────┐     ┌─────────┐
        │ Google  │     │ GitHub  │     │ Email   │
        │ OAuth   │     │ OAuth   │     │ Magic   │
        └────┬────┘     └────┬────┘     └────┬────┘
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                      ┌─────────────┐
                      │ Session     │
                      └──────┬──────┘
                             ▼
                      ┌─────────────┐
                      │ Permissions │
                      └─────────────┘

Question: which edge is actually causing pain?
```

### Spectrum map

막연한 아이디어가 여러 복잡도 수준에 걸쳐 있을 때 사용한다.

```text
COLLABORATION SPECTRUM

Awareness              Coordination              Sync
    │                       │                     │
    ▼                       ▼                     ▼
┌──────────┐           ┌──────────┐          ┌──────────┐
│Presence  │           │Cursors   │          │CRDT      │
│"3 online"│           │selection │          │merge-free│
└──────────┘           └──────────┘          └──────────┘
  simple                 moderate              complex

Where on this spectrum is the actual user need?
```

### Option comparison

```text
STORAGE OPTIONS FOR LOCAL CLI

Constraint        SQLite        Postgres
────────────────────────────────────────────
Offline           yes           no
Daemon required   no            yes
Single-user       natural       overkill
Migration cost    low           medium

Recommendation: SQLite, unless sync/multi-user access is a near-term requirement.
```

### Scope map

```text
IN SCOPE                         OUT OF SCOPE
────────────────────────────     ────────────────────────────
Parse existing config            New config language
Validate required fields         Remote config service
Clear error messages             UI for editing config
Migration note                   Auto-fix every legacy file
```

### Decision tree

```text
                 Is this user-visible?
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
             yes                    no
              │                     │
     Need compatibility?      Is it cleanup only?
              │                     │
        ┌─────┴─────┐         ┌─────┴─────┐
        ▼           ▼         ▼           ▼
      yes           no       yes          no
   migrate       simplify   defer      clarify
```

다이어그램은 작게 유지한다. 답변을 장식하는 것이 아니라 구조를 드러내야 한다.

## Comparing Approaches

가능한 경로가 여러 개면 2~3개 선택지를 제시한다.

다음 형태를 사용한다.

```md
### Option A: <name>

- Idea:
- Strengths:
- Risks:
- Best when:

### Option B: <name>

- Idea:
- Strengths:
- Risks:
- Best when:

Recommendation: <option>
Reason: <constraint-driven rationale>
```

tradeoff를 구체적으로 말한다. “상황에 따라 다르다”로 끝내지 말고 무엇에 따라 달라지는지 말한다.

## Framing The Result

생각이 결정으로 굳어지면 유용한 것만 요약한다. 사용자가 명확성만 필요로 했는데 문서를 강요하지 않는다.

### Decision Frame

```md
## Problem

## Goal

## Non-Goals

## Current Context

## Options

## Recommendation

## Risks / Unknowns

## Next Step
```

### PRD Frame

사용자가 PRD/spec을 요청했거나, 구현에 안정적인 계약이 필요할 만큼 작업이 클 때 사용한다.

```md
## Problem Statement

## Goals

## Non-Goals

## User Stories

## Current Context

## Proposed Direction

## Implementation Decisions

## Testing Decisions

## Risks and Open Questions
```

Implementation decisions에는 모듈, 경계, 인터페이스, 데이터 흐름, 아키텍처 결정을 적는다. 정확한 파일 자체가 결정의 일부인 경우가 아니라면 깨지기 쉬운 파일 경로 수준 약속은 피한다.

Testing decisions는 외부에서 관찰 가능한 동작, edge case, 기존 검증 패턴에 집중한다.

## Capturing Decisions

자동으로 캡처하지 않는다. 결정이 안정되면 문서 저장이나 업데이트를 제안한다.

예시:

- “그건 범위 결정처럼 보입니다. PRD에 캡처할까요?”
- “이건 설계를 바꿉니다. decision note를 업데이트할까요?”
- “구현에 들어갈 만큼 정리됐습니다. 먼저 계획을 쓸까요, 아니면 더 탐색할까요?”

## Completion

다음 중 하나가 참이면 탐색은 완료된다.

- 사용자가 충분히 명확해졌고 멈추길 원함
- tradeoff가 포함된 추천안이 명확함
- 변경을 계획할 수 있을 만큼 코드 영역이 지도화됨
- open question이 명시되고 소유자 또는 다음 probe가 있음
- 다음 모드가 명확함: plan, prototype, diagnose, TDD implementation, PRD, issue, more exploration

핵심 요구사항, 제약, 리스크가 남아 있으면 구현 준비가 됐다고 말하지 않는다. 누락된 결정을 명확히 말한다.
