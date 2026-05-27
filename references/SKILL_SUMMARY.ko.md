# 레퍼런스 스킬 조사 요약

이 문서는 `references/`에 서브모듈로 추가된 외부 저장소들의 스킬/워크플로우를 한국어로 정리한 참고 문서다.

- 조사 대상
  - `references/mattpocock/skills`
  - `references/obra/superpowers`
  - `references/Fission-AI/OpenSpec`
- 라이선스: 세 저장소 모두 MIT License
- 주의: 이 문서는 참고용 요약이다. 외부 저장소의 코드, 문서, 스크립트를 복사·수정·실질적으로 포함할 경우 `NOTICE.md`와 원본 라이선스 고지를 유지해야 한다.

## 전체 개요

| 저장소 | 확인한 스킬/템플릿 | 성격 |
|---|---:|---|
| `mattpocock/skills` | 27개 `SKILL.md` | 개인 생산성, 글쓰기, 엔지니어링 워크플로우, 이슈/PRD/TDD/진단 중심 |
| `obra/superpowers` | 14개 `SKILL.md` | 고신뢰 개발 프로세스: 브레인스토밍, 계획, 실행, TDD, 검증, 리뷰, 마감 |
| `Fission-AI/OpenSpec` | 11개 등록 워크플로우 스킬 템플릿 + 1개 feedback 템플릿 | OpenSpec 변경 관리용 `/opsx:*` 커맨드/스킬 생성 템플릿 |

---

## 1. `mattpocock/skills`

구조: `references/mattpocock/skills/skills/<category>/<skill>/SKILL.md`

이 저장소는 개인 작업 방식과 엔지니어링 워크플로우를 스킬로 세분화한다. 특히 엔지니어링 계열은 이슈 트래커, 라벨, 도메인 문서, ADR, TDD, 진단, PRD/이슈 분해가 서로 연결되는 형태다.

### 1.1 Productivity

| 스킬 | 경로 | 요약 |
|---|---|---|
| `caveman` | `skills/productivity/caveman/SKILL.md` | 응답을 극도로 짧고 직접적인 톤으로 줄이는 모드. 기술 용어는 유지하되 불필요한 수식어를 제거한다. |
| `grill-me` | `skills/productivity/grill-me/SKILL.md` | 계획이나 설계를 강하게 질문해 빈틈을 찾는 스킬. 한 번에 한 질문씩 던지고 의사결정 트리를 완성한다. |
| `handoff` | `skills/productivity/handoff/SKILL.md` | 현재 대화와 작업 상태를 다음 세션에 넘길 수 있도록 인수인계 문서로 압축한다. 민감정보 제거와 중복 회피를 강조한다. |
| `write-a-skill` | `skills/productivity/write-a-skill/SKILL.md` | 새 스킬을 만들 때 요구사항 수집, `SKILL.md` 작성, 설명/리소스/스크립트 구조화를 안내한다. |

### 1.2 Personal

| 스킬 | 경로 | 요약 |
|---|---|---|
| `edit-article` | `skills/personal/edit-article/SKILL.md` | 기사나 초안을 섹션 단위로 재구성하고 문체를 다듬는다. 제목 기반 구조화와 문단 단위 재작성에 초점이 있다. |
| `obsidian-vault` | `skills/personal/obsidian-vault/SKILL.md` | Obsidian vault 안에서 노트를 검색, 생성, 정리한다. wikilink, 파일명, 역링크, 인덱스 노트 규칙을 사용한다. |

### 1.3 Misc

| 스킬 | 경로 | 요약 |
|---|---|---|
| `migrate-to-shoehorn` | `skills/misc/migrate-to-shoehorn/SKILL.md` | 테스트 코드의 TypeScript 타입 단언을 `@total-typescript/shoehorn` 기반 헬퍼로 바꿔 타입 안정성을 높인다. |
| `scaffold-exercises` | `skills/misc/scaffold-exercises/SKILL.md` | 강의/실습용 exercise 디렉터리 구조를 번호 규칙에 맞춰 생성하고 lint 통과까지 확인한다. |
| `setup-pre-commit` | `skills/misc/setup-pre-commit/SKILL.md` | Husky, lint-staged, Prettier 기반 pre-commit 훅을 설정한다. 패키지 매니저 감지와 실행 검증을 포함한다. |
| `git-guardrails-claude-code` | `skills/misc/git-guardrails-claude-code/SKILL.md` | Claude Code에서 위험한 git 명령을 차단하는 hook/script 설정을 구성한다. |

### 1.4 Engineering

| 스킬 | 경로 | 요약 |
|---|---|---|
| `triage` | `skills/engineering/triage/SKILL.md` | 이슈를 상태/카테고리 라벨 기반으로 분류하고 재현, 요구사항, 범위 판단을 정리한다. |
| `zoom-out` | `skills/engineering/zoom-out/SKILL.md` | 낯선 코드 영역을 모듈, 호출자, 도메인 용어 관점에서 상위 구조로 이해한다. |
| `to-issues` | `skills/engineering/to-issues/SKILL.md` | PRD, 계획, 스펙을 독립 실행 가능한 구현 이슈들로 쪼갠다. vertical slice 단위 분해를 지향한다. |
| `to-prd` | `skills/engineering/to-prd/SKILL.md` | 대화와 코드베이스 탐색 결과를 PRD로 정리하고 이슈에 발행한다. 문제, 해결, 사용자 스토리, 테스트, 범위 외 항목을 포함한다. |
| `tdd` | `skills/engineering/tdd/SKILL.md` | Red-Green-Refactor 방식으로 기능/버그 작업을 진행한다. 테스트 하나씩 작성하고 세로 슬라이스로 통과시킨다. |
| `prototype` | `skills/engineering/prototype/SKILL.md` | 설계 검증을 위해 일회성 프로토타입을 만든다. UI 또는 로직 검증 후 삭제하거나 설계 결정으로 반영한다. |
| `setup-matt-pocock-skills` | `skills/engineering/setup-matt-pocock-skills/SKILL.md` | 이슈 트래커, 라벨, 도메인 문서, `AGENTS.md`/`CLAUDE.md` 등 엔지니어링 스킬의 전제 컨텍스트를 세팅한다. |
| `improve-codebase-architecture` | `skills/engineering/improve-codebase-architecture/SKILL.md` | 코드베이스의 아키텍처 마찰, 테스트성 문제, AI 탐색성 문제를 찾아 보고서로 정리한다. |
| `grill-with-docs` | `skills/engineering/grill-with-docs/SKILL.md` | 계획을 `CONTEXT.md`, ADR, 도메인 문서와 대조하며 공격적으로 검증한다. 필요하면 문서 갱신까지 유도한다. |
| `diagnose` | `skills/engineering/diagnose/SKILL.md` | 재현 루프, 가설, 계측, 수정, 회귀 검증을 통해 버그나 성능 문제의 근본 원인을 찾는다. |

### 1.5 In progress

| 스킬 | 경로 | 요약 |
|---|---|---|
| `writing-shape` | `skills/in-progress/writing-shape/SKILL.md` | raw material을 기사/논문 형태로 점진적으로 성형한다. 오프닝 후보와 섹션 전개를 반복적으로 제안한다. |
| `review` | `skills/in-progress/review/SKILL.md` | 특정 기준점 대비 diff를 표준 준수와 스펙 적합성 두 축으로 병렬 리뷰한다. |
| `writing-beats` | `skills/in-progress/writing-beats/SKILL.md` | 글을 선형 초안이 아니라 이야기의 beat 단위로 구성하며 다음 전개를 반복 제안한다. |
| `writing-fragments` | `skills/in-progress/writing-fragments/SKILL.md` | 아이디어 조각을 하나의 파일에 계속 추가해 장기 글쓰기 원재료로 축적한다. |

### 1.6 Deprecated

| 스킬 | 경로 | 요약 |
|---|---|---|
| `qa` | `skills/deprecated/qa/SKILL.md` | 버그/QA 세션을 통해 사용자 관점의 GitHub issue를 만든다. 현재는 deprecated 영역에 있다. |
| `request-refactor-plan` | `skills/deprecated/request-refactor-plan/SKILL.md` | 리팩터링 계획을 작은 커밋 단위로 쪼개고 GitHub issue로 만든다. |
| `ubiquitous-language` | `skills/deprecated/ubiquitous-language/SKILL.md` | 도메인 용어를 정리해 `UBIQUITOUS_LANGUAGE.md`로 저장한다. |
| `design-an-interface` | `skills/deprecated/design-an-interface/SKILL.md` | 같은 모듈에 대한 서로 다른 API/인터페이스 설계안을 병렬로 만들고 비교한다. |

---

## 2. `obra/superpowers`

구조: `references/obra/superpowers/skills/<skill>/SKILL.md`

이 저장소는 “작업을 시작하기 전 스킬을 선택하고, 계획하고, 검증하고, 리뷰하고, 마감한다”는 개발 운영 규칙을 강하게 밀어붙인다. 개별 스킬은 독립적으로 쓸 수 있지만, 전체적으로는 고신뢰 개발 파이프라인처럼 연결된다.

### 2.1 진입/사고/계획

| 스킬 | 경로 | 요약 |
|---|---|---|
| `using-superpowers` | `skills/using-superpowers/SKILL.md` | 대화 시작 및 작업 전 적용 가능한 스킬을 먼저 확인하도록 강제하는 진입 규칙이다. |
| `brainstorming` | `skills/brainstorming/SKILL.md` | 기능이나 행동 변경 전에 요구사항과 설계를 탐색하고 사용자 승인 게이트를 둔다. |
| `writing-plans` | `skills/writing-plans/SKILL.md` | 다단계 구현 전 파일, 테스트, 체크포인트가 포함된 상세 계획을 만든다. |

### 2.2 실행/병렬화/작업공간

| 스킬 | 경로 | 요약 |
|---|---|---|
| `subagent-driven-development` | `skills/subagent-driven-development/SKILL.md` | 독립 작업을 하위 에이전트로 분해하고 spec review와 code quality review를 반복한다. |
| `executing-plans` | `skills/executing-plans/SKILL.md` | 작성된 plan을 단계별로 실행하고 각 단계 완료 검증 후 다음 단계로 넘어간다. |
| `dispatching-parallel-agents` | `skills/dispatching-parallel-agents/SKILL.md` | 서로 독립적인 문제나 영역을 여러 에이전트에 병렬 분산한다. |
| `using-git-worktrees` | `skills/using-git-worktrees/SKILL.md` | 격리된 작업공간이 필요할 때 git worktree 생성, 설정, 베이스라인 검증을 규칙화한다. |

### 2.3 개발 규율/검증/디버깅

| 스킬 | 경로 | 요약 |
|---|---|---|
| `test-driven-development` | `skills/test-driven-development/SKILL.md` | 기능/버그 작업을 RED-GREEN-REFACTOR로 진행해 동작 정의와 회귀 방지를 강제한다. |
| `verification-before-completion` | `skills/verification-before-completion/SKILL.md` | “완료”, “고침”, “통과”라고 말하기 전에 실제 검증 명령과 출력 근거를 요구한다. |
| `systematic-debugging` | `skills/systematic-debugging/SKILL.md` | 실패 발생 시 근본 원인 분석, 패턴 추적, 가설 검증 순서로 수정하도록 한다. |

### 2.4 리뷰/마감

| 스킬 | 경로 | 요약 |
|---|---|---|
| `requesting-code-review` | `skills/requesting-code-review/SKILL.md` | 마일스톤이나 병합 전에 리뷰를 요청하고, 발견 사항을 중요도별로 분류한다. |
| `receiving-code-review` | `skills/receiving-code-review/SKILL.md` | 리뷰 피드백을 무비판적으로 수용하지 않고 기술적으로 검증한 뒤 항목별로 반영한다. |
| `finishing-a-development-branch` | `skills/finishing-a-development-branch/SKILL.md` | 테스트 통과 후 병합, PR, 보류, 폐기 등 브랜치 마감 옵션과 정리 절차를 제시한다. |

### 2.5 스킬 작성

| 스킬 | 경로 | 요약 |
|---|---|---|
| `writing-skills` | `skills/writing-skills/SKILL.md` | 새 스킬 작성/수정/배포를 위한 메타 스킬. 문서 품질을 테스트하듯 검증하고 압력 시나리오를 사용한다. |

---

## 3. `Fission-AI/OpenSpec`

OpenSpec에는 위 두 저장소처럼 완성된 `skills/<name>/SKILL.md` 모음이 아니라, 스킬/커맨드를 생성하기 위한 TypeScript 템플릿이 있다.

주요 구조:

- `src/core/templates/workflows/*.ts`: 각 워크플로우 스킬/커맨드 템플릿 정의
- `src/core/templates/skill-templates.ts`: 템플릿 export 허브
- `src/core/shared/skill-generation.ts`: 실제 스킬 템플릿 등록/필터링/명령 콘텐츠 변환

`getSkillTemplates()`에 등록된 기본 워크플로우 스킬은 11개다. `feedback`은 `skill-templates.ts`에서 export되지만 `getSkillTemplates()` 기본 목록에는 포함되지 않는 별도 템플릿이다.

### 3.1 등록 워크플로우 스킬 템플릿

| 템플릿/스킬 | 커맨드 | 경로 | 요약 |
|---|---|---|---|
| `openspec-explore` | `/opsx:explore` | `src/core/templates/workflows/explore.ts` | 구현 없이 자유 탐색, 질문, 가설, 시각화를 통해 변경 아이디어를 정리한다. 필요하면 산출물 후보로 캡처한다. |
| `openspec-new-change` | `/opsx:new` | `src/core/templates/workflows/new-change.ts` | 새 change 컨테이너를 만들고 첫 번째 ready artifact의 지침을 보여준다. 직접 artifact를 작성하지는 않는다. |
| `openspec-continue-change` | `/opsx:continue` | `src/core/templates/workflows/continue-change.ts` | 현재 change의 다음 ready artifact 하나를 생성한다. proposal → specs → design → tasks 같은 순서를 따른다. |
| `openspec-apply-change` | `/opsx:apply` | `src/core/templates/workflows/apply-change.ts` | artifact와 task 목록을 기반으로 실제 구현을 진행한다. blocked/all_done 상태와 편집 가능 범위를 가드한다. |
| `openspec-ff-change` | `/opsx:ff` | `src/core/templates/workflows/ff-change.ts` | 준비된 변경 요청을 바탕으로 apply에 필요한 artifact들을 의존성 순서대로 빠르게 생성한다. |
| `openspec-propose` | `/opsx:propose` | `src/core/templates/workflows/propose.ts` | 새 change 생성 후 proposal, specs, design, tasks 등 필수 artifact를 한 번에 생성하는 빠른 경로다. 구현은 하지 않는다. |
| `openspec-sync-specs` | `/opsx:sync` | `src/core/templates/workflows/sync-specs.ts` | change의 delta spec을 메인 `openspec/specs/<capability>/spec.md`로 병합한다. ADDED/MODIFIED/REMOVED/RENAMED 섹션을 처리한다. |
| `openspec-archive-change` | `/opsx:archive` | `src/core/templates/workflows/archive-change.ts` | 변경을 마무리하고 archive 디렉터리로 이동한다. 미완료 artifact/task와 spec 동기화 여부를 확인한다. |
| `openspec-bulk-archive-change` | `/opsx:bulk-archive` | `src/core/templates/workflows/bulk-archive-change.ts` | 여러 change를 동시에 아카이브하고, 같은 capability spec을 건드리는 충돌을 감지/해소한다. |
| `openspec-verify-change` | `/opsx:verify` | `src/core/templates/workflows/verify-change.ts` | 구현 전후로 task 완료도, 요구사항/시나리오 커버리지, 설계 일치성, 패턴 일관성을 검증한다. |
| `openspec-onboard` | `/opsx:onboard` | `src/core/templates/workflows/onboard.ts` | 실제 코드베이스를 대상으로 OpenSpec의 Explore → New → Proposal → Specs → Design → Tasks → Apply → Archive 흐름을 교육형으로 안내한다. |

### 3.2 별도 feedback 템플릿

| 템플릿/스킬 | 커맨드 | 경로 | 요약 |
|---|---|---|---|
| `feedback` | `openspec feedback "<title>" --body "<body>"` | `src/core/templates/workflows/feedback.ts` | 대화 맥락에서 OpenSpec 피드백 초안을 만들고, 파일 경로/비밀값/회사명/사용자명/URL을 익명화한 뒤 사용자 승인 후 제출한다. |

### 3.3 OpenSpec 워크플로우의 핵심 패턴

- 변경 작업을 `change` 단위로 관리한다.
- 구현 전에 proposal/spec/design/tasks 같은 artifact를 생성한다.
- `applyRequires`와 artifact dependency를 기준으로 다음 단계를 판단한다.
- `/opsx:apply`는 문서 artifact 기반으로 실제 코드를 수정하는 단계다.
- `/opsx:verify`, `/opsx:sync`, `/opsx:archive`가 구현 후 검증과 정리를 담당한다.
- `docs/workflows.md`, `docs/commands.md`, `docs/customization.md`가 템플릿 이해에 필요한 배경 문서다.

---

## 내 전용 스킬 제작 관점에서 참고할 점

### 가져올 만한 패턴

- `mattpocock/skills`
  - 개인 생산성/글쓰기/엔지니어링 작업을 작은 스킬로 나누는 방식
  - `setup-*` 스킬로 저장소별 전제 컨텍스트를 먼저 세팅하는 방식
  - TDD, diagnose, PRD, issue decomposition 같은 실무 중심 스킬 설계

- `obra/superpowers`
  - 작업 전 스킬 선택 → 브레인스토밍 → 계획 → 실행 → 검증 → 리뷰 → 마감으로 이어지는 강한 프로세스
  - “완료 주장 전 검증”처럼 실패 가능성이 큰 지점을 명시적으로 막는 규칙
  - subagent와 parallel agent를 프로세스의 일부로 다루는 방식

- `Fission-AI/OpenSpec`
  - 스킬과 slash command를 템플릿으로 생성하는 구조
  - 변경 관리 artifact를 dependency graph처럼 다루는 방식
  - `new`, `continue`, `apply`, `verify`, `archive`처럼 작업 생애주기를 명확한 명령으로 나누는 방식

### 주의할 점

- 그대로 복사하는 경우 MIT 라이선스 고지를 유지해야 한다.
- 단순 아이디어나 구조를 참고해 새로 작성하는 것은 보통 더 깔끔하다.
- 특정 스킬이 원본 문장, 체크리스트, 스크립트, 템플릿을 상당 부분 포함한다면 해당 skill 디렉터리 README 또는 파일 주석에 출처를 추가하는 것이 좋다.
- deprecated 또는 in-progress 스킬은 현재 사용 목적보다 패턴 참고용으로 보는 편이 안전하다.
