# parallel-execution

[English](README.md) | [한국어](README.kr.md)

독립적인 작업을 여러 subagent에 분산하고, controller가 통합과 최종 검증을 책임지는 in-progress 스킬이다.

## 구성

```text
parallel-execution/
├─ SKILL.md
├─ SKILL.kr.md
├─ README.md
├─ README.kr.md
└─ references/
   ├─ task-decomposition.md
   ├─ subagent-prompts.md
   └─ review-integration.md
```

## 파일 역할

- `SKILL.md`: 기본 스킬 정의와 병렬 실행 checklist.
- `SKILL.kr.md`: `SKILL.md`의 한국어판.
- `README.md`: 영어 원본 README.
- `README.kr.md`: 이 README의 한국어 번역본.
- `references/task-decomposition.md`: 병렬화 가능한 task와 순차화해야 하는 task를 구분하는 기준.
- `references/subagent-prompts.md`: self-contained subagent assignment 작성 기준과 template.
- `references/review-integration.md`: subagent 결과 검토, conflict 확인, 최종 검증 기준.

## 사용 범위

사용할 때:

- 독립적인 implementation task가 여러 개 있을 때
- 서로 다른 file/subsystem의 failure를 나눠 조사할 때
- codebase investigation이나 review를 병렬화할 때
- 겹치지 않는 파일의 mechanical edit를 분산할 때

핵심 규칙:

```text
분해 → self-contained dispatch → 결과 검토 → 통합 → 중앙 검증
```

subagent는 자기 task를 수행하고 보고한다. 통합과 최종 검증은 controller가 수행한다.

## Contract note

- 독립 병렬 요청은 하나의 `task` 배치에서 여러 `tasks[]`를 사용한다.
- 큰 slice의 리뷰는 필요할 때만 read-only reviewer를 사용하며, task brief, implementer report, review package(정확한 target/evidence 포함)를 `local://...`/`artifact://...`으로 전달한다.

## 레퍼런스 출처

이 스킬은 다음 레퍼런스를 바탕으로 정리했다.

- `obra/superpowers/skills/subagent-driven-development`
- `obra/superpowers/skills/dispatching-parallel-agents`

## 참고한 파일

다음 파일이 업데이트되면 이 스킬도 다시 검토한다.

- `references/obra/superpowers/skills/subagent-driven-development/SKILL.md`
- `references/obra/superpowers/skills/subagent-driven-development/implementer-prompt.md`
- `references/obra/superpowers/skills/subagent-driven-development/task-reviewer-prompt.md`
- `references/obra/superpowers/skills/subagent-driven-development/scripts/task-brief`
- `references/obra/superpowers/skills/subagent-driven-development/scripts/review-package`
- `references/obra/superpowers/skills/dispatching-parallel-agents/SKILL.md`

원본 저장소의 라이선스 고지는 루트 `NOTICE.md`를 따른다.
