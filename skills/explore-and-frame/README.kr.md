# explore-and-frame

[English](README.md) | [한국어](README.kr.md)

`explore-and-frame`은 구현 전 탐색, 문제 정의, 코드 맥락 파악, 선택지 비교, PRD/결정 메모 작성을 위한 in-progress 스킬이다.

목표는 “바로 만들기”가 아니라, 무엇을 만들어야 하는지와 왜 그렇게 해야 하는지를 먼저 선명하게 만드는 것이다.

## 파일 구성

- `SKILL.md`: 실제 스킬 정의. description은 영어와 한국어를 모두 포함해 영어/한국어 요청 모두에서 트리거될 수 있게 한다.
- `SKILL.kr.md`: `SKILL.md`의 한국어 번역본. 한국어로 내용을 검토하거나 수정할 때 기준으로 사용한다.
- `README.md`: 레퍼런스에서 어떤 요소를 가져왔고 어떻게 합쳤는지 설명하는 영어 원본 README.
- `README.kr.md`: 이 README의 한국어 번역본.

## 조합 방식

이 스킬은 네 개 레퍼런스의 역할을 하나의 탐색 스킬로 합쳤다.

```text
brainstorming                            → 질문과 요구사항 정리
openspec-explore                         → 자유 탐색 stance + 강한 시각화
historical zoom-out (제거된 개념)         → 기존 코드의 상위 구조 지도화
to-spec (구 to-prd)                     → 정리된 결정을 PRD/결정 프레임으로 압축

                explore-and-frame
        탐색 → 시각화 → 맥락 지도화 → 선택지 비교 → 결정 프레임
```

`brainstorming`처럼 모든 작업을 무조건 긴 승인 절차로 끌고 가지 않고, `openspec-explore`처럼 탐색 자체의 유연성을 유지한다. 다만 탐색이 흐릿하게 끝나지 않도록 `historical zoom-out`의 코드 맥락 지도화와 `to-spec`(구 `to-prd`)의 문서화 프레임을 붙였다.

## 레퍼런스별로 가져온 요소

### `obra/superpowers/brainstorming`

가져온 요소:

- 구현 전에 의도, 제약, 성공 기준을 먼저 확인하는 태도
- “한 번에 한 질문” 원칙
- 여러 접근안을 2~3개로 나누고 tradeoff와 추천안을 제시하는 방식
- 사용자의 목적과 현재 프로젝트 맥락을 먼저 확인하는 순서
- 불필요한 범위를 잘라내는 YAGNI 태도

변형한 점:

- 원본의 강한 hard gate, spec 저장, commit, 사용자 승인 루프는 그대로 가져오지 않았다.
- 이 스킬에서는 탐색과 framing이 목적이므로, 문서 저장은 사용자가 원할 때만 한다.
- 질문 절차도 체크리스트가 아니라 “가장 큰 불확실성을 줄이는 질문 하나”로 줄였다.

### `Fission-AI/OpenSpec`의 `openspec-explore`

가져온 요소:

- “workflow가 아니라 stance”라는 관점
- 구현하지 않고 생각, 조사, 가설, 비교, 정리를 수행하는 explore mode
- 사용자의 아이디어를 한 방향으로 몰지 않고 여러 thread를 열어두는 방식
- 코드가 관련되면 실제 코드베이스를 읽고 grounding하는 원칙
- `Use ASCII diagrams liberally` 원칙
- 문제 공간, 현재 구조, 선택지, 리스크, unknown을 시각화하는 방식
- 결정이 생겼을 때 자동 저장하지 않고 “캡처할까요?”라고 제안하는 태도

특히 비주얼 측면에서 다음 패턴을 직접 반영했다.

| OpenSpec 패턴 | 이 스킬에서의 형태 |
|---|---|
| architecture sketch | `System or flow map` |
| collaboration spectrum 예시 | `Spectrum map` |
| option table | `Option comparison` |
| scope visualization | `Scope map` |
| decision path | `Decision tree` |

변형한 점:

- OpenSpec 전용 CLI 명령, change artifact, `openspec status`, `proposal.md`, `design.md` 같은 특정 시스템 의존성은 제거했다.
- 대신 일반 코드베이스와 일반 작업 대화에서도 쓸 수 있는 시각화/탐색 패턴만 남겼다.
- “OpenSpec artifact 업데이트”는 “결정 메모/PRD 저장 제안”으로 일반화했다.

### `mattpocock/skills`의 `zoom-out` (제거됨)

가져온 요소:

- 낯선 코드 영역을 바로 세부 구현으로 들어가지 않고 한 단계 위에서 보는 방식
- 관련 모듈, 호출자, 데이터 흐름, 의존성, seam을 먼저 파악하는 태도
- 프로젝트의 도메인 어휘를 사용해 설명하는 원칙

변형한 점:

- 원본은 매우 짧은 지시문에 가깝다.
- 이 스킬에서는 `What To Investigate` 섹션으로 확장해, 코드 탐색 시 확인해야 할 항목을 구체화했다.
- 단순 설명이 아니라 이후 선택지 비교와 PRD/결정 프레임으로 이어지도록 연결했다.

### `mattpocock/skills`의 `to-spec` (구 `to-prd`)

가져온 요소:

- 대화와 코드베이스 이해를 PRD 형태로 압축하는 방식
- 문제, 목표, 사용자 스토리, 구현 결정, 테스트 결정을 분리하는 구조
- 구현 결정은 모듈, 인터페이스, 경계, 데이터 흐름 중심으로 적는 태도
- 테스트 결정은 구현 세부가 아니라 외부 동작, 검증 범위, 기존 high-level testing seam 중심으로 적는 태도

변형한 점:

- 원본은 이슈 트래커 발행까지 포함하지만, 이 스킬에서는 발행을 필수로 하지 않는다.
- PRD는 항상 만드는 산출물이 아니라, 탐색 결과가 충분히 안정됐거나 사용자가 요청할 때만 만드는 선택지로 뒀다.
- 파일 경로나 코드 스니펫을 남발하지 말라는 취지는 유지하되, 결정 자체가 특정 파일과 관련될 때는 예외를 허용하는 방향으로 일반화했다.

## 최종 스킬 안에서의 역할 분담

```text
1. Entry Points
   - brainstorming의 요구사항 정리
   - openspec-explore의 다양한 진입점 처리

2. What To Investigate
   - historical zoom-out (제거된 개념)의 코드 맥락 지도화
   - openspec-explore의 codebase grounding

3. Questions
   - brainstorming의 one-question-at-a-time
   - 목적/제약/성공 기준 중심 질문

4. Visual Thinking
   - openspec-explore의 ASCII diagram 중심 탐색
   - flow, spectrum, option, scope, decision tree 패턴

5. Comparing Approaches
   - brainstorming의 2~3개 접근안 비교
   - constraint-driven recommendation

6. Framing The Result
   - to-spec (구 to-prd)의 PRD 구조
   - 작은 작업용 decision frame 추가

7. Capturing Decisions
   - openspec-explore의 “자동 저장하지 말고 제안하기” 태도
```

## 의도적으로 제외한 것

- 구현 단계 지침
- 테스트 작성 지침
- OpenSpec 전용 CLI 사용법
- GitHub issue 발행 절차
- 강제 commit 절차
- 모든 탐색을 PRD로 끝내는 규칙
- 사용자 승인 게이트를 매 단계 강제하는 절차

이 스킬은 구현 프로세스 전체가 아니라, 구현으로 들어가기 전의 탐색과 framing만 담당한다.

## 참고한 파일

다음 파일이 업데이트되면 이 스킬도 다시 검토한다.

- `references/obra/superpowers/skills/brainstorming/SKILL.md`
- `references/obra/superpowers/skills/brainstorming/visual-companion.md`
- `references/obra/superpowers/skills/brainstorming/spec-document-reviewer-prompt.md`
- `references/Fission-AI/OpenSpec/src/core/templates/workflows/explore.ts`
- `references/Fission-AI/OpenSpec/openspec/explorations/explore-workflow-ux.md`
- `references/mattpocock/skills/skills/engineering/to-spec/SKILL.md`
- `zoom-out` 아이디어의 제거된 역사적 출처(현재 교체본 아님): https://github.com/mattpocock/skills/blob/694fa30311e02c2639942308513555e61ee84a6f/skills/engineering/zoom-out/SKILL.md (commit-pinned)

## 라이선스 메모

레퍼런스 저장소들은 MIT License다. 원문, 체크리스트, 템플릿, 스크립트를 실질적으로 복사하거나 수정해 포함하는 경우 `NOTICE.md`의 고지를 유지해야 한다.
